from pair import Pair, nil
from operator import truediv, add, sub, mul

def main():
    print("Welcome to the CS 111 Calculator Interpreter.")
    while True:
        try:
            user = input("calc >> ")
            if user.strip() == 'exit':
                break
            tokens = tokenize(user)
            parsed  = parse(tokens)
            if parsed is nil:
                raise ValueError("Invalid expression")
            result = eval(parsed)
            print(result)
        except Exception as e:
            print(f"Error: {e}")
    print("Goodbye!")

def tokenize(expression):
    expression1 = expression.replace('(','( ')
    expression2 = expression1.replace(')', ' )')
    splitexpression= expression2.split()
    tokens = [i for i in splitexpression]
    return tokens
def parse(tokens):
    def parse_tokens(tokens, index):
        if index >= len(tokens):
            return nil, index

        if tokens[index] == '(':
            operator = tokens[index+1]
            if index == 0:
                index += 2
                pairlist, newindex = parse_tokens(tokens,index)
                return Pair(operator,pairlist), newindex

            if index != 0:
                index += 2
                subexp, newindex = parse_tokens(tokens, index)
                pairlist2, newindex2 = parse_tokens(tokens,newindex)
                return Pair(Pair(operator, subexp),pairlist2),newindex2

        elif tokens[index] == ')':
            return nil, index+1

        else:
            try:
                value = float(tokens[index]) if '.' in tokens[index] else int(tokens[index])
                rest_expr, index = parse_tokens(tokens, index + 1)
                return Pair(value, rest_expr), index
            except ValueError:
                raise TypeError(f"Invalid token '{tokens[index]}', expected a number.")

    parsedTree, finalindex = parse_tokens(tokens,0)
    if finalindex != len(tokens):
        raise ValueError("Unexpected Tokens")
    return parsedTree

def reduce(func, operands, initial):
    result = initial
    while operands is not nil:
        result = func(result, operands.first)
        operands = operands.rest
    return result

def to_list(pair):
    list1 = []
    while pair is not nil:
        list1.append(pair.first)
        pair=pair.rest
    return list1

def apply(operator, operands):
    if operator == "+":
        return reduce(add, operands, 0 )
    elif operator == "*":
        return reduce(mul, operands, 1)
    elif operator == "-":
        return reduce(sub, operands.rest, operands.first)
    elif operator == "/":
        return reduce(truediv, operands.rest, operands.first)
    else:
        raise TypeError

def eval(expression):
    if isinstance(expression, int) or isinstance(expression, float):
        return expression
    try:
        if expression.first in ("+", "-", "*", "/"):
            operands = []
            rest = expression.rest
            while rest is not nil:
                operands.append(eval(rest.first))
                rest = rest.rest
            return apply(expression.first, expression.rest.map(eval))
    except Exception:
        raise TypeError
if __name__ == "__main__":
    main()
