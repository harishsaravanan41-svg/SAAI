from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import text

def tool_get_departments(db: Session) -> Dict[str, Any]:
    """Retrieve all department information."""
    sql = text("SELECT department_id, name, url FROM departments ORDER BY department_id ASC")
    result = db.execute(sql).mappings().all()

    if not result:
        return {
            "status": "NOT_FOUND",
            "message": "No departments found in the system.",
            "data": []
        }

    return {
        "status": "SUCCESS",
        "message": f"Found {len(result)} department(s).",
        "data": [dict(r) for r in result]
    }


def tool_get_staff(
    db: Session,
    department_name: Optional[str] = None,
    role: Optional[str] = None
) -> Dict[str, Any]:
    """Retrieve faculty/staff information filtered by department name or role."""
    conditions = []
    params: Dict[str, Any] = {}

    sql_str = """
        SELECT 
            s.staff_id,
            s.name AS staff_name,
            s.role,
            s.email,
            s.phone,
            s.qualification,
            d.name AS department_name
        FROM staff s
        LEFT JOIN departments d ON s.department_id = d.department_id
    """

    if department_name:
        conditions.append("(d.name LIKE :dept_pattern)")
        params["dept_pattern"] = f"%{department_name.strip()}%"

    if role:
        conditions.append("(s.role LIKE :role_pattern)")
        params["role_pattern"] = f"%{role.strip()}%"

    if conditions:
        sql_str += " WHERE " + " AND ".join(conditions)

    sql_str += " ORDER BY s.staff_id ASC"

    result = db.execute(text(sql_str), params).mappings().all()

    if not result:
        filter_desc = []
        if department_name:
            filter_desc.append(f"department '{department_name}'")
        if role:
            filter_desc.append(f"role '{role}'")
        criteria = " and ".join(filter_desc) if filter_desc else "specified criteria"

        return {
            "status": "NOT_FOUND",
            "message": f"No faculty or staff found matching {criteria}.",
            "data": []
        }

    return {
        "status": "SUCCESS",
        "message": f"Found {len(result)} staff member(s).",
        "data": [dict(r) for r in result]
    }


def tool_get_events(
    db: Session,
    department_name: Optional[str] = None,
    club_name: Optional[str] = None
) -> Dict[str, Any]:
    """Retrieve college events associated with departments, clubs, or general campus."""
    conditions = []
    params: Dict[str, Any] = {}

    sql_str = """
        SELECT 
            e.event_id,
            e.title,
            e.event_date,
            e.venue,
            e.description,
            e.url,
            d.name AS department_name,
            c.name AS club_name
        FROM events e
        LEFT JOIN departments d ON e.department_id = d.department_id
        LEFT JOIN clubs c ON e.club_id = c.club_id
    """

    if department_name:
        conditions.append("(d.name LIKE :dept_pattern)")
        params["dept_pattern"] = f"%{department_name.strip()}%"

    if club_name:
        conditions.append("(c.name LIKE :club_pattern)")
        params["club_pattern"] = f"%{club_name.strip()}%"

    if conditions:
        sql_str += " WHERE " + " OR ".join(conditions) if (department_name and club_name) else " WHERE " + " AND ".join(conditions)

    sql_str += " ORDER BY e.event_date DESC"

    result = db.execute(text(sql_str), params).mappings().all()

    if not result:
        filter_desc = []
        if department_name:
            filter_desc.append(f"department '{department_name}'")
        if club_name:
            filter_desc.append(f"club '{club_name}'")
        criteria = " / ".join(filter_desc) if filter_desc else "the requested criteria"

        return {
            "status": "NOT_FOUND",
            "message": f"No upcoming or recorded events found for {criteria}.",
            "data": []
        }

    data = []
    for r in result:
        item = dict(r)
        if item.get("event_date"):
            item["event_date"] = str(item["event_date"])
        data.append(item)

    return {
        "status": "SUCCESS",
        "message": f"Found {len(data)} event(s).",
        "data": data
    }


def tool_get_clubs(db: Session) -> Dict[str, Any]:
    """Retrieve college clubs information."""
    sql = text("SELECT club_id, name, parent_body FROM clubs ORDER BY club_id ASC")
    result = db.execute(sql).mappings().all()

    if not result:
        return {
            "status": "NOT_FOUND",
            "message": "No active clubs found in the system.",
            "data": []
        }

    return {
        "status": "SUCCESS",
        "message": f"Found {len(result)} club(s).",
        "data": [dict(r) for r in result]
    }


def tool_get_my_result(db: Session, register_number: int) -> Dict[str, Any]:
    """
    Retrieve academic results strictly scoped to the authenticated student's register number.
    Security: The register_number MUST be injected by the backend session, never from AI input.
    """
    sql_str = """
        SELECT 
            sr.register_number,
            sr.name AS student_name,
            d.name AS department_name,
            sr.python_practical,
            sr.tamil,
            sr.english,
            sr.python,
            sr.office_automation,
            sr.naan_mudhalvan,
            sr.main_total,
            sr.percentage,
            sr.rank
        FROM student_result sr
        LEFT JOIN departments d ON sr.department_id = d.department_id
        WHERE sr.register_number = :reg_no
    """
    result = db.execute(text(sql_str), {"reg_no": register_number}).mappings().first()

    if not result:
        return {
            "status": "NOT_FOUND",
            "message": f"No academic result records found for register number {register_number}.",
            "data": None
        }

    res_dict = dict(result)
    if res_dict.get("percentage") is not None:
        res_dict["percentage"] = float(res_dict["percentage"])

    res_dict["subjects"] = {
        "Python Practical": res_dict.get("python_practical"),
        "Tamil": res_dict.get("tamil"),
        "English": res_dict.get("english"),
        "Python": res_dict.get("python"),
        "Office Automation": res_dict.get("office_automation"),
        "Naan Mudhalvan": res_dict.get("naan_mudhalvan"),
    }

    return {
        "status": "SUCCESS",
        "message": f"Academic record retrieved successfully for {res_dict['student_name']}.",
        "data": res_dict
    }
