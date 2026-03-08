def run(length: str = "16", count: str = "5"):
    """
    length: Length (default: 16)
    count: Count (default: 5)
    """
    import secrets,string
    chars=string.ascii_letters+string.digits+string.punctuation
    print(f"\U0001f511 Passwords (len={length})\n"+"="*40)
    for i in range(int(count)):
        pw=''.join(secrets.choice(chars)for _ in range(int(length)))
        strength=sum([any(c.isupper()for c in pw),any(c.islower()for c in pw),any(c.isdigit()for c in pw),any(c in string.punctuation for c in pw)])
        bar='\U0001f7e2'*strength+'\u26aa'*(4-strength)
        print(f"  {i+1}. {pw}  {bar}")