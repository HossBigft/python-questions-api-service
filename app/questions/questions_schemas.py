from pydantic import BaseModel, Field


class QuestionSchema(BaseModel):
    text: str = Field(max_length=255, description="Question text")
    
    model_config = {
        "from_attributes": True 
    }


class AnswerSchema(BaseModel):
    text: str = Field(max_length=10000, description="Answer to the question")
