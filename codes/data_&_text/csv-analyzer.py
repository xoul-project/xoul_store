def run(csv_text: str):
    """
    csv_text: CSV data with header
    """
    import csv,io
    reader=csv.reader(io.StringIO(csv_text));rows=list(reader)
    if not rows:print('(empty)');exit()
    hdr=rows[0];data=rows[1:]
    print(f"\U0001f4c8 CSV Analysis\n"+"="*40+f"\n  Cols: {len(hdr)} | Rows: {len(data)}\n  Headers: {', '.join(hdr)}")
    for i,col in enumerate(hdr):
        vals=[r[i]for r in data if i<len(r)and r[i]];nums=[]
        for v in vals:
            try:nums.append(float(v.replace(',','')))
            except:pass
        if nums:print(f"\n  [{col}] min={min(nums):.2f} max={max(nums):.2f} avg={sum(nums)/len(nums):.2f}")
        else:print(f"\n  [{col}] {len(set(vals))} unique values")