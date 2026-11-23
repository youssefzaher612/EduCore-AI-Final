"""Student-facing AI functionality.

Keep commonly used analytics exports here so existing imports such as
``from educore.student_ai import build_mastery`` remain compatible.
"""
from .analytics import BKT, MIN_ATTEMPTS, bkt_update, build_mastery, create_study_plan

__all__ = [
    "BKT", "MIN_ATTEMPTS", "bkt_update", "build_mastery", "create_study_plan",
]
