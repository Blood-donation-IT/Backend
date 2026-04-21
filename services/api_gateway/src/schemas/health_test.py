from datetime import datetime
from typing import List, Optional

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class HealthTestQuestionOut(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    question_id: int = Field(serialization_alias="questionId")
    text: str


class GetHealthTestResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    questions: List[HealthTestQuestionOut]
    blood_type_options: List[str] = Field(serialization_alias="bloodTypeOptions")
    blood_type_unknown_value: str = Field(serialization_alias="bloodTypeUnknownValue")


class HealthTestAnswerIn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    question_id: int = Field(
        validation_alias=AliasChoices("questionId", "question_id")
    )
    value: bool


class PostHealthTestRequest(BaseModel):
    """userId from body is ignored; owner is taken from JWT."""

    model_config = ConfigDict(populate_by_name=True)
    user_id: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("userId", "user_id"),
    )
    completed_at: datetime = Field(
        validation_alias=AliasChoices("completedAt", "completed_at")
    )
    answers: List[HealthTestAnswerIn]
    blood_type: str = Field(
        default="",
        validation_alias=AliasChoices("bloodType", "blood_type"),
        serialization_alias="bloodType",
    )


class PostHealthTestResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    success: bool
    message: str
