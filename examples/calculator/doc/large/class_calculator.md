# Calculator Class Documentation

## Overview

The `cal` class is a simple calculator implementation in Python that performs basic arithmetic operations such as addition, subtraction, multiplication, and division. The calculator takes two numbers as input from the user and allows continuous operation until the user decides to exit.

## Class Definition

### `cal`

This class encapsulates the arithmetic operations for two numbers. 

#### Initialization

```python
def __init__(self, a: int, b: int)
```

**Parameters:**

- `a` (int): The first number for calculations.
- `b` (int): The second number for calculations.

**Usage:**

To create an object of the class, provide two integers as arguments.

```python
obj = cal(5, 10)  # Example instantiation of the class
```

### Methods

#### `add()`

```python
def add(self) -> int
```

**Returns:**

- int: The sum of `self.a` and `self.b`.

**Example:**

```python
result = obj.add()  # Adds the two numbers
print(result)       # Prints the result
```

#### `sub()`

```python
def sub(self) -> int
```

**Returns:**

- int: The difference between `self.a` and `self.b`.

**Example:**

```python
result = obj.sub()  # Subtracts the two numbers
print(result)       # Prints the result
```

#### `mul()`

```python
def mul(self) -> int
```

**Returns:**

- int: The product of `self.a` and `self.b`.

**Example:**

```python
result = obj.mul()  # Multiplies the two numbers
print(result)       # Prints the result
```

#### `div()`

```python
def div(self) -> float
```

**Returns:**

- float: The quotient of `self.a` divided by `self.b`. If `self.b` is zero, this will raise a `ZeroDivisionError`.

**Example:**

```python
result = obj.div()  # Divides the two numbers
print(result)       # Prints the result rounded to 2 decimal places
```

## User Interaction

The calculator operates in a loop, allowing the user to select which operation to perform. The user can choose to:

- **Add** the numbers
- **Subtract** the numbers
- **Multiply** the numbers
- **Divide** the numbers
- **Exit** the program

### Input Handling

The user inputs two integers at the start of the program:
```python
a = int(input("Enter first number: "))
b = int(input("Enter second number: "))
```

### Menu Loop

The interactive menu is presented as follows:

```python
while choice != 0:
    print("0. Exit")
    print("1. Add")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    choice = int(input("Enter choice: "))
```

Depending on the user's choice, the corresponding method of the `cal` class is called to perform the operation. The result is displayed immediately after the calculation.

### Example Usage

Here’s an example of how the code can be run:

```python
Enter first number: 10
Enter second number: 5
0. Exit
1. Add
2. Subtraction
3. Multiplication
4. Division
Enter choice: 1
Result: 15
...
```

The loop will continue until the user inputs `0` to exit the program.

## Note on Error Handling

Currently, the code does not handle potential errors such as:
- Non-integer inputs when asking for numbers.
- Division by zero would raise an error but is not caught in the current implementation. Proper error handling should be introduced to manage these cases more gracefully.

## Conclusion

The `cal` class is a straightforward implementation of a calculator in Python that illustrates basic object-oriented principles. It allows for easy extension and modification, such as adding more operations or refining user input handling.

