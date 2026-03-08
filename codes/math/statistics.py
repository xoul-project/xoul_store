def run(numbers: str = "10,20,30,40,50,60,70,80,90,100"):
    """
    numbers: Numbers (comma separated) (default: 10,20,30,40,50,60,70,80,90,100)
    """
    import math
    nums=sorted(float(x.strip())for x in numbers.split(',')if x.strip())
    n=len(nums);mean=sum(nums)/n
    median=nums[n//2]if n%2 else(nums[n//2-1]+nums[n//2])/2
    variance=sum((x-mean)**2 for x in nums)/n
    stddev=math.sqrt(variance)
    print(f"\U0001f4c8 Statistics ({n} values)\n"+"="*40)
    print(f"  Min:    {min(nums):,.2f}\n  Max:    {max(nums):,.2f}\n  Sum:    {sum(nums):,.2f}")
    print(f"  Mean:   {mean:,.2f}\n  Median: {median:,.2f}\n  StdDev: {stddev:,.2f}\n  Var:    {variance:,.2f}")