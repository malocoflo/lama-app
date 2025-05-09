from pydantic import BaseModel

class Requestmodel(BaseModel):
    question: str