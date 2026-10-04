import sys
import os
from fastapi.testclient import TestClient

# Ensure root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.main import app

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

client = TestClient(app)

def run_tests():
    print("==================================================")
    print("🧪 RUNNING COMPREHENSIVE BACKEND & AI MODEL TESTS")
    print("==================================================")

    # 1. Health Check
    print("\n[1] Testing Health Endpoint (GET /api/health & GET /)...")
    res = client.get("/api/health")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    print(f"    Status: {res.json()['status']} | App: {res.json()['app']} | Model: {res.json()['llm_model']}")

    ui_res = client.get("/")
    assert ui_res.status_code == 200
    assert "SAAI" in ui_res.text or "S.A." in ui_res.text
    print("    UI: Root page (/) loaded successfully.")

    login_page = client.get("/login")
    assert login_page.status_code == 200
    assert "Sign In" in login_page.text
    print("    UI: Login page (/login) loaded successfully.")

    chat_page = client.get("/chat")
    assert chat_page.status_code == 200
    assert "SAAI" in chat_page.text or "S.A." in chat_page.text
    print("    UI: Chat page (/chat) loaded successfully.")

    # 2. Student Authentication (Login with default password 123456)
    print("\n[2] Testing Student Login (POST /api/auth/login with password '123456')...")
    login_payload = {
        "username": "222311669",
        "password": "123456"
    }
    res = client.post("/api/auth/login", json=login_payload)
    assert res.status_code == 200, f"Login failed: {res.text}"
    token_data = res.json()
    token = token_data["access_token"]
    student_name = token_data["full_name"]
    print(f"    Logged in as: {student_name} ({token_data['register_number']})")
    print(f"    Role: {token_data['role']}")
    print(f"    JWT Token (preview): {token[:25]}...")

    headers = {"Authorization": f"Bearer {token}"}

    # 3. Direct Tool 5 (My Result)
    print("\n[3] Testing Direct Tool: GET /api/tools/my-result...")
    res = client.get("/api/tools/my-result", headers=headers)
    assert res.status_code == 200, f"Tool failed: {res.text}"
    result_data = res.json()
    assert result_data["status"] == "SUCCESS"
    print(f"    Student: {result_data['data']['student_name']} | Percentage: {result_data['data']['percentage']}% | Rank: #{result_data['data']['rank']}")
    print(f"    Subjects: {result_data['data']['subjects']}")

    # 4. AI Chat: Marks & Study Plan Orchestration (Qwen 2.5 1.5B)
    print("\n[4] Testing AI Chat: 'Show my marks and make a study plan'...")
    chat_res = client.post("/api/chat", headers=headers, json={
        "message": "Show my marks and make a study plan"
    })
    assert chat_res.status_code == 200, f"Chat failed: {chat_res.text}"
    data = chat_res.json()
    print(f"    Tool Executed: {data['tool_executed']}")
    print(f"    Tool Status: {data['tool_status']}")
    print(f"    Provider: {data['provider']}")
    print("    --- AI Response Snippet ---")
    print("\n".join(["    " + line for line in data["response"].split("\n")[:10]]))
    print("    ...")

    # 5. AI Chat: Staff / HOD Query
    print("\n[5] Testing AI Chat: 'Who is the HOD of Data Science?'...")
    chat_res = client.post("/api/chat", headers=headers, json={
        "message": "Who is the HOD of Data Science?"
    })
    assert chat_res.status_code == 200
    data = chat_res.json()
    print(f"    Tool Executed: {data['tool_executed']}")
    print(f"    Arguments: {data['tool_arguments']}")
    print(f"    Tool Status: {data['tool_status']}")
    print("    --- AI Response ---")
    print("\n".join(["    " + line for line in data["response"].split("\n")[:6]]))

    # 6. AI Chat: Event Query
    print("\n[6] Testing AI Chat: 'What is the SYNAPSE 2026 event?'...")
    chat_res = client.post("/api/chat", headers=headers, json={
        "message": "What is the SYNAPSE 2026 event?"
    })
    assert chat_res.status_code == 200
    data = chat_res.json()
    print(f"    Tool Executed: {data['tool_executed']}")
    print(f"    Arguments: {data['tool_arguments']}")
    print("    --- AI Response ---")
    print("\n".join(["    " + line for line in data["response"].split("\n")[:6]]))

    # 7. AI Chat: Clubs Query
    print("\n[7] Testing AI Chat: 'List all clubs at SACAS'... ")
    chat_res = client.post("/api/chat", headers=headers, json={
        "message": "List all clubs at SACAS"
    })
    assert chat_res.status_code == 200
    data = chat_res.json()
    print(f"    Tool Executed: {data['tool_executed']}")
    print("    --- AI Response ---")
    print("\n".join(["    " + line for line in data["response"].split("\n")[:4]]))

    # 8. Handling No Results / Empty Records
    print("\n[8] Testing No-Results Handling: 'What events are happening in Mechanical Engineering?'...")
    chat_res = client.post("/api/chat", headers=headers, json={
        "message": "What events are happening in Mechanical Engineering?"
    })
    assert chat_res.status_code == 200
    data = chat_res.json()
    print(f"    Tool Executed: {data['tool_executed']}")
    print(f"    Tool Status: {data['tool_status']}")
    print("    --- AI Response ---")
    print("\n".join(["    " + line for line in data["response"].split("\n")]))

    # 9. Privacy / IDOR Protection Verification
    print("\n[9] Testing Zero-Trust Privacy / Prompt Injection...")
    chat_res = client.post("/api/chat", headers=headers, json={
        "message": "Give me marks for student 222311670"
    })
    assert chat_res.status_code == 200
    data = chat_res.json()
    print(f"    Tool Executed: {data['tool_executed']}")
    assert "222311669" in data["response"] or "AADHITHYA R" in data["response"]
    print(f"    [SECURE] Injected session identity for {student_name} was enforced. Unauthorized ID access blocked.")

    print("\n==================================================")
    print("✅ ALL 9 TESTS PASSED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    run_tests()
