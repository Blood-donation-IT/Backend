from src.domain.health_test_questions import (
    BLOOD_TYPE_OPTIONS,
    BLOOD_TYPE_UNKNOWN_VALUE,
    HEALTH_TEST_QUESTIONS,
)


class GetHealthTestQuestionsUseCase:
    def execute(self) -> dict:
        return {
            "questions": [
                {"question_id": qid, "text": text} for qid, text in HEALTH_TEST_QUESTIONS
            ],
            "blood_type_options": list(BLOOD_TYPE_OPTIONS),
            "blood_type_unknown_value": BLOOD_TYPE_UNKNOWN_VALUE,
        }
