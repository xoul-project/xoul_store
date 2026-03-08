def run(text: str, mode: str = "encode"):
    """
    text: Text
    mode: encode or decode (default: encode)
    """
    import base64
    print(f"\U0001f504 Base64 {mode.upper()}\n"+"="*40)
    if mode=='encode':print(base64.b64encode(text.encode()).decode())
    else:
        try:print(base64.b64decode(text).decode())
        except Exception as e:print(f"\u274c {e}")