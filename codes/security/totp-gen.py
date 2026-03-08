def run(secret: str):
    """
    secret: Base32 secret key
    """
    import hmac,hashlib,struct,time,base64
    def totp(secret,interval=30):
        key=base64.b32decode(secret.upper()+'='*(8-len(secret)%8))
        t=int(time.time()//interval)
        msg=struct.pack('>Q',t)
        h=hmac.new(key,msg,hashlib.sha1).digest()
        o=h[-1]&0x0F
        code=(struct.unpack('>I',h[o:o+4])[0]&0x7FFFFFFF)%1000000
        remaining=interval-int(time.time())%interval
        return f"{code:06d}",remaining
    print(f"\U0001f510 TOTP Generator\n"+"="*40)
    code,rem=totp(secret)
    print(f"  Code: {code}\n  Expires in: {rem}s")