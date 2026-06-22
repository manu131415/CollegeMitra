# predictor-service/scoring.py
from math import radians, sin, cos, sqrt, atan2

# --- Branch tier hierarchy (Phase 1: fixed, no per-branch package data yet) ---
# Higher tier = bigger bonus. Tune these bonus values as you see real outcomes.
BRANCH_TIERS = {
    # Tier 1 — highest market demand / outcomes
    "computer science": 15,
    "computer science and engineering": 15,
    "cse": 15,
    "information technology": 14,
    "it": 14,
    "electronics and communication": 12,
    "electronics and communication engineering": 12,
    "ece": 12,

    # Tier 2 — strong, steady outcomes
    "electrical engineering": 8,
    "electrical": 8,
    "mechanical engineering": 6,
    "mechanical": 6,
    "chemical engineering": 6,
    "chemical": 6,

    # Tier 3 — everything else, including civil
    "civil engineering": 2,
    "civil": 2,
}
DEFAULT_BRANCH_BONUS = 3  # any branch not explicitly listed above


def branch_bonus(program_name: str) -> float:
    if not program_name:
        return DEFAULT_BRANCH_BONUS
    key = program_name.strip().lower()
    return BRANCH_TIERS.get(key, DEFAULT_BRANCH_BONUS)


# Institutes that are mistagged in the source data (e.g. IISc is stored as
# type='GFTI' even though it isn't a standard Government Funded Technical
# Institute in the JoSAA sense). Keyed by a lowercase substring match against
# institute_name. Maps to the effective type Claude/the scoring logic should
# treat them as, for sorting/tiering purposes — does not touch the DB.
INSTITUTE_TYPE_OVERRIDES = {
    "indian institute of science": "IISc",
}

# Sort weight for the quality-qualified tier's tiebreak: lower number = ranked first.
INSTITUTE_TYPE_RANK = {
    "IIT": 0,
    "NIT": 1,
    "IIIT": 2,
    "GFTI": 3,
    "IISc": 0,  # treat as IIT-tier prestige, but see exclusion note below
}
DEFAULT_TYPE_RANK = 4


def effective_institute_type(row) -> str:
    """Returns the institute's type, correcting known data mistags by name."""
    name = (row["institute_name"] or "").strip().lower()
    for substring, override_type in INSTITUTE_TYPE_OVERRIDES.items():
        if substring in name:
            return override_type
    return (row["type"] or "").strip().upper()


def institute_type_rank(row) -> int:
    """Lower = higher priority. Used as a tiebreaker within the quality-qualified tier."""
    return INSTITUTE_TYPE_RANK.get(effective_institute_type(row), DEFAULT_TYPE_RANK)


def haversine(lat1, lng1, lat2, lng2):
    if lat1 is None or lng1 is None or lat2 is None or lng2 is None:
        return 9999.0
    R = 6371
    dlat, dlng = radians(float(lat2) - float(lat1)), radians(float(lng2) - float(lng1))
    a = sin(dlat / 2) ** 2 + cos(radians(float(lat1))) * cos(radians(float(lat2))) * sin(dlng / 2) ** 2
    return 2 * R * atan2(sqrt(a), sqrt(1 - a))


def parse_nirf_rank(value, default=9999) -> float:
    """
    Handles the real formats found in nirf_rank (VARCHAR column):
      - plain numbers:      "42"      -> 42
      - rank bands:         "100-150" -> 125 (midpoint)
      - unranked:           "Not Ranked", None, "", etc. -> default
    """
    if value is None:
        return default

    text = str(value).strip()
    if not text:
        return default

    # Plain integer
    try:
        return float(text)
    except ValueError:
        pass

    # Range like "100-150"
    if "-" in text:
        parts = text.split("-")
        if len(parts) == 2:
            try:
                low = float(parts[0].strip())
                high = float(parts[1].strip())
                return (low + high) / 2
            except ValueError:
                pass

    # Anything else (e.g. "Not Ranked") falls back to default
    return default


def safe_num(value, default=0.0):
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def score_best_available(row):
    """Best Available: pure quality signal. NIRF rank + branch tier. No distance, no fee."""
    nirf_rank = parse_nirf_rank(row["nirf_rank"])
    nirf_score = max(0, 100 - nirf_rank)
    bonus = branch_bonus(row["program_name"])

    total = nirf_score + bonus
    return round(total, 2)


def score_near_home(row, home_lat, home_lng):
    """Near Home: distance dominates. NIRF + branch tier only break ties."""
    dist_km = haversine(home_lat, home_lng, row["latitude"], row["longitude"])

    nirf_rank = parse_nirf_rank(row["nirf_rank"])
    nirf_score = max(0, 100 - nirf_rank)
    bonus = branch_bonus(row["program_name"])
    proximity_score = max(0, 300 - dist_km)  # distance dominates the total

    total = proximity_score * 0.75 + (nirf_score + bonus) * 0.25
    return round(total, 2), round(dist_km, 1)


def is_quality_qualified(row) -> bool:
    """
    Hard floor for 'near home' mode: an institute only qualifies for the
    quality-first tier if it has a real (non-default) NIRF rank, or is an
    IIT/NIT/IIIT (inherently reputable even without that year's NIRF entry).
    Anything else (unranked, unknown-type institutes) is shown but ranked
    after every quality-qualified institute, regardless of distance.
    """
    nirf_rank = parse_nirf_rank(row["nirf_rank"])
    if nirf_rank < 9999:
        return True
    institute_type = effective_institute_type(row)
    return institute_type in ("IIT", "NIT", "IIIT", "IISc")


def is_eligible_for_quota(institute_state: str, home_state: str, quota: str) -> bool:
    """Correctness gate, not a preference. HS quota only valid when institute is in student's home state."""
    if quota == "AI":
        return True
    same_state = (institute_state or "").strip().lower() == (home_state or "").strip().lower()
    if quota == "HS":
        return same_state
    if quota == "OS":
        return not same_state
    return False