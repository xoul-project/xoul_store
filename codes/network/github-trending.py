def run(language: str = "python"):
    """
    language: Language (default: python)
    """
    import urllib.request,json
    url=f'https://api.github.com/search/repositories?q=language:{language}&sort=stars&order=desc&per_page=10'
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
    with urllib.request.urlopen(req,timeout=10) as r:data=json.loads(r.read())
    print(f"\U0001f419 GitHub Top {language}\n"+"="*50)
    for i,repo in enumerate(data.get('items',[])[:10]):
        print(f"  {i+1}. \u2b50{repo['stargazers_count']:,} {repo['full_name']}")
        print(f"     {repo.get('description','')[:60]}")