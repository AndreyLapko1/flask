from pydantic import BaseModel, Field

class CreateQuestion(BaseModel):
    text: str = Field(..., min_length=5)
    category: str




class ResponseQuestion(BaseModel):
    text: str
    # category: str | None
    model_config = {
        'from_attributes': True
    }

class CategoryBase(BaseModel):
    text: str


class MessageResponse(BaseModel):
    msg: str



