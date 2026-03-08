def run(token: str):
    """
    token: JWT token
    """
    import base64,json
    parts=token.split('.')
    if len(parts)<2:print('\u274c Not a valid JWT');exit()
    def dec(s):
        s+='='*(4-len(s)%4)
        return json.loads(base64.urlsafe_b64decode(s))
    print(f"\U0001f3ab JWT Decoder\n"+"="*40)
    print(f"\n  [Header]\n{json.dumps(dec(parts[0]),indent=2)}")
    p=dec(parts[1])
    print(f"\n  [Payload]\n{json.dumps(p,indent=2,ensure_ascii=False)}")
    if 'exp' in p:
        from datetime import datetime
        exp=datetime.fromtimestamp(p['exp'])
        diff=(exp-datetime.now()).total_seconds()/3600
        print(f"\n  Expires: {exp} ({'\U0001f7e2' if diff>0 else '\U0001f534'} {diff:.1f}h)")