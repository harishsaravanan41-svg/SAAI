import os
import json
import threading
from typing import Dict, Any, List, Optional, AsyncGenerator
import asyncio
from sqlalchemy.orm import Session
from backend.database.models import User
from backend.tool_executor import execute_tool_call
from ai_model.prompt_templates import build_system_prompt
from ai_model.response_validator import validate_and_sanitize_response


class QwenAssistant:
    """
    Ultra-Fast Local Qwen 2.5 1.5B Assistant.
    
    Optimizations:
    - Direct PyTorch multi-threaded CPU/CUDA inference mode
    - Single-pass dynamic database context injection
    - Immediate TextIteratorStreamer token streaming
    - 100% local weights from `ai_model/Qwen2.5-1.5B-Instruct`
    """

    def __init__(self):
        self.local_model_dir = os.path.join(os.path.dirname(__file__), "Qwen2.5-1.5B-Instruct")
        self._model = None
        self._tokenizer = None
        self._device = None
        self._lock = threading.Lock()

    def _load_local_model(self):
        """Loads local Qwen 2.5 1.5B Instruct model once into memory."""
        if self._model is not None:
            return

        with self._lock:
            if self._model is not None:
                return

            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer

            # Maximize PyTorch CPU performance
            cpu_cores = os.cpu_count() or 4
            try:
                torch.set_num_threads(cpu_cores)
            except Exception:
                pass

            if not os.path.exists(self.local_model_dir):
                raise RuntimeError(f"Local model directory not found at: {self.local_model_dir}")

            device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"🔄 Pre-warming local Qwen2.5-1.5B-Instruct model on {device.upper()} (Threads: {cpu_cores})...")

            self._tokenizer = AutoTokenizer.from_pretrained(
                self.local_model_dir,
                trust_remote_code=True
            )
            self._model = AutoModelForCausalLM.from_pretrained(
                self.local_model_dir,
                dtype=torch.float16 if device == "cuda" else torch.float32,
                device_map=device,
                trust_remote_code=True
            )
            self._device = device
            print(f"✅ Local Qwen2.5-1.5B-Instruct ready and active on {device.upper()}!")

    def _get_dynamic_db_context(self, user_msg: str, db: Session, current_user: User) -> tuple[Optional[str], Optional[str], Optional[Dict[str, Any]]]:
        """
        Dynamically fetches verified database records if relevant to query,
        allowing single-pass instant streaming without double-generation latency.
        """
        msg = user_msg.lower().strip()

        # 1. Personal Academic Intent
        if any(w in msg for w in ["mark", "marks", "result", "results", "cgpa", "percentage", "score", "scores", "grade", "grades", "rank", "ranking", "how am i doing", "how did i do", "my performance", "weak", "fail", "pass"]):
            res = execute_tool_call("tool_get_my_result", {}, db, current_user)
            if res.get("status") == "SUCCESS":
                return "tool_get_my_result", f"\n[Verified Student Examination Record from MySQL]:\n{json.dumps(res['data'], indent=2)}\n", res
            return "tool_get_my_result", "\n[Database Status: No examination records found for this student registration number.]\n", res

        # 2. Staff / Faculty Intent
        elif any(w in msg for w in ["hod", "head", "faculty", "staff", "professor", "professors", "teacher", "teachers", "who teaches", "dean", "dr.", "mr.", "mrs."]):
            dept = "Data Science" if "data science" in msg else "Artificial Intelligence" if "ai" in msg else "Computer Science" if "cs" in msg or "computer" in msg else None
            role = "Head" if any(r in msg for r in ["hod", "head", "chair"]) else None
            args = {"department_name": dept, "role": role}
            res = execute_tool_call("tool_get_staff", args, db, current_user)
            if res.get("status") == "SUCCESS":
                return "tool_get_staff", f"\n[Verified Staff Information from MySQL]:\n{json.dumps(res['data'], indent=2)}\n", res
            return "tool_get_staff", None, res

        # 3. Events Intent
        elif any(w in msg for w in ["event", "events", "symposium", "celebration", "farewell", "synapse", "novazen", "cleanup", "fest", "workshop"]):
            dept = "Data Science" if "synapse" in msg or "data science" in msg else "Artificial Intelligence" if "novazen" in msg or "ai" in msg else None
            club = "Rotaract" if "rotaract" in msg else "Exnora" if "exnora" in msg else None
            args = {"department_name": dept, "club_name": club}
            res = execute_tool_call("tool_get_events", args, db, current_user)
            if res.get("status") == "SUCCESS":
                return "tool_get_events", f"\n[Verified Events Schedule from MySQL]:\n{json.dumps(res['data'], indent=2)}\n", res
            return "tool_get_events", None, res

        # 4. Clubs Intent
        elif any(w in msg for w in ["club", "clubs", "rotaract", "exnora", "extension cell", "nss", "yrc", "leo"]):
            res = execute_tool_call("tool_get_clubs", {}, db, current_user)
            if res.get("status") == "SUCCESS":
                return "tool_get_clubs", f"\n[Verified Clubs from MySQL]:\n{json.dumps(res['data'], indent=2)}\n", res
            return "tool_get_clubs", None, res

        # 5. Departments Intent
        elif any(w in msg for w in ["department", "departments", "courses", "branches", "what courses", "dept"]):
            res = execute_tool_call("tool_get_departments", {}, db, current_user)
            if res.get("status") == "SUCCESS":
                return "tool_get_departments", f"\n[Verified Departments from MySQL]:\n{json.dumps(res['data'], indent=2)}\n", res
            return "tool_get_departments", None, res

        return None, None, None

    async def chat_stream(
        self,
        user_message: str,
        chat_history: List[Dict[str, str]],
        db: Session,
        current_user: User
    ) -> AsyncGenerator[str, None]:
        """
        Instantly streams generated response tokens in a single fast pass.
        """
        loop = asyncio.get_running_loop()
        system_prompt = build_system_prompt(current_user)

        # Ensure model is warm
        await loop.run_in_executor(None, self._load_local_model)

        import torch
        from transformers import TextIteratorStreamer

        # Fast dynamic DB context retrieval
        tool_name, db_context, tool_res = self._get_dynamic_db_context(user_message, db, current_user)

        messages = [{"role": "system", "content": system_prompt}]
        for h in chat_history[-4:]:
            messages.append({"role": h["role"], "content": h["content"]})

        user_content = user_message
        if db_context:
            user_content += f"\n\n{db_context}\nAnswer the student naturally using this verified information."

        messages.append({"role": "user", "content": user_content})

        text_prompt = self._tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = self._tokenizer(text_prompt, return_tensors="pt").to(self._device)

        # Initialize real-time streamer
        streamer = TextIteratorStreamer(self._tokenizer, skip_prompt=True, skip_special_tokens=True)
        gen_kwargs = dict(
            **inputs,
            streamer=streamer,
            max_new_tokens=220,
            do_sample=True,
            temperature=0.6,
            top_p=0.9,
            pad_token_id=self._tokenizer.eos_token_id
        )

        # Run inference in a lightweight background worker
        def _generate_worker():
            with torch.inference_mode():
                self._model.generate(**gen_kwargs)

        thread = threading.Thread(target=_generate_worker)
        thread.start()

        # Stream tokens immediately as they are generated
        for token in streamer:
            yield token

        thread.join()

    async def chat(
        self,
        user_message: str,
        chat_history: List[Dict[str, str]],
        db: Session,
        current_user: User
    ) -> Dict[str, Any]:
        """Non-streaming batch method for API contracts and tests."""
        tokens = []
        async for token in self.chat_stream(user_message, chat_history, db, current_user):
            tokens.append(token)

        full_text = "".join(tokens)
        sanitized = validate_and_sanitize_response(full_text, None, None, current_user)
        return {
            "response": sanitized,
            "tool_executed": None,
            "tool_arguments": None,
            "tool_status": None,
            "provider": "Local Qwen 2.5 1.5B (Safetensors)"
        }


qwen_orchestrator = QwenAssistant()
