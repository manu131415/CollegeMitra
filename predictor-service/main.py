# predictor-service/main.py
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from db import init_db_pool, close_db_pool, get_pool, get_state_coords
from models import PredictRequest, PredictResponse
from scoring import (
    score_best_available,
    score_near_home,
    is_eligible_for_quota,
    is_quality_qualified,
    institute_type_rank,
    parse_nirf_rank,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db_pool()
    yield
    await close_db_pool()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Predictor service is running. See /docs for API."}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
async def predict(req: PredictRequest):
    institute_types = ["IIT"] if req.exam == "jee_adv" else ["NIT", "IIIT", "GFTI"]

    pool = get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT DISTINCT ON (i.institute_id, p.program_id, j.quota)
                i.institute_name,
                i.state,
                i.type,
                i.latitude,
                i.longitude,
                i.nirf_rank,
                i.annual_fees,
                i.median_package_lpa,
                p.program_name,
                j.quota,
                j.seat_type,
                j.closing_rank,
                j.year,
                j.round
            FROM jossa_ranks j
            JOIN institutes i ON i.institute_id = j.institute_id
            JOIN programs p ON p.program_id = j.program_id
            WHERE j.seat_type = $1
              AND j.closing_rank >= $2 * 0.85
              AND i.type = ANY($3)
              AND i.institute_name NOT ILIKE '%Indian Institute of Science%'
            ORDER BY i.institute_id, p.program_id, j.quota, j.year DESC, j.round DESC
        """, req.category, req.rank, institute_types)

    # --- Eligibility filter: applies identically regardless of mode ---
    eligible_rows = [
        r for r in rows
        if is_eligible_for_quota(r["state"], req.home_state, r["quota"])
    ]

    def to_result(r, score, dist=None):
        nirf_rank = parse_nirf_rank(r["nirf_rank"])
        return {
            "institute_name": r["institute_name"],
            "branch": r["program_name"],
            "state": r["state"] or "Unknown",
            "nirf_rank": int(nirf_rank),
            "fee": float(r["annual_fees"] or 0),
            "median_package": float(r["median_package_lpa"] or 0),
            "distance_km": dist,
            "match_score": score,
        }

    # --- Build BOTH result sets so we can always return a comparison ---
    home = await get_state_coords(req.home_state)
    if home is None:
        raise HTTPException(status_code=400, detail=f"Unknown state: {req.home_state}")
    home_lat, home_lng = home["latitude"], home["longitude"]

    best_results = sorted(
        (to_result(r, score_best_available(r)) for r in eligible_rows),
        key=lambda x: x["match_score"],
        reverse=True,
    )

    near_home_results = sorted(
        (
            {**to_result(r, *score_near_home(r, home_lat, home_lng)),
             "_quality_qualified": is_quality_qualified(r),
             "_type_rank": institute_type_rank(r)}
            for r in eligible_rows
        ),
        key=lambda x: (
            0 if x["_quality_qualified"] else 1,  # quality-qualified institutes always rank above unranked ones
            x["_type_rank"],                       # within that tier: IIT > NIT > IIIT > GFTI
            x["distance_km"],
            -x["match_score"],
        ),
    )
    for r in near_home_results:
        r.pop("_quality_qualified", None)
        r.pop("_type_rank", None)

    comparison = {
        "best_available": _to_comparison_pick(best_results[0]) if best_results else None,
        "near_home": _to_comparison_pick(near_home_results[0]) if near_home_results else None,
    }

    results = best_results if req.preference == "best" else near_home_results

    return {"results": results[:20], "comparison": comparison}


def _to_comparison_pick(result: dict):
    return {
        "institute_name": result["institute_name"],
        "branch": result["branch"],
        "state": result["state"],
        "nirf_rank": result["nirf_rank"],
        "median_package": result["median_package"],
        "distance_km": result["distance_km"],
    }