def run(game_id: str, agent_name: str = "Xoul에이전트", persona: str = "자유로운 토론 참가자"):
    """
    game_id: 참가할 게임 ID
    agent_name: 에이전트 이름 (default: Xoul에이전트)
    persona: 에이전트 성격 (default: 자유로운 토론 참가자)
    """
    """
    💬 AI Discussion Arena Agent — 토론 게임 자동 참여 에이전트
    # arena-loop

    Discussion 게임에 참가하여 주제에 대해 자율적으로 발언.
    - Arena 서버 API 폴링
    - Ollama LLM으로 자율 토론 발언
    - 쿨다운/발언 제한 자동 처리
    - 주제 변경 감지 & 게임 종료 시 결과 반환
    """
    import urllib.request
    import json
    import time
    import os

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 설정
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ARENA_URL = os.environ.get("ARENA_URL", "http://15.165.31.212:8081")
    HOST = "10.0.2.2" if os.path.exists("/root/xoul") else "localhost"
    OLLAMA_URL = f"http://{HOST}:11434"

    CONFIG_PATHS = [
        os.environ.get("XOUL_CONFIG", ""),
        os.path.join(os.path.dirname(__file__), "..", "config.json"),
        "/root/xoul/config.json",
    ]

    def _load_llm_model():
        for p in CONFIG_PATHS:
            if p and os.path.exists(p):
                try:
                    with open(p, encoding="utf-8-sig") as f:
                        c = json.load(f)
                    provider = c.get("llm", {}).get("provider", "local")
                    model = c.get("llm", {}).get("providers", {}).get(provider, {}).get("model_name", "")
                    if model:
                        return model
                    model = c.get("llm", {}).get("ollama_model", "")
                    if model:
                        return model
                except Exception:
                    continue
        raise RuntimeError("config.json에 LLM 모델이 설정되지 않았습니다")

    OLLAMA_MODEL = _load_llm_model()

    def _load_jwt_secret():
        for p in CONFIG_PATHS:
            if p and os.path.exists(p):
                try:
                    with open(p, encoding="utf-8-sig") as f:
                        c = json.load(f)
                    return c.get("server", {}).get("api_key", "xoul-secret-key")
                except Exception:
                    pass
        return "xoul-secret-key"

    JWT_SECRET = _load_jwt_secret()

    import jwt as pyjwt
    import warnings
    warnings.filterwarnings("ignore", message=".*key size.*")

    def make_token(user_id):
        return pyjwt.encode({"sub": user_id, "email": f"{user_id}@arena"}, JWT_SECRET, algorithm="HS256")

    AGENT_NAME = agent_name
    PERSONA = persona

    # 언어 설정
    def _load_lang():
        for p in CONFIG_PATHS:
            if p and os.path.exists(p):
                try:
                    with open(p, encoding="utf-8-sig") as f:
                        c = json.load(f)
                    return c.get("assistant", {}).get("language", "ko")
                except Exception:
                    pass
        return "ko"

    LANG = _load_lang()
    LANG_INSTRUCTION = {
        "ko": "반드시 한국어로 답하세요.",
        "en": "Always respond in English.",
        "ja": "必ず日本語で答えてください。",
    }.get(LANG, f"Respond in {LANG}.")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # API 호출
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def api_get(path, token=None):
        req = urllib.request.Request(f"{ARENA_URL}{path}")
        if token:
            req.add_header("Authorization", f"Bearer {token}")
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                return json.loads(r.read())
        except Exception as e:
            return {"error": str(e)}

    def api_post(path, data, token=None):
        body = json.dumps(data).encode()
        req = urllib.request.Request(f"{ARENA_URL}{path}", data=body,
                                     headers={"Content-Type": "application/json"})
        if token:
            req.add_header("Authorization", f"Bearer {token}")
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                return json.loads(r.read())
        except Exception as e:
            return {"error": str(e)}

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # LLM 호출
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def call_llm(messages, max_tokens=8192):
        payload = json.dumps({
            "model": OLLAMA_MODEL,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.9,
            "think": True,
        }).encode()
        req = urllib.request.Request(
            f"{OLLAMA_URL}/v1/chat/completions",
            data=payload,
            headers={"Content-Type": "application/json", "Authorization": "Bearer none"}
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                d = json.loads(resp.read())
                msg = d["choices"][0]["message"]
                content = (msg.get("content") or "").strip()
                reasoning = (msg.get("reasoning") or "").strip()
                if not content and reasoning:
                    lines = [l.strip() for l in reasoning.split("\n") if l.strip()]
                    content = lines[-1] if lines else ""
                # 정리: 200자 제한
                lines = [l.strip() for l in content.split("\n") if l.strip()]
                result = " ".join(lines)[:200]
                print(f"   [LLM] {result[:80]}...")
                return result
        except Exception as e:
            print(f"   [LLM] ERROR: {e}")
            return ""

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 프롬프트 빌더 (토론용)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    _name_map = {}

    def _build_name_map(state):
        for p in state.get("players", []):
            _name_map[p["player_id"]] = p.get("agent_name", p["player_id"])

    def _pid_to_name(pid):
        return _name_map.get(pid, pid)

    def build_speak_prompt(state, topic):
        chats = state.get("chat_log", [])
        speaks = [c for c in chats if c.get("type") == "speak"]
        # 최근 10개만
        recent = speaks[-10:]
        chat_str = "\n".join(
            f"  {_pid_to_name(c['player'])}: {c['data'].get('message','')}"
            for c in recent
        )

        my_speaks = [c for c in speaks if c.get("player") == state.get("_my_pid")]

        system = f"""당신은 토론 참가자 '{AGENT_NAME}'. {PERSONA}
현재 주제: "{topic}"

❗규칙:
- {LANG_INSTRUCTION}
- 이름표 없이 발언만 출력. '이름:' 형식 금지.
- 주제에 집중하되, 독창적이고 깊이 있는 관점을 제시.
- 1~3문장으로."""

        if not my_speaks:
            hint = "이 주제에 대한 첫 발언입니다. 주제에 대한 당신의 관점을 밝혀주세요."
        elif len(recent) > 0:
            last_speaker = _pid_to_name(recent[-1].get("player", ""))
            hint = f"직전 발언자({last_speaker})의 의견을 참고하여, 동의/반박/확장하세요."
        else:
            hint = "주제에 대한 발언을 이어가세요."

        user = f"""현재 주제: "{topic}"

대화 기록:
{chat_str if chat_str else "(아직 발언 없음)"}

{hint}
1~3문장으로 발언만 출력하세요."""

        return [{"role": "system", "content": system}, {"role": "user", "content": user}]

    # fallback 응답
    FALLBACK_RESPONSES = [
        "흥미로운 관점이네요. 저는 조금 다르게 생각합니다.",
        "그 부분에 대해서는 더 깊이 생각해볼 필요가 있을 것 같습니다.",
        "좋은 지적입니다. 거기에 덧붙이자면...",
        "이 주제는 정말 다양한 시각에서 볼 수 있는 것 같아요.",
        "동의합니다. 다만 한 가지 고려할 점이 있습니다.",
    ]

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 메인 게임 루프
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def main():
        import random
        user_id = f"disc-agent-{int(time.time()) % 10000}"
        token = make_token(user_id)

        print(f"💬 Discussion Agent: {AGENT_NAME}")
        print(f"   게임 ID: {game_id}")

        # 1. 참가
        join = api_post(f"/arena/games/{game_id}/join",
                        {"agent_name": AGENT_NAME, "persona_prompt": PERSONA}, token)
        my_pid = join.get("player_id")
        if not my_pid:
            print(f"❌ 참가 실패: {join}")
            return
        print(f"✅ 참가 완료: {my_pid} ({AGENT_NAME})")

        # 2. 게임 시작 대기 (Discussion은 즉시 시작하므로 짧게 대기)
        for _ in range(10):
            state = api_get(f"/arena/games/{game_id}/state?player_id={my_pid}", token)
            if state.get("status") == "playing":
                break
            if state.get("status") == "finished":
                print("❌ 게임이 이미 끝남")
                return
            time.sleep(1)

        _build_name_map(state)
        current_topic = state.get("current_topic", "")
        topic_idx = state.get("topic_index", 0)
        total = state.get("total_topics", 0)
        print(f"📢 주제 [{topic_idx+1}/{total}]: {current_topic}")

        # 3. 토론 루프
        last_topic_idx = topic_idx
        speak_failures = 0

        while True:  # arena-loop
            state = api_get(f"/arena/games/{game_id}/state?player_id={my_pid}", token)
            if state.get("error"):
                time.sleep(3)
                continue

            status = state.get("status")
            if status == "finished":
                print(f"\n🏁 토론 종료! 총 {state.get('total_topics', 0)}개 주제 토론 완료")
                return

            state["_my_pid"] = my_pid
            action = state.get("pending_action")

            # 주제 변경 감지
            new_topic_idx = state.get("topic_index", 0)
            if new_topic_idx != last_topic_idx:
                current_topic = state.get("current_topic", "")
                total = state.get("total_topics", 0)
                print(f"\n📢 주제 [{new_topic_idx+1}/{total}]: {current_topic}")
                last_topic_idx = new_topic_idx
                speak_failures = 0

            if action == "speak":
                # 자연스러운 딜레이 (2~6초)
                time.sleep(random.uniform(2, 6))

                topic = state.get("current_topic", current_topic)
                prompt = build_speak_prompt(state, topic)
                response = call_llm(prompt)

                # LLM 실패 시 fallback
                if not response:
                    response = random.choice(FALLBACK_RESPONSES)

                # 접두사 정리
                import re
                response = re.sub(r'^[\w가-힣]+:\s*', '', response).strip()
                if len(response) > 200:
                    response = response[:200]

                result = api_post(f"/arena/games/{game_id}/speak",
                                {"player_id": my_pid, "message": response}, token)
                if result.get("ok"):
                    remaining = result.get("remaining", "?")
                    print(f"💬 [{topic_idx+1}] {response[:70]}.. (남은 발언: {remaining})")
                    speak_failures = 0
                else:
                    speak_failures += 1
                    err = result.get("error", "")
                    if err == "too_fast":
                        wait = result.get("wait_seconds", 3)
                        time.sleep(wait)
                    elif err == "max_speaks_reached":
                        print(f"   ⚠️ 이 주제 발언 상한 도달")
                        time.sleep(10)
                    else:
                        time.sleep(3)

            elif action == "cooldown":
                time.sleep(3)

            elif action == "wait":
                time.sleep(5)

            elif action == "game_over":
                print(f"\n🏁 토론 종료!")
                return

            else:
                time.sleep(3)

    main()
