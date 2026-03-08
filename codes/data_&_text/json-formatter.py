def run(json_text: str):
    """
    json_text: JSON string
    """
    import json
    print("\U0001f4dd JSON Formatter\n"+"="*40)
    try:
        p=json.loads(json_text)
        print(f"\u2705 Valid | Type: {type(p).__name__}")
        if isinstance(p,dict):print(f"  Keys: {len(p)}")
        elif isinstance(p,list):print(f"  Items: {len(p)}")
        print(f"\n{json.dumps(p,indent=2,ensure_ascii=False)}")
    except json.JSONDecodeError as e:print(f"\u274c Invalid: {e}")