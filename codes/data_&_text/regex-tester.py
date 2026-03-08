def run(pattern: str, text: str):
    """
    pattern: Regex pattern
    text: Test text
    """
    import re
    print(f"\U0001f50e Regex: {pattern}\n"+"="*40)
    try:
        m=list(re.finditer(pattern,text))
        print(f"  Matches: {len(m)}")
        for i,x in enumerate(m[:15]):print(f"    [{i}] pos={x.start()}: '{x.group()}'")
    except re.error as e:print(f"\u274c {e}")