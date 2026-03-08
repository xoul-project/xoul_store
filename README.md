# 🧠 Xoul Store

Community-contributed personas, workflows, and code utilities for the [Xoul AI Agent](https://github.com/akirasum/xoul).

## 📂 Structure

```
xoul-store/
├── codes/           # Python utility scripts
│   ├── finance/
│   ├── system/
│   ├── text/
│   └── manifest.json
├── personas/        # AI persona prompts
│   ├── research/
│   ├── productivity/
│   ├── daily_routine/
│   └── manifest.json
└── workflows/       # Pre-built workflow templates
    └── manifest.json
```

## 🤝 Contributing

1. **Fork** this repo
2. **Add** your file in the appropriate category folder
3. **Update** the corresponding `manifest.json`
4. **Submit** a Pull Request

### Adding a Code
- Create a `.py` file with `def run(params):` signature
- Add entry to `codes/manifest.json`

### Adding a Persona
- Create a `.md` file with the persona prompt
- Add entry to `personas/manifest.json`

## 📊 Stats

- **50** Codes across 9 categories
- **40** Personas across 6 categories

## 📦 Codes

### Data & Text
- 📝 **JSON Formatter / JSON 포매터**
- 🔄 **Base64 Encode/Decode / Base64 변환**
- #️⃣ **Hash Generator / 해시 생성**
- 📊 **Text Statistics / 텍스트 분석**
- 🔎 **Regex Tester / 정규식 테스터**
- 📈 **CSV Analyzer / CSV 분석**
- 📱 **QR Code Text / QR코드 텍스트**
- 🎨 **Color Converter / 색상 변환**

### Finance
- 💹 **Binance Portfolio / 바이낸스 포트폴리오**
- 📈 **Crypto Prices / 암호화폐 시세**
- 😱 **Fear & Greed Index / 공포/탐욕 지수**
- 💱 **Exchange Rates / 환율 조회**
- 📊 **Stock Price / 주식 시세**
- ⛽ **ETH Gas Tracker / ETH 가스비**

### Games
- 🎲 **Dice Roller / 주사위 게임**
- 🎨 **ASCII Art / ASCII 아트**
- 🥠 **Fortune Cookie / 포춘 쿠키**
- 🏰 **Maze Generator / 미로 생성**
- 🔢 **Number Guessing / 숫자 맞추기**
- 👁️ **Arena Spectator / 아레나 관전**
- 📊 **Arena Statistics / 아레나 통계**
- 🎮 **Mafia Game Agent / 마피아게임 에이전트**

### Math
- 🔢 **Prime Checker / 소수 판별**
- 🌀 **Fibonacci Sequence / 피보나치 수열**
- 📈 **Statistics Calculator / 통계 계산기**
- 🧮 **Matrix Calculator / 행렬 연산**

### Network
- 📡 **Ping Test / 핑 테스트**
- 📰 **Hacker News Top / Hacker News 인기글**
- 🐙 **GitHub Trending / GitHub 트렌딩**
- ⚡ **Download Speed Test / 다운로드 속도 측정**

### Productivity
- 🕐 **Timezone Converter / 시간대 변환**
- ⏳ **D-Day Countdown / D-Day 카운트다운**
- 📐 **Unit Converter / 단위 변환**
- 🎲 **Random Picker / 랜덤 선택기**
- 🍅 **Pomodoro Timer / 포모도로 타이머**

### Security
- 🔑 **Password Generator / 비밀번호 생성**
- 🎫 **JWT Decoder / JWT 디코더**
- 🆔 **UUID Generator / UUID 생성**
- 🔐 **TOTP Generator / TOTP 생성**
- 💪 **Password Strength / 비밀번호 강도**

### System
- 🔌 **Port Scanner / 포트 스캐너**
- 💾 **System Status / 시스템 상태**
- 📋 **Process Monitor / 프로세스 모니터**
- ⏰ **Cron Parser / Cron 스케줄 해석**
- 🔧 **Environment Variables / 환경 변수 탐색**

### Web & API
- 🌍 **IP Information / IP 정보 조회**
- 🔍 **DNS Lookup / DNS 조회**
- 🏥 **HTTP Status Check / 사이트 상태 체크**
- 🔒 **SSL Certificate Check / SSL 인증서 체크**
- 📋 **WHOIS Lookup / WHOIS 조회**

## 🎭 Personas

### Daily Routine
- 🧘 **Anxiety Relief Guide** (en)
- 🧘 **불안 해소 가이드** (ko)
- ☀️ **Daily Briefing** (en)
- ☀️ **일일 브리핑** (ko)
- 🌙 **Daily Review** (en)
- 🌙 **일일 리뷰** (ko)
- 🥗 **Diet Tracker** (en)
- 🥗 **식단 관리사** (ko)
- 🌤️ **Weather Briefing Assistant** (en)
- 🌤️ **날씨 브리핑 어시스턴트** (ko)

### Data
- 📊 **Data Analyst** (en)
- 📊 **데이터 분석가** (ko)

### DevOps
- 🐍 **Python Developer** (en)
- 🐍 **파이썬 개발자** (ko)
- 🖥️ **System Admin** (en)
- 🖥️ **시스템 관리자** (ko)
- 🔀 **Git & Code Manager** (en)
- 🔀 **깃 & 코드 매니저** (ko)

### Finance
- 💰 **Expense Tracker** (en)
- 💰 **가계부 도우미** (ko)

### Productivity
- 💡 **Creative Thought Partner** (en)
- 💡 **창의적 사고 파트너** (ko)
- 🚀 **Founder Coach** (en)
- 🚀 **창업 코치** (ko)
- 📧 **Email Manager** (en)
- 📧 **이메일 매니저** (ko)
- 📅 **Schedule Planner** (en)
- 📅 **일정 플래너** (ko)
- 📁 **File Organizer** (en)
- 📁 **파일 정리사** (ko)
- 🧠 **Personal Knowledge Manager** (en)
- 🧠 **개인 지식 관리자** (ko)

### Research
- 📝 **Academic Writing Coach** (en)
- 📝 **학술 글쓰기 코치** (ko)
- 🔍 **Competitor Analyst** (en)
- 🔍 **경쟁사 분석가** (ko)
- 📰 **Tech News Researcher** (en)
- 📰 **기술 뉴스 리서처** (ko)
- 🛒 **Price Tracker** (en)
- 🛒 **가격 추적기** (ko)

