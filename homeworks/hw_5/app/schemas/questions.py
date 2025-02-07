from pydantic import BaseModel, Field

class CreateQuestion(BaseModel):
    text: str = Field(..., min_length=5)
    category_id: int = Field(...)




class ResponseQuestion(BaseModel):
    text: str
    category_id: int
    model_config = {
        'from_attributes': True
    }

class CategoryBase(BaseModel):
    text: str


class MessageResponse(BaseModel):
    msg: str



