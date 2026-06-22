# predictor-service/models.py
from pydantic import BaseModel
from typing import Optional, Literal


class PredictRequest(BaseModel):
    rank: int
    category: str                                   # seat_type: OPEN / OBC-NCL / SC / ST / EWS
    home_state: str
    exam: Literal["jee_main", "jee_adv"] = "jee_main"  # jee_main -> NIT/IIIT/GFTI, jee_adv -> IIT
    preference: Literal["best", "near_home"] = "best"
    branch_preference: Optional[list[str]] = None    # reserved for future use


class InstituteResult(BaseModel):
    institute_name: str
    branch: str
    state: str
    nirf_rank: int
    fee: float
    median_package: float
    distance_km: Optional[float] = None
    match_score: float


class ComparisonPick(BaseModel):
    institute_name: str
    branch: str
    state: str
    nirf_rank: int
    median_package: float
    distance_km: Optional[float] = None


class PredictResponse(BaseModel):
    results: list[InstituteResult]
    comparison: dict[str, Optional[ComparisonPick]]  # {"best_available": ..., "near_home": ...}