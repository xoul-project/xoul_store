def run(game_id: str = "auto", agent_name: str = "Xoul에이전트", persona: str = "분석적이고 논리적인 성격. 다양한 주제에 관심이 많다.", create_chance: float = 0.15, rounds: int = 1, **kwargs):
    """
    game_id: 참가할 방 ID (default: auto = LLM이 자동 선택)
    agent_name: 에이전트 이름 (default: Xoul에이전트)
    persona: 에이전트 성격/페르소나
    create_chance: 새 방 자동 생성 확률 (0.0~1.0, default: 0.15 = 15%)
    rounds: 실행 횟수 (default: 1, 여러 번 반복 실행 가능)
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
    import random
    import warnings
    warnings.filterwarnings("ignore")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 설정
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ARENA_URL = os.environ.get("ARENA_URL", "https://www.xoulai.net:8081")
    HOST = "10.0.2.2" if os.path.exists("/root/xoul") else "localhost"
    OLLAMA_URL = f"http://{HOST}:11434"

    CONFIG_PATHS = [
        os.environ.get("XOUL_CONFIG", ""),
        os.path.join(os.path.dirname(__file__), "..", "config.json"),
        "/root/xoul/config.json",
    ]

    AGENT_NAME = agent_name or os.environ.get("ARENA_AGENT_NAME", "Xoul에이전트")
    PERSONA = persona or os.environ.get("ARENA_PERSONA", "분석적이고 논리적인 성격. 다양한 주제에 관심이 많다.")
    _gid = game_id if game_id not in ("", "auto", "-1") else ""
    ARENA_GAME_ID = _gid or os.environ.get("ARENA_GAME_ID", "")
    ROOM_CREATE_CHANCE = max(0.0, min(1.0, float(create_chance)))

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
        # auth_config.json (웹서비스/Arena 서버와 동일한 JWT secret)
        auth_paths = [
            os.path.join(os.path.dirname(__file__), "..", "web_service", "backend", "auth_config.json"),
            "/app/auth_config.json",
            "/root/xoul/web_service/backend/auth_config.json",
        ]
        for ap in auth_paths:
            try:
                if os.path.exists(ap):
                    with open(ap, encoding="utf-8") as f:
                        secret = json.load(f).get("jwt_secret")
                        if secret:
                            return secret
            except Exception:
                pass
        secret = _config.get("server", {}).get("api_key")
        if secret and secret != "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA":
            return secret
        return "xoul-secret-key"

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
                # 다양한 모델의 reasoning/thinking 태그 제거
                for tag in ("think", "thinking", "reasoning", "thought", "reflection"):
                    content = re.sub(rf'<{tag}>.*?</{tag}>', '', content, flags=re.DOTALL).strip()
                    content = re.sub(rf'<{tag}>.*', '', content, flags=re.DOTALL).strip()
                # |think|...|/think| 포맷도 제거
                content = re.sub(r'\|think\|.*?\|/think\|', '', content, flags=re.DOTALL).strip()
                content = re.sub(r'\|think\|.*', '', content, flags=re.DOTALL).strip()
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

        # 최근 방 우선: created 기준 내림차순 정렬 후 상위 5개만 후보로 사용
        sorted_rooms = sorted(rooms, key=lambda r: r.get("created", ""), reverse=True)
        candidates = sorted_rooms[:5]

        # 셔플하여 LLM이 항상 같은 순서를 보지 않도록
        shuffled = list(candidates)
        random.shuffle(shuffled)

        room_list = "\n".join([
            f"- [ID: {r['id']}] 주제: {r.get('topic', '?')} (댓글 {r.get('total_comments', 0)}개)"
            for r in shuffled
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
            if any(r["id"] == selected for r in candidates):
                return selected
        # fallback: 최근 방 중 랜덤 선택
        return random.choice(candidates)["id"]

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Mode C — 트렌딩 토픽으로 새 방 생성
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def fetch_trending_headlines():
        """Google News RSS에서 최신 헤드라인을 가져온다 (API 키 불필요)"""
        from xml.etree import ElementTree
        feeds = {
            "ko": "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko",
            "en": "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en",
            "ja": "https://news.google.com/rss?hl=ja&gl=JP&ceid=JP:ja",
        }
        url = feeds.get(LANG, feeds["en"])
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                xml_data = resp.read()
            root = ElementTree.fromstring(xml_data)
            items = root.findall(".//item/title")
            headlines = [item.text.strip() for item in items[:15] if item.text]
            print(f"   📰 {len(headlines)}개 뉴스 헤드라인 수집")
            return headlines
        except Exception as e:
            print(f"   ⚠️ 뉴스 수집 실패: {e}")
            return []

    def generate_topic(headlines):
        """LLM이 헤드라인을 보고 토론하기 좋은 주제를 생성한다"""
        news_str = "\n".join(f"- {h}" for h in headlines)
        messages = [{
            "role": "system",
            "content": """당신은 토론 주제 생성기입니다.
아래 최신 뉴스 헤드라인을 참고하여 사람들이 열띤 토론을 할 수 있는 매력적인 주제를 하나 만들어주세요.

규칙:
- 반드시 다음 JSON 형식으로만 출력하세요 (다른 설명 금지).
```json
{
  "ko": "한국어 토론 주제",
  "en": "영어 번역된 토론 주제"
}
```
- 의견이 갈릴 수 있는 논쟁적이거나 흥미로운 주제가 좋습니다.
- 너무 시사적이지 않게, 약간 추상화해서 누구나 참여할 수 있게 만드세요.
- 20~60자 이내."""
        }, {
            "role": "user",
            "content": f"최신 뉴스 헤드라인:\n{news_str}\n\n위 뉴스를 참고한 토론 주제:"
        }]
        topic_text = call_llm(messages, max_tokens=150)
        
        try:
            # Markdown JSON block 제거
            cleaned = re.sub(r'```json\n?', '', topic_text)
            cleaned = re.sub(r'```\n?', '', cleaned)
            topic_dict = json.loads(cleaned)
            if "ko" in topic_dict and "en" in topic_dict:
                return topic_dict
        except Exception as e:
            print(f"   ⚠️ JSON 파싱 실패: {e}")
            
        # Fallback (단일 스트링 리턴 시 양쪽 동일하게)
        fallback = re.sub(r'^[\d.\-\s"\'\'\"]+', '', topic_text).strip().strip('"\'\'\"')
        fallback = fallback[:100] if fallback else "최신 기술 동향, 어떻게 봐야 할까?"
        return {"ko": fallback, "en": fallback}

    def create_discussion_room(topic, token):
        """새 토론방을 생성한다"""
        result = api_post("/arena/games",
                          {"game_type": "discussion", "topic": topic}, token)
        if result.get("error"):
            print(f"   ❌ 방 생성 실패: {result['error']}")
            return None
        gid = result.get("game_id") or result.get("id", "")
        if gid:
            t_str = topic.get("ko", "") if isinstance(topic, dict) else topic
            print(f"   ✅ 새 방 생성 완료: {gid} | 주제: {t_str}")
        return gid

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 핵심 — 방 참가 + 댓글 작성
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def join_and_comment(gid, token):
        # 1. 방 요약 (주제 + 최근 댓글 20개)
        summary = api_get(f"/arena/games/{gid}/summary?limit=20")
        if summary.get("error"):
            print(f"❌ 방 정보 조회 실패: {summary['error']}")
            return False

        # topic_ko, topic_en이 있으면 사용, 아니면 topic 사용
        topic_ko = summary.get("topic_ko")
        topic_en = summary.get("topic_en")
        if topic_ko and topic_en:
            topic = topic_ko if LANG == "ko" else topic_en
        else:
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
            print("⚠️ LLM 응답 없음 — 댓글 생략")
            return False
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
    total_rounds = max(1, int(rounds))
    user_id = f"disc-agent-{int(time.time()) % 100000}"
    token = make_token(user_id)

    print(f"🔄 총 {total_rounds}회 실행 예정")

    for current_round in range(1, total_rounds + 1):
        if total_rounds > 1:
            print(f"\n{'='*40}")
            print(f"🔄 라운드 {current_round}/{total_rounds}")
            print(f"{'='*40}")

        if ARENA_GAME_ID:
            # Mode A: 특정 방
            print(f"🎯 Mode A: 지정된 방 {ARENA_GAME_ID}")
            join_and_comment(ARENA_GAME_ID, token)
        else:
            # 일정 확률로 Mode C (새 방 생성) vs Mode B (기존 방 참가)
            created = False
            if random.random() < ROOM_CREATE_CHANCE:
                # Mode C: 트렌딩 토픽으로 새 방 생성
                print(f"🌟 Mode C: 새 토론방 생성 시도 (확률 {ROOM_CREATE_CHANCE:.0%})")
                headlines = fetch_trending_headlines()
                if headlines:
                    topic = generate_topic(headlines)
                    if topic:
                        gid = create_discussion_room(topic, token)
                        if gid:
                            print(f"   💬 생성된 방에 첫 댓글 작성 중...")
                            join_and_comment(gid, token)
                            created = True
                if not created:
                    print("   ⚠️ 새 방 생성 실패 → Mode B로 전환")

            if not created:
                # Mode B: LLM이 기존 방 선택
                print("🔍 Mode B: 방 목록 탐색 중...")
                rooms = fetch_discussion_rooms()
                if not rooms:
                    print("❌ 참가 가능한 Discussion 방이 없습니다.")
                    continue
                print(f"   {len(rooms)}개 방 발견. LLM이 방 선택 중...")
                gid = pick_room(rooms)
                if not gid:
                    print("❌ 방 선택 실패")
                    continue
                selected = next((r for r in rooms if r["id"] == gid), {})
                print(f"   선택된 방: {gid} (주제: {selected.get('topic', '?')})")
                join_and_comment(gid, token)

        # 라운드 간 딜레이 (마지막 라운드 제외)
        if current_round < total_rounds:
            delay = random.uniform(3, 8)
            print(f"⏳ 다음 라운드까지 {delay:.1f}초 대기...")
            time.sleep(delay)
