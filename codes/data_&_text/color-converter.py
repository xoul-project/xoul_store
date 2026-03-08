def run(color: str = "#FF5500"):
    """
    color: Color (#FF5500 or 255,85,0) (default: #FF5500)
    """
    print("Color Converter\n"+"="*40)
    if color.startswith("#"):
        h=color.lstrip("#");r,g,b=int(h[0:2],16),int(h[2:4],16),int(h[4:6],16)
    else:
        r,g,b=map(int,color.split(","));h=f"{r:02x}{g:02x}{b:02x}"
    print(f"  HEX: #{h.upper()}\n  RGB: ({r},{g},{b})")
    mx,mn=max(r,g,b)/255,min(r,g,b)/255;l=(mx+mn)/2
    if mx==mn:hue=s=0
    else:
        d=mx-mn;s=d/(2-mx-mn)if l>0.5 else d/(mx+mn)
        if mx==r/255:hue=((g/255-b/255)/d+(6 if g<b else 0))*60
        elif mx==g/255:hue=((b/255-r/255)/d+2)*60
        else:hue=((r/255-g/255)/d+4)*60
    print(f"  HSL: ({hue:.0f}, {s*100:.0f}%, {l*100:.0f}%)")
