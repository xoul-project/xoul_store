def run(domain: str = "google.com"):
    """
    domain: Domain (default: google.com)
    """
    import socket
    tld=domain.rsplit('.',1)[-1]
    srv={'com':'whois.verisign-grs.com','net':'whois.verisign-grs.com','org':'whois.pir.org','io':'whois.nic.io'}.get(tld,f'whois.nic.{tld}')
    try:
        s=socket.socket();s.settimeout(10);s.connect((srv,43));s.send((domain+'\r\n').encode())
        resp=b''
        while True:
            d=s.recv(4096)
            if not d:break
            resp+=d
        s.close()
        print(f"\U0001f4cb WHOIS: {domain}\n"+"="*45)
        for l in resp.decode(errors='ignore').split('\n'):
            l=l.strip()
            if any(k in l.lower()for k in['domain name','registrar','creation','expir','updated','name server']):print(f"  {l}")
    except Exception as e:print(f"\u274c {e}")