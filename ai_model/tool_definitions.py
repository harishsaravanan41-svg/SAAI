from typing import List, Dict, Any

TOOLS_DEFINITIONS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "tool_get_departments",
            "description": "Retrieve all academic departments offered at SACAS with official web links.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "tool_get_staff",
            "description": "Retrieve information about professors, HODs, and staff members by department name and/or role.",
            "parameters": {
                "type": "object",
                "properties": {
                    "department_name": {
                        "type": "string",
                        "description": "Name or partial name of the department (e.g. 'Data Science', 'Computer Science', 'Artificial Intelligence')"
                    },
                    "role": {
                        "type": "string",
                        "description": "Role of the staff member (e.g. 'Head of the Department', 'HOD', 'Assistant Professor', 'Associate Professor')"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "tool_get_events",
            "description": "Retrieve college events, symposiums, cleanups, celebrations, or workshops organized by departments or clubs.",
            "parameters": {
                "type": "object",
                "properties": {
                    "department_name": {
                        "type": "string",
                        "description": "Name or partial name of the department organizing the event (e.g. 'Data Science')"
                    },
                    "club_name": {
                        "type": "string",
                        "description": "Name or partial name of the club organizing the event (e.g. 'Rotaract', 'Exnora')"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "tool_get_clubs",
            "description": "Retrieve all student clubs and extension cells active at SACAS.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "tool_get_my_result",
            "description": "Retrieve the current authenticated student's academic marks, subjects, overall total, percentage, and rank.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]
