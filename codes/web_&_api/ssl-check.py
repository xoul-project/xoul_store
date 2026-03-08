def run(domain: str = "google.com"):
    """
    domain: Domain (default: google.com)
    """
    import ssl,socket,datetime
    ctx=ssl.create_default_context()
    with ctx.wrap_socket(socket.socket(),server_hostname=domain) as s:
        s.settimeout(10);s.connect((domain,443));cert=s.getpeercert()
        exp=datetime.datetime.strptime(cert["notAfter"],"%b %d %H:%M:%S %Y GMT")
        days=(exp-datetime.datetime.utcnow()).days
        print(f"\U0001f512 SSL: {domain}\n"+"="*40)
        print(f"  Issuer: {dict(x[0]for x in cert['issuer']).get('organizationName','?')}")
        print(f"  Expires: {exp:%Y-%m-%d} ({'\U0001f7e2'if days>30 else'\U0001f534'} {days}d left)")