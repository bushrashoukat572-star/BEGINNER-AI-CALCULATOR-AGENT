import math

memory = {
    "last_result": None
}

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: Division by zero"
    return a / b

def power(a, b):
    return a ** b

def sqrt(a):
    if a < 0:
        return "Error: Negative number"
    return math.sqrt(a)
