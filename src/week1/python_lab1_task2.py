"""
Task 2 – Greeting Function with String Manipulation
--------------------------------------------------
Write a function `greet_user(name)` that:
- removes extra spaces with .strip()
- capitalizes the first letter with .capitalize()
- returns "Hello, <Name>! Welcome to Python!"
Ask user for their name and print result.
"""

def greet_user(name):
    """Return a greeting message after cleaning and capitalizing the name."""
    # TODO: implement cleaning and formatting
    a = name.strip()
    b = a.capitalize()

    return b

if __name__ == "__main__":
    # TODO: read name from input and print greeting
    x = str(input('Enter word ='))
    print(greet_user(x))
    pass
