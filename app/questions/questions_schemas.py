from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

from app.answers.answers_schemas import AnswerOut


class QuestionOut(BaseModel):
    id: int
    text: str = Field(max_length=255, description="Question text")
    created_at: datetime
    answers: List[AnswerOut] | None
    model_config = {"from_attributes": True}


class QuestionIn(BaseModel):
    text: str = Field(min_length=3, max_length=255, description="Question text")
