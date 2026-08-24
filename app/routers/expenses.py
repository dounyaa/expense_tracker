from datetime import date
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import ExpenseDB

router = APIRouter(
    prefix="/expenses",
)

@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)) -> ExpenseDB:
    new_expense = ExpenseDB(
        amount=expense.amount,
        category=expense.category,
        description=expense.description,
        date=date.today(),
        is_recurring=expense.is_recurring,
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

@router.get("/", response_model=list[ExpenseResponse])
def list_all_expenses(category: str | None = None, db: Session = Depends(get_db)) -> list[ExpenseResponse]:
    query = db.query(ExpenseDB)
    if category is not None:
        query = query.filter(ExpenseDB.category == category)
    return query.all()

@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: int, db: Session = Depends(get_db)) -> ExpenseResponse:
    expense = db.query(ExpenseDB).filter(ExpenseDB.id == expense_id).first()
    if expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dépense introuvable")
    return expense

# PUT /expenses/{expense_id}
@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, new_expense: ExpenseUpdate, db: Session = Depends(get_db)) -> ExpenseResponse:
    expense = db.query(ExpenseDB).filter(ExpenseDB.id == expense_id).first()
    if expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dépense introuvable")
    expense.amount = new_expense.amount
    expense.category = new_expense.category
    expense.description = new_expense.description
    db.commit()
    db.refresh(expense)
    return expense


# DELETE /expenses/{expense_id}
@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int, db: Session = Depends(get_db)) -> None:
    expense = db.query(ExpenseDB).filter(ExpenseDB.id == expense_id).first()
    if expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dépense introuvable")
    db.delete(expense)
    db.commit()
