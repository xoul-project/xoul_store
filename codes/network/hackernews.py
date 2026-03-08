def run(count: str = "10"):
    """
    count: Count (default: 10)
    """
    import urllib.request,json
    ids=json.loads(urllib.request.urlopen('https://hacker-news.firebaseio.com/v0/topstories.json',timeout=10).read())
    print(f"\U0001f4f0 HN Top {count}\n"+"="*50)
    for j,sid in enumerate(ids[:int(count)]):
        s=json.loads(urllib.request.urlopen(f'https://hacker-news.firebaseio.com/v0/item/{sid}.json',timeout=10).read())
        print(f"  {j+1}. [{s.get('score',0)}\u2b06] {s.get('title','')}")
        if s.get('url'):print(f"     {s['url'][:70]}")