def run(exchange: str = "binance", api_key: str = "", api_secret: str = ""):
    """
    exchange: Exchange name (binance/upbit) (default: binance)
    api_key: API Key
    api_secret: API Secret
    """
    if not api_key or not api_secret:
        print("❌ api_key와 api_secret을 모두 입력해주세요.")
        return
    masked_key = api_key[:6] + "***" + api_key[-4:] if len(api_key) > 10 else "***"
    print(f"🔑 {exchange.upper()} API 설정")
    print("=" * 50)
    print(f"  Exchange : {exchange}")
    print(f"  API Key  : {masked_key}")
    print(f"  Secret   : {'*' * 8}")
    print()
    print(f"📌 아래 키를 메모리에 저장해주세요:")
    print(f"  memorize key=\"{exchange}_api_key\" value=\"{api_key}\"")
    print(f"  memorize key=\"{exchange}_api_secret\" value=\"{api_secret}\"")
    print()
    print("✅ 저장 후 인증이 필요한 코드 실행 시 자동으로 recall됩니다.")
