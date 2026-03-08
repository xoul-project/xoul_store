def run(text: str):
    """
    text: Text to analyze
    """
    import re
    chars=len(text);words=len(text.split());lines=text.count('\n')+1
    print(f"\U0001f4ca Text Stats\n"+"="*40)
    print(f"  Chars: {chars:,}\n  Words: {words:,}\n  Lines: {lines}\n  Read: ~{max(1,words//200)}min")
    freq={}
    for w in re.findall(r'\w+',text.lower()):freq[w]=freq.get(w,0)+1
    print('\n  Top words:')
    for w,c in sorted(freq.items(),key=lambda x:-x[1])[:8]:print(f"    {w}: {c}")