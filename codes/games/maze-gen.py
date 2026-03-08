def run(size: str = "10"):
    """
    size: Maze size (default: 10)
    """
    import random
    n=int(size)
    maze=[[1]*(2*n+1)for _ in range(2*n+1)]
    for i in range(n):
        for j in range(n):maze[2*i+1][2*j+1]=0
    visited=set();stack=[(0,0)];visited.add((0,0))
    while stack:
        x,y=stack[-1];neighbors=[]
        for dx,dy in[(0,1),(0,-1),(1,0),(-1,0)]:
            nx,ny=x+dx,y+dy
            if 0<=nx<n and 0<=ny<n and(nx,ny)not in visited:neighbors.append((nx,ny,dx,dy))
        if neighbors:
            nx,ny,dx,dy=random.choice(neighbors)
            maze[2*x+1+dx][2*y+1+dy]=0
            visited.add((nx,ny));stack.append((nx,ny))
        else:stack.pop()
    maze[1][0]=0;maze[2*n-1][2*n]=0
    print(f"\U0001f3f0 Maze ({n}x{n})\n")
    for row in maze:print('  '+''.join('\u2588\u2588'if c else'  'for c in row))