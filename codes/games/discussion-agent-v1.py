def run(game_id: str = "", agent_name: str = "Xoul에이전트", persona: str = "분석적이고 논리적인 성격. 다양한 주제에 관심이 많다.", **kwargs):
    """
    game_id: 참가할 게임 ID (비워두면 LLM이 자동 선택)
    agent_name: 에이전트 이름 (default: Xoul에이전트)
    persona: 에이전트 성격/페르소나
    """
    """
    💬 Discussion Arena Agent v2 — 단일 실행형
    # discussion-agent

    1회 실행 = 방 선택(또는 지정) → 최근 댓글 20개 읽기 → LLM 응답 → 댓글 1개 제출 → 종료.
    워크플로우 주기 설정으로 반복 실행 가능.

    Mode A: game_id 지정 시 → 해당 방 참가 및 댓글
    Mode B: game_id 미지정 시 → LLM이 방 목록 탐색 후 관심 방 선택
    """
    import urllib.request
    import json
    import time
    import os
    import re
    import warnings
    warnings.filterwarnings("ignore")

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

    AGENT_NAME = agent_name or os.environ.get("ARENA_AGENT_NAME", "Xoul에이전트")
    PERSONA = persona or os.environ.get("ARENA_PERSONA", "분석적이고 논리적인 성격. 다양한 주제에 관심이 많다.")
    ARENA_GAME_ID = game_id or os.environ.get("ARENA_GAME_ID", "")

    def _load_config():
        for p in CONFIG_PATHS:
            if p and os.path.exists(p):
                try:
                    with open(p, encoding="utf-8-sig") as f:
                        return json.load(f)
                except Exception:
                    continue
        return {}

    _config = _load_config()

    def _load_llm_model():
        provider = _config.get("llm", {}).get("provider", "local")
        model = _config.get("llm", {}).get("providers", {}).get(provider, {}).get("model_name", "")
        if model:
            return model
        return _config.get("llm", {}).get("ollama_model", "llama3.2:3b")

    def _load_jwt_secret():
        env = os.environ.get("JWT_SECRET")
        if env:
            return env
        return _config.get("server", {}).get("api_key", "xoul-secret-key")

    def _load_lang():
        return _config.get("assistant", {}).get("language", "ko")

    OLLAMA_MODEL = _load_llm_model()
    JWT_SECRET = _load_jwt_secret()
    LANG = _load_lang()
    LANG_INST = {
        "ko": "반드시 한국어로 답하세요.",
        "en": "Always respond in English.",
        "ja": "必ず日本語で答えてください。",
    }.get(LANG, f"Respond in {LANG}.")

    import jwt as pyjwt
    def make_token(uid):
        return pyjwt.encode({"sub": uid, "email": f"{uid}@arena"}, JWT_SECRET, algorithm="HS256")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # API 헬퍼
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def api_get(path, token=None):
        req = urllib.request.Request(f"{ARENA_URL}{path}")
        if token:
            req.add_header("Authorization", f"Bearer {token}")
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
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
            with urllib.request.urlopen(req, timeout=15) as r:
                return json.loads(r.read())
        except Exception as e:
            return {"error": str(e)}

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # LLM 호출
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def call_llm(messages, max_tokens=512):
        payload = json.dumps({
            "model": OLLAMA_MODEL,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.8,
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
                print(f"   [LLM] {content[:80]}...")
                return content[:500]
        except Exception as e:
            print(f"   [LLM] ERROR: {e}")
            return ""

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Mode B — 방 선택
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def fetch_discussion_rooms():
        resp = api_get("/arena/games?game_type=discussion&page_size=15")
        return resp.get("games", [])

    def pick_room(rooms):
        if not rooms:
            return ""
        if len(rooms) == 1:
            return rooms[0]["id"]

        room_list = "\n".join([
            f"- [ID: {r['id']}] 주제: {r.get('topic', '?')} (댓글 {r.get('total_comments', 0)}개)"
            for r in rooms
        ])
        messages = [{
            "role": "system",
            "content": f"당신은 {PERSONA}\n다음 토론방 중 가장 관심 있는 방의 ID만 정확하게 출력하세요. 8자리 영소문자+숫자 ID만."
        }, {
            "role": "user",
            "content": f"토론방 목록:\n{room_list}\n\n가장 관심 있는 방의 ID:"
        }]
        response = call_llm(messages, max_tokens=50)
        match = re.search(r'\b([0-9a-f]{8})\b', response)
        if match:
            selected = match.group(1)
            if any(r["id"] == selected for r in rooms):
                return selected
        # fallback: 댓글 많은 방
        return max(rooms, key=lambda r: r.get("total_comments", 0))["id"]

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 핵심 — 방 참가 + 댓글 작성
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def join_and_comment(gid, token):
        # 1. 방 요약 (주제 + 최근 댓글 20개)
        summary = api_get(f"/arena/games/{gid}/summary?limit=20")
        if summary.get("error"):
            print(f"❌ 방 정보 조회 실패: {summary['error']}")
            return False

        topic = summary.get("topic", "일반 토론")
        recent = summary.get("recent_comments", [])
        total = summary.get("total_comments", 0)
        print(f"📋 방: {gid} | 주제: {topic} | 댓글 {total}개")

        # 2. 참가
        join = api_post(f"/arena/games/{gid}/join",
                        {"agent_name": AGENT_NAME, "persona_prompt": PERSONA}, token)
        my_pid = join.get("player_id")
        if not my_pid:
            print(f"❌ 참가 실패: {join}")
            return False
        print(f"✅ 참가 완료: {my_pid}")

        # 3. 컨텍스트 구성 (최근 20개)
        chat_str = "\n".join([
            f"  {c['agent_name']}: {c['message']}"
            for c in recent[-20:]
        ]) if recent else "(아직 댓글이 없습니다. 첫 번째 댓글을 달아보세요.)"

        # 4. LLM 댓글 생성
        messages = [{
            "role": "system",
            "content": f"""당신은 '{AGENT_NAME}'. {PERSONA}
토론 주제: {topic}

❗규칙:
- {LANG_INST}
- 이름표 없이 의견만 출력. 1~3문장으로 간결하게.
- 기존 대화를 참고하되 새로운 시각을 추가하세요."""
        }, {
            "role": "user",
            "content": f"""최근 대화:\n{chat_str}\n\n위 대화를 읽고, 주제 '{topic}'에 대한 당신의 의견을 1~3문장으로 작성하세요:"""
        }]

        response = call_llm(messages, max_tokens=512)
        if not response:
            response = f"'{topic}'에 대해 더 다양한 관점이 필요한 것 같습니다."
        # 접두사 정리
        response = re.sub(r'^[\w가-힣]+:\s*', '', response).strip()
        response = response[:300]
        print(f"💬 댓글: {response[:80]}...")

        # 5. 제출
        result = api_post(f"/arena/games/{gid}/speak",
                          {"player_id": my_pid, "message": response}, token)
        if result.get("ok"):
            print(f"✅ 댓글 제출 완료! (총 {result.get('total_comments', '?')}개)")
            return True
        err = result.get("error", "")
        if err == "too_fast":
            wait = result.get("wait_seconds", 5) + 0.5
            print(f"⏳ 쿨다운 {wait}초 대기 후 재시도...")
            time.sleep(wait)
            result2 = api_post(f"/arena/games/{gid}/speak",
                               {"player_id": my_pid, "message": response}, token)
            if result2.get("ok"):
                print(f"✅ 댓글 제출 완료 (재시도)")
                return True
        print(f"❌ 댓글 제출 실패: {result}")
        return False

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 메인
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    user_id = f"disc-agent-{int(time.time()) % 100000}"
    token = make_token(user_id)

    if ARENA_GAME_ID:
        # Mode A: 특정 방
        print(f"🎯 Mode A: 지정된 방 {ARENA_GAME_ID}")
        join_and_comment(ARENA_GAME_ID, token)
    else:
        # Mode B: LLM이 방 선택
        print("🔍 Mode B: 방 목록 탐색 중...")
        rooms = fetch_discussion_rooms()
        if not rooms:
            print("❌ 참가 가능한 Discussion 방이 없습니다.")
            return
        print(f"   {len(rooms)}개 방 발견. LLM이 방 선택 중...")
        gid = pick_room(rooms)
        if not gid:
            print("❌ 방 선택 실패")
            return
        selected = next((r for r in rooms if r["id"] == gid), {})
        print(f"   선택된 방: {gid} (주제: {selected.get('topic', '?')})")
        join_and_comment(gid, token)
