def run(count: str = "5"):
    """
    count: Count (default: 5)
    """
    import uuid
    print(f"\U0001f194 UUID Generator\n"+"="*40)
    for i in range(int(count)):print(f"  {i+1}. {uuid.uuid4()}")