def run(text: str = "Hello"):
    """
    text: Text (default: Hello)
    """
    import hashlib
    print("QR Pattern\n"+"="*40+"\n  Text: "+text)
    h=hashlib.sha256(text.encode()).hexdigest()
    for y in range(15):
        row="  "
        for x in range(15):
            idx=(y*15+x)%len(h)
            if y<2 or y>=13 or x<2 or x>=13:row+=chr(9608)*2
            elif int(h[idx],16)>7:row+=chr(9608)*2
            else:row+="  "
        print(row)
