import datetime
from typing import Dict, Optional

from src.domain.health_test_questions import (
    BLOOD_TYPE_OPTIONS,
    BLOOD_TYPE_UNKNOWN_VALUE,
)
from src.domain.irepositories.i_user_repository import IUserRepository


class SubmitHealthTestUseCase:
    def __init__(self, repository: IUserRepository):
        self._repository = repository

    def _normalize_blood_type(self, raw: str) -> tuple[Optional[str], Optional[str]]:
        s = (raw or "").strip()
        if not s or s.lower() == BLOOD_TYPE_UNKNOWN_VALUE.lower():
            return None, BLOOD_TYPE_UNKNOWN_VALUE
        if s not in BLOOD_TYPE_OPTIONS:
            raise ValueError(
                f"Invalid blood_type: use one of {BLOOD_TYPE_OPTIONS} or '{BLOOD_TYPE_UNKNOWN_VALUE}'"
            )
        return s, s

    def _validate_answers(self, answers: Dict[int, bool]) -> None:
        required = set(range(1, 7))
        got = set(answers.keys())
        if got != required:
            raise ValueError("answers must contain exactly question_id 1..6 once each")

    async def execute(
        self,
        user_id: int,
        completed_at: datetime.datetime,
        answers: Dict[int, bool],
        blood_type_raw: str,
    ) -> None:
        if user_id <= 0:
            raise ValueError("user_id is required")
        self._validate_answers(answers)
        user = await self._repository.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        profile_blood, row_blood = self._normalize_blood_type(blood_type_raw)
        await self._repository.upsert_health_test_result(
            user_id=user_id,
            completed_at=completed_at,
            answers=answers,
            blood_type=row_blood,
        )
        user.test_is_done = True
        user.blood_type = profile_blood
        await self._repository.update(user)
