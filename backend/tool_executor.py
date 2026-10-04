from typing import Dict, Any
from sqlalchemy.orm import Session
from backend.database import repositories
from backend.database.models import User

ALLOWED_TOOLS = {
    "tool_get_departments",
    "tool_get_staff",
    "tool_get_events",
    "tool_get_clubs",
    "tool_get_my_result"
}

def execute_tool_call(
    tool_name: str,
    tool_args: Dict[str, Any],
    db: Session,
    current_user: User
) -> Dict[str, Any]:
    """
    Executes a requested tool function with strict authorization and session-based identity binding.
    """
    if tool_name not in ALLOWED_TOOLS:
        return {
            "status": "ERROR",
            "message": f"Unauthorized or unrecognized tool: '{tool_name}'",
            "data": None
        }

    try:
        # Tool 1: Departments
        if tool_name == "tool_get_departments":
            return repositories.tool_get_departments(db)

        # Tool 2: Staff
        elif tool_name == "tool_get_staff":
            dept = tool_args.get("department_name")
            role = tool_args.get("role")
            return repositories.tool_get_staff(db, department_name=dept, role=role)

        # Tool 3: Events
        elif tool_name == "tool_get_events":
            dept = tool_args.get("department_name")
            club = tool_args.get("club_name")
            return repositories.tool_get_events(db, department_name=dept, club_name=club)

        # Tool 4: Clubs
        elif tool_name == "tool_get_clubs":
            return repositories.tool_get_clubs(db)

        # Tool 5: Student Personal Results
        elif tool_name == "tool_get_my_result":
            # SECURITY CHECK: Zero-trust session identity injection
            if not current_user.register_number:
                return {
                    "status": "NOT_FOUND",
                    "message": "Current authenticated user does not have a linked student register number.",
                    "data": None
                }
            
            return repositories.tool_get_my_result(db, register_number=current_user.register_number)

    except Exception as e:
        return {
            "status": "ERROR",
            "message": f"Database execution error: {str(e)}",
            "data": None
        }

    return {
        "status": "ERROR",
        "message": "Tool execution could not be completed.",
        "data": None
    }
