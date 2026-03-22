def run(game_id: str, agent_name: str = "Xoul에이전트", persona: str = "분석적이고 논리적인 성격."):
    """
    game_id: 참가할 게임 ID
    agent_name: 에이전트 이름 (default: Xoul에이전트)
    persona: 에이전트 성격 (default: 분석적이고 논리적인 성격.)
    """
    """
    🎭 AI Mafia Arena Agent — 워크플로우 실행용 독립 스크립트
    # arena-loop

    워크플로우의 code 스텝에서 run_python_code(timeout=600)으로 실행.
    - Arena 서버 API 폴링
    - Ollama LLM으로 자율 발언/투표/밤행동
    - 게임 종료 시 결과 반환
    """
    import urllib.request
    import json
    import time
    import os
    import sys

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 설정
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # VM에서 실행 시 AWS 아레나 서버 사용 (로컬 fallback)
    ARENA_URL = os.environ.get("ARENA_URL", "http://15.165.31.212:8081")
    HOST = "10.0.2.2" if os.path.exists("/root/xoul") else "localhost"
    OLLAMA_URL = f"http://{HOST}:11434"

    # config.json 경로 후보
    CONFIG_PATHS = [
        os.environ.get("XOUL_CONFIG", ""),
        os.path.join(os.path.dirname(__file__), "..", "config.json"),
        "/root/xoul/config.json",
    ]

    def _load_llm_model():
        """config.json에서 LLM 모델명 로드 (없으면 오류)"""
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

    # JWT 생성 — config.json에서 시크릿 읽기
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

    AGENT_NAME = agent_name or os.environ.get("ARENA_AGENT_NAME", "Xoul에이전트")
    PERSONA = persona or os.environ.get("ARENA_PERSONA", "분석적이고 논리적인 성격. 증거 기반으로 판단.")

    # config에서 언어 설정 로드
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
    def _clean_llm_output(text):
        """LLM 응답 기본 정리 (앞뒤 공백, 과도한 줄바꿈 제거)"""
        if not text:
            return ""
        import re
        # 여러 줄이면 첫 번째 비어있지 않은 줄들을 이어붙이기
        lines = [l.strip() for l in text.strip().split("\n") if l.strip()]
        result = " ".join(lines)
        # 200자 제한
        return result[:200]


    def call_llm(messages, max_tokens=8192):
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
                print(f"   [LLM] content({len(content)}): {content[:60]}...")
                if reasoning:
                    print(f"   [LLM] reasoning({len(reasoning)}): {reasoning[:60]}...")
                if not content and reasoning:
                    lines = [l.strip() for l in reasoning.split("\n") if l.strip()]
                    content = lines[-1] if lines else ""
                result = _clean_llm_output(content)
                print(f"   [LLM] final: {result[:60]}...")
                return result
        except Exception as e:
            print(f"   [LLM] ERROR: {e}")
            return f"(LLM 오류: {e})"


    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 이름 매핑
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    _name_map = {}  # P1 -> "Xoul에이전트" 등

    def _pid_to_name(pid):
        return _name_map.get(pid, pid)

    def _names_list(pids):
        return ', '.join(_pid_to_name(p) for p in pids)

    def _build_name_map(state):
        """state에서 player_id→이름 매핑 구축"""
        for p in state.get("players", []):
            _name_map[p["player_id"]] = p.get("agent_name", p["player_id"])


    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 게임 설명 가져오기
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    _game_description = ""

    def fetch_game_description():
        """서버에서 게임 규칙 설명을 가져와 시스템 프롬프트에 사용"""
        nonlocal _game_description
        try:
            desc = api_get("/arena/docs")
            if isinstance(desc, dict) and not desc.get("error"):
                _game_description = desc.get("description", "")
        except:
            pass


    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 프롬프트 빌더
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def _strip_prefix(text):
        """LLM 응답에서 '발언:', '대사:', 이름 접두사 등 제거"""
        import re
        # '발언:', '대사:' 제거
        text = re.sub(r'^(발언:|\s*대사:\s*)', '', text).strip()
        # '이름: ' 접두사 제거 (예: 'Xoul에이전트: 내용')
        text = re.sub(r'^[\w가-힣]+:\s*', '', text).strip()
        # 'I'm sorry' 등 영어 거부 응답 처리
        if text.lower().startswith("i'm sorry") or text.lower().startswith("i cannot"):
            return ""
        return text


    def build_speak_prompt(state):
        role = state.get("my_role", "citizen")
        role_kr = {"citizen": "시민", "mafia": "마피아", "police": "경찰"}.get(role, role)
        chats = state.get("chat_log", [])
        speaks = [c for c in chats if c.get("type") == "speak"]
        chat_str = "\n".join(f"  {_pid_to_name(c['player'])}: {c['data'].get('message','')}" for c in speaks[-10:])

        system = f"""당신은 '{AGENT_NAME}'. {PERSONA}
    당신은 [{role_kr}]. {"마피아를 찾아내세요." if role != "mafia" else "정체를 숨기고 시민인 척 하세요."}

    ❗규칙:
    - {LANG_INSTRUCTION}
    - 이름표 없이 대사만 출력. '이름:' 형식 금지.
    - 1~2문장으로 짧게."""
        if _game_description:
            system = _game_description + "\n\n" + system
        # 첫 발언 여부
        my_speaks = [c for c in speaks if c.get("player") == state.get("_my_pid")]
        rnd = state.get('round', 1)

        if len(my_speaks) == 0 and rnd == 1:
            hint = "첫 라운드입니다. 캐릭터로서 간단한 자기소개를 해주세요."
        elif rnd == 1:
            hint = "다른 사람들의 자기소개를 듣고 느낀 점이나 의심을 말하세요."
        else:
            hint = "대화를 분석하고 의심되는 사람을 언급하세요."

        user = f"[R{rnd} 토론] 생존자: {_names_list(state.get('alive',[]))}\n\n대화:\n{chat_str}\n\n{hint}\n1~2문장으로 캐릭터 대사만 출력하세요."
        return [{"role": "system", "content": system}, {"role": "user", "content": user}]

    def build_vote_prompt(state):
        chats = state.get("chat_log", [])
        speaks = [c for c in chats if c.get("type") == "speak"]
        chat_str = "\n".join(f"  {_pid_to_name(c['player'])}: {c['data'].get('message','')}" for c in speaks[-14:])
        alive_names = [_pid_to_name(p) for p in state.get("alive", []) if p != state.get("_my_pid")]

        user = f"투표 시간. 생존자: {_names_list(state.get('alive',[]))}\n대화:\n{chat_str}\n\n처형할 사람의 이름만 출력:"
        return [{"role": "system", "content": f"당신은 '{AGENT_NAME}'. {PERSONA}"}, {"role": "user", "content": user}]

    def build_night_prompt(state):
        role = state.get("my_role", "citizen")
        if role == "mafia":
            action_desc = "제거할"
        else:
            action_desc = "조사할"
        alive_names = [_pid_to_name(p) for p in state.get("alive", []) if p != state.get("_my_pid")]
        user = f"밤 시간입니다. 마피아 게임의 밤 페이즈입니다. {action_desc} 대상을 한 명 선택하세요.\n생존자: {', '.join(alive_names)}\n\n이름만 출력:"
        return [{"role": "system", "content": f"마피아 게임의 [{{'mafia':'마피아','police':'경찰'}}.get(role, role)] 역할. 대상 이름만 출력하세요."}, {"role": "user", "content": user}]

    def extract_pid(text, valid_pids):
        """응답에서 player ID 추출 (이름 또는 PID 매칭)"""
        import re
        # PID 직접 매칭
        for pid in re.findall(r'P\d+', text):
            if pid in valid_pids:
                return pid
        # 이름으로 매칭
        for pid in valid_pids:
            name = _pid_to_name(pid)
            if name in text:
                return pid
        return valid_pids[0] if valid_pids else None


    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 메인 게임 루프
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def main():
        user_id = f"arena-agent-{int(time.time()) % 10000}"
        token = make_token(user_id)

        # 파라미터 → 환경변수 순서로 game_id 결정
        target_game_id = game_id or os.environ.get("ARENA_GAME_ID", "")

        # 1. 대기 중인 마피아 게임 찾기 (또는 파라미터/환경변수에서 지정)
        if target_game_id:
            print(f"✅ 대상 게임 ID: {target_game_id}")
        else:
            print("🔍 대기 중인 마피아 게임 찾는 중...")
            while not target_game_id:  # arena-loop
                games = api_get("/arena/games?status=waiting&game_type=mafia")
                if games.get("games"):
                    target_game_id = games["games"][0]["id"]
                    countdown = games["games"][0].get("starts_in_seconds")
                    real_count = games["games"][0].get("real_player_count", 0)
                    if countdown is not None:
                        print(f"✅ 대기 게임 발견: {target_game_id} (참가자 {real_count}명, {countdown}초 후 시작)")
                    else:
                        print(f"✅ 대기 게임 발견: {target_game_id} (참가자 대기 중)")
                else:
                    time.sleep(3)
                    continue

        if not target_game_id:
            print("❌ 게임 참가 실패 (타겟 게임 ID 없음)")
            return

        # 2. 참가
        join = api_post(f"/arena/games/{target_game_id}/join",
                        {"agent_name": AGENT_NAME, "persona_prompt": PERSONA}, token)
        my_pid = join.get("player_id")
        if not my_pid:
            print(f"❌ 참가 실패: {join}")
            return
        print(f"✅ 참가 완료: {my_pid} ({AGENT_NAME})")

        # 3. 게임 시작 대기
        print("⏳ 게임 시작 대기...")
        while True:  # arena-loop
            state = api_get(f"/arena/games/{target_game_id}/state?player_id={my_pid}", token)
            if state.get("status") == "playing":
                print("✅ 게임 시작!")
                break
            if state.get("status") == "finished":
                print("❌ 게임이 이미 끝남")
                return
            time.sleep(3)

        # 이름 매핑 구축 + 게임 설명 가져오기
        _build_name_map(state)
        fetch_game_description()
        role = state.get("my_role", "?")
        role_kr = {"citizen": "시민", "mafia": "마피아", "police": "경찰"}.get(role, role)
        print(f"   참가자: {_names_list(state.get('alive', []))}")
        print(f"   🎭 내 역할: [{role_kr}]")

        # 4. 게임 루프
        last_action = None
        while True:  # arena-loop
            state = api_get(f"/arena/games/{target_game_id}/state?player_id={my_pid}", token)
            if state.get("error"):
                time.sleep(2)
                continue

            status = state.get("status")
            if status == "finished":
                winner = state.get("winner", "?")
                print(f"\n🏁 게임 종료! 승자: {winner}")
                print(f"   내 역할: {state.get('my_role')}")
                return

            action = state.get("pending_action")
            state["_my_pid"] = my_pid

            if action == "speak":
                # 이중 체크: current_speaker가 나인지 확인
                current_speaker = state.get("current_speaker")
                if current_speaker and current_speaker != my_pid:
                    time.sleep(1)
                    continue


                prompt = build_speak_prompt(state)
                response = call_llm(prompt)
                response = _strip_prefix(response)  # "발언:" 접두사 제거
                if not response or response.startswith("(LLM"):
                    print(f"   ⚠️ LLM 실패: {response[:80] if response else 'empty'}")
                    import random
                    response = random.choice(["아직 확실한 근거는 없지만, 좀 더 지켜봐야 할 것 같습니다.", "의심되는 사람이 있긴 한데, 좀 더 들어보겠습니다.", "누군가 말을 돌리고 있는 것 같아요."])
                if len(response) > 200:
                    response = response[:200]
                result = api_post(f"/arena/games/{target_game_id}/speak",
                                {"player_id": my_pid, "message": response}, token)
                if result.get("ok"):
                    print(f"💬 R{state.get('round')}: {response[:60]}")
                else:
                    time.sleep(2)  # speak 실패 시 잠깐 대기

            elif action == "vote" and last_action != f"vote-{state.get('round')}":
                prompt = build_vote_prompt(state)
                response = call_llm(prompt, max_tokens=8192)
                valid = [p for p in state.get("alive", []) if p != my_pid]
                target = extract_pid(response, valid)
                if target:
                    api_post(f"/arena/games/{target_game_id}/vote",
                            {"player_id": my_pid, "target": target}, token)
                    print(f"🗳️  R{state.get('round')}: → {_pid_to_name(target)}")
                last_action = f"vote-{state.get('round')}"

            elif action == "night_action" and last_action != f"night-{state.get('round')}":
                prompt = build_night_prompt(state)
                response = call_llm(prompt, max_tokens=8192)
                valid = [p for p in state.get("alive", []) if p != my_pid]
                target = extract_pid(response, valid)
                act = "kill" if state.get("my_role") == "mafia" else "investigate"
                if target:
                    api_post(f"/arena/games/{target_game_id}/night",
                            {"player_id": my_pid, "action": act, "target": target}, token)
                    print(f"🌙 R{state.get('round')}: {act} → {target}")
                last_action = f"night-{state.get('round')}"

            time.sleep(2)


    if __name__ == "__main__":
        main()
