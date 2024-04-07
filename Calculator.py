def add(n1, n2):
    return n1 + n2

def subtract(n1, n2):
    return n1 - n2

def multiply(n1, n2):
    return n1 * n2

def divide(n1, n2):
    return n1 / n2

# do it a dictionary 
operations = {
    "+" : add,
    "-" : subtract,
    "*" : multiply,
    "/" : divide
}
#create a recursion function = have a function that calls itself

def calculator():
    print(logo)
    num1 = float(input("What's the first number? "))
    for symbol in operations:
        print(symbol)
    should_continue = True
    
    while should_continue:
        operation_symbol = input("Pick an operation: ")
        num2 = float(input("What´s the second number? "))
        calculating_function = operations[operation_symbol]
        answer = calculating_function(num1, num2)
        
        print(f"{num1} {operation_symbol} {num2} = {answer}")
    
        if input(f"Type 'y' to continue calculating with {answer}\n"
                 "or type 'n' to start a new calculation: ") == "y":
            num1 = answer
        else: 
            should_continue = False
            calculator()

calculator()
