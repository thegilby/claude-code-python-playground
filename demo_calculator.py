def add(a, b):
    """Add two numbers."""
    return a + b

def multiply(a, b):
    """Multiply two numbers."""
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Arguments must be numbers")
    return a * b

class Calculator:
    """Simple calculator class."""

    def __init__(self):
        self.history = []

    def calculate(self, operation, a, b):
        """Perform calculation and store in history."""
        if operation == "add":
            result = add(a, b)
        elif operation == "multiply":
            result = multiply(a, b)
        else:
            raise ValueError("Unsupported operation")

        self.history.append(f"{a} {operation} {b} = {result}")
        return result
