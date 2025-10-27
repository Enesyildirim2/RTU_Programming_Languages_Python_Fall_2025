"""
Task 3 – Function with Combined Logic
------------------------------------
Write a function `analyze_sentence(text)` that returns:
1. total character count (len)
2. word count (split)
3. whether it contains the word "Python" (case-insensitive)
Return results as a tuple and print summary in main.
"""

def analyze_sentence(text):
    """Return length, word count, and whether 'Python' appears in text."""
    # TODO: implement function logic
    a = len(text)
    b = len(text.split())
    c = text.find('Python')
    if c == 0:
        d = print('There is Python word')
    else:
        d = print('There is no Python word')
    return a, b, d

if __name__ == "__main__":
    # TODO: read sentence from input, call function, and print results
    a = str(input('Enter word ='))
    print(analyze_sentence(a))
    pass
