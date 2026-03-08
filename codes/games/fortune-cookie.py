def run():
    import random
    quotes=[
    'The best way to predict the future is to create it. - Peter Drucker',
    'Stay hungry, stay foolish. - Steve Jobs',
    'The only way to do great work is to love what you do. - Steve Jobs',
    'In the middle of difficulty lies opportunity. - Albert Einstein',
    'Simplicity is the ultimate sophistication. - Leonardo da Vinci',
    'Innovation distinguishes between a leader and a follower. - Steve Jobs',
    'The journey of a thousand miles begins with one step. - Lao Tzu',
    'Talk is cheap. Show me the code. - Linus Torvalds',
    'First, solve the problem. Then, write the code. - John Johnson',
    'Code is like humor. When you have to explain it, it is bad. - Cory House',
    'Debugging is twice as hard as writing the code in the first place.',
    'There are only two hard things in CS: cache invalidation and naming things.',
    'Any fool can write code that a computer can understand. Good programmers write code that humans can understand. - Martin Fowler',
    'Programs must be written for people to read, and only incidentally for machines to execute. - Abelson',
    'The best error message is the one that never shows up. - Thomas Fuchs',
    ]
    q=random.choice(quotes)
    print(f"\U0001f960 Fortune Cookie\n"+"="*45+f"\n\n  \"{q}\"")