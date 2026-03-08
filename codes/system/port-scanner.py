def run(host: str = "127.0.0.1", ports: str = "22,80,443,3000,3306,5432,6379,8080,8443,9090"):
    """
    host: Target host (default: 127.0.0.1)
    ports: Ports (comma separated) (default: 22,80,443,3000,3306,5432,6379,8080,8443,9090)
    """
    import socket
    print(f"\U0001f50c Port Scan: {host}\n"+"="*40)
    for p in ports.split(','):
        p=int(p.strip());s=socket.socket();s.settimeout(1)
        r=s.connect_ex((host,p));s.close()
        st='\U0001f7e2 OPEN' if r==0 else '\u26aa CLOSED'
        print(f"  {st}  :{p}")