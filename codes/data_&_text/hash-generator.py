def run(text: str):
    """
    text: Text to hash
    """
    import hashlib
    print(f"#\ufe0f\u20e3 Hash Generator\n"+"="*40+f"\n  Input: {text[:50]}")
    for a in['md5','sha1','sha256','sha512']:print(f"  {a.upper():<8}: {hashlib.new(a,text.encode()).hexdigest()}")