from pydantic import BaseModel

class TermCreate(BaseModel):
    program_id: str
    term_number: int
