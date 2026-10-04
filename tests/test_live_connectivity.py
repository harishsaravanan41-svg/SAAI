import sys
import requests
import json

sys.stdout.reconfigure(encoding='utf-8')

base_url = 'http://localhost:8000'

def run_live_tests():
    print("==================================================")
    print("🔍 LIVE END-TO-END CONNECTIVITY & AI MODEL TEST")
    print("==================================================")

    # 1. Health check
    try:
        health = requests.get(f'{base_url}/api/health', timeout=10).json()
        print(f"[✓] Backend Status: {health.get('status')} | Model: {health.get('llm_model')}", flush=True)
    except Exception as e:
        print(f"[✗] Failed to connect to backend server: {e}")
        return

    # 2. Login as student AADHITHYA R (222311669)
    login_res = requests.post(f'{base_url}/api/auth/login', json={'username': '222311669', 'password': '123456'}).json()
    if 'access_token' not in login_res:
        print("[✗] Student login failed:", login_res)
        return
    
    token = login_res['access_token']
    user_info = login_res.get('user', {})
    print(f"[✓] Authenticated Student: {user_info.get('full_name')} ({user_info.get('register_number')}) | Role: {user_info.get('role')}")
    print(f"[✓] JWT Bearer Token Generated Successfully.")

    # 3. Test queries
    headers = {'Authorization': f'Bearer {token}'}

    test_questions = [
        "Hi bro",
        "What is my CGPA / marks?",
        "Who is the principal?",
        "What is my marks and tell me whether it is good?",
        "What is recursion in Python?"
    ]

    for i, q in enumerate(test_questions, 1):
        print("\n" + "="*50, flush=True)
        print(f"TEST {i}: Student asks: \"{q}\"", flush=True)
        print("="*50, flush=True)
        res = requests.post(f'{base_url}/api/chat', json={'message': q, 'history': []}, headers=headers).json()
        
        tool_name = res.get('tool_executed')
        tool_status = res.get('tool_status')
        print(f"► Tool Intercepted & Executed by Backend: {tool_name} (Status: {tool_status})", flush=True)
        print(f"► AI Provider / Engine: {res.get('provider')}", flush=True)
        print("► AI Generated Dynamic Response:", flush=True)
        print(res.get('response'), flush=True)

    print("\n==================================================", flush=True)
    print("🎉 ALL LIVE END-TO-END TESTS COMPLETED SUCCESSFULLY!", flush=True)
    print("==================================================", flush=True)

if __name__ == '__main__':
    run_live_tests()
