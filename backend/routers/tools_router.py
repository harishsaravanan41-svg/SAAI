from fastapi import APIRouter, Depends, Query
from typing import Optional
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.database.models import User
from backend.auth.dependencies import get_current_user, require_student
from backend.database import repositories

router = APIRouter(prefix="/api/tools", tags=["Backend Tool Direct APIs"])

@router.get("/departments")
def get_departments_api(db: Session = Depends(get_db)):
    """Direct invocation of Tool 1: Departments"""
    return repositories.tool_get_departments(db)

@router.get("/staff")
def get_staff_api(
    department: Optional[str] = Query(None, description="Department filter"),
    role: Optional[str] = Query(None, description="Role filter"),
    db: Session = Depends(get_db)
):
    """Direct invocation of Tool 2: Staff"""
    return repositories.tool_get_staff(db, department_name=department, role=role)

@router.get("/events")
def get_events_api(
    department: Optional[str] = Query(None, description="Department filter"),
    club: Optional[str] = Query(None, description="Club filter"),
    db: Session = Depends(get_db)
):
    """Direct invocation of Tool 3: Events"""
    return repositories.tool_get_events(db, department_name=department, club_name=club)

@router.get("/clubs")
def get_clubs_api(db: Session = Depends(get_db)):
    """Direct invocation of Tool 4: Clubs"""
    return repositories.tool_get_clubs(db)

@router.get("/my-result")
def get_my_result_api(
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """
    Direct invocation of Tool 5: Personal Result
    Bound strictly to authenticated user's register number.
    """
    if not current_user.register_number:
        return {
            "status": "NOT_FOUND",
            "message": "User does not have a linked student register number.",
            "data": None
        }
    return repositories.tool_get_my_result(db, register_number=current_user.register_number)
