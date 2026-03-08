def run(matrix_a: str = "1,2;3,4", operation: str = "det"):
    """
    matrix_a: Matrix A (rows separated by ;) (default: 1,2;3,4)
    operation: Operation: det, transpose, square (default: det)
    """
    def parse(s):return[[float(x)for x in row.split(',')]for row in s.split(';')]
    A=parse(matrix_a)
    print(f"\U0001f9ee Matrix ({operation})\n"+"="*40)
    print('  A =')
    for row in A:print(f"    [{' '.join(f'{x:>6.2f}'for x in row)}]")
    if operation=='det':
        if len(A)==2:d=A[0][0]*A[1][1]-A[0][1]*A[1][0]
        elif len(A)==3:d=A[0][0]*(A[1][1]*A[2][2]-A[1][2]*A[2][1])-A[0][1]*(A[1][0]*A[2][2]-A[1][2]*A[2][0])+A[0][2]*(A[1][0]*A[2][1]-A[1][1]*A[2][0])
        else:d='(only 2x2/3x3)'
        print(f"\n  det(A) = {d}")
    elif operation=='transpose':
        T=list(map(list,zip(*A)))
        print('\n  A^T =')
        for row in T:print(f"    [{' '.join(f'{x:>6.2f}'for x in row)}]")
    elif operation=='square':
        n=len(A)
        R=[[sum(A[i][k]*A[k][j]for k in range(len(A[0])))for j in range(n)]for i in range(n)]
        print('\n  A*A =')
        for row in R:print(f"    [{' '.join(f'{x:>6.2f}'for x in row)}]")