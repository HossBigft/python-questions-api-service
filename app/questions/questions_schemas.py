from pydantic import BaseModel, Field


class QuestionOut(BaseModel):
    id:int
    text: str = Field(max_length=255, description="Question text")
    
    model_config = {
        "from_attributes": True 
    }
class QuestionIn(BaseModel):
    text: str = Field(max_length=255, description="Question text")
    


