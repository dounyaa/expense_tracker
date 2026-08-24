from pydantic import BaseModel, Field
from datetime import date

class ExpenseCreate(BaseModel):
    amount : float = Field(gt=0.0)
    category : str = Field(min_length=3, max_length=25)
    description : str = Field(min_length=3, max_length=50)
    is_recurring : bool = Field(default=False)

class ExpenseResponse(BaseModel):
    id : int
    amount : float
    category : str
    description : str
    date : date
    is_recurring : bool = Field(default=False)

    model_config = {"from_attributes": True}

class ExpenseUpdate(BaseModel):
    amount : float = Field(gt=0.0)
    category : str = Field(min_length=3, max_length=25)
    description : str = Field(min_length=3, max_length=50)
    