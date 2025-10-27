"""
Task 4 – Text-based Arithmetic Analyzer
--------------------------------------
Create a text-based analyzer that:
1. Counts non-space characters.
2. Counts words.
3. Extracts numbers and computes their sum and average.
Use helper functions:
- count_characters(text)
- count_words(text)
- extract_numbers(text)
- analyze_text(text)
Print formatted summary in main.
"""

def count_characters(text):
    """Count non-space characters in a string."""
    # TODO: implement
    a = len(text.replace(" ", ""))
    return a


def count_words(text):
    """Count number of words in a string."""
    # TODO: implement
    b = len(text.split())
    return b

def extract_numbers(text):
    """Return list of integers found in text."""
    a = text.split()
    numbers = []
    for item in a:
        if item.isdigit():
            numbers.append(int(item))
    return numbers
    # TODO: implement

def analyze_text(text):
    """Perform text-based arithmetic analysis."""
    # TODO: call helper functions and compute total, average, etc.
    total_chars = count_characters(text)
    total_words = count_words(text)
    numbers = extract_numbers(text)
    total_sum = sum(numbers)
    average = total_sum / len(numbers)
    return total_chars, total_words, total_sum, average

if __name__ == "__main__":
    # TODO: read input, call analyze_text(), and print results
    text = input("Enter text: ")
    print(analyze_text(text))
    pass
