"""Backward-compatible imports; schemas live in educore.student_ai.schemas."""
from educore.student_ai.schemas import (
    CourseTopicOutput, CourseTopicsOutput, StudyPlanEntryOutput, StudyPlanOutput,
    StudentExamQuestionOutput, StudentExamOutput,
)

__all__ = [
    "CourseTopicOutput", "CourseTopicsOutput", "StudyPlanEntryOutput",
    "StudyPlanOutput", "StudentExamQuestionOutput", "StudentExamOutput",
]
