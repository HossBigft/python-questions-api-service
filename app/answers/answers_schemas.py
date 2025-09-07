from pydantic import BaseModel, Field
from datetime import datetime


class AnswerIn(BaseModel):
    text: str = Field(min_length=1,max_length=10000, description="Answer to the question")


class AnswerOut(BaseModel):
    id: int
    text: str = Field(max_length=10000, description="Answern text")
    created_at: datetime
    model_config = {"from_attributes": True}
