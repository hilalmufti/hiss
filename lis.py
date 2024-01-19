import inspect

def trace(func):
    func.depth = 0  # Initialize a depth attribute for the function

    def wrapper(*args, **kwargs):
        # Print the call with appropriate indentation and spaces
        print(("> " * func.depth) + f"{func.__name__}({', '.join(map(str, args))})")
        func.depth += 1  # Increase depth for the next call
        result = func(*args, **kwargs)
        func.depth -= 1  # Decrease depth after returning
        # Print the return value with indentation and spaces
        print(("< " * func.depth) + f"{result}")
        return result

    return wrapper

# scheme_type = python_type
Symbol = str 
Number = (int, float)
Atom   = (Symbol, Number)
List   = list
Exp    = (Atom, List)
Env    = dict

def tokenize(program: str) -> list:
    return program.replace('(', ' ( ').replace(')', ' ) ').split()

def parse(program: str) -> Exp:
    return read_from_tokens(tokenize(program))

@trace
def read_from_tokens(tokens: list) -> Exp:
    assert len(tokens) > 0, 'unexpected EOF'
    match tokens.pop(0): 
        case '(': 
            L = []
            while tokens[0] != ')':
                L.append(read_from_tokens(tokens))
            tokens.pop(0) # pop off ')'
            return L
        case ')':   raise SyntaxError('unexpected )')
        case token: return atom(token)

def atom(token: str) -> Atom:
    if token.isdigit():                    return int(token)
    elif token.replace('.', '').isdigit(): return float(token)
    else:                                  return Symbol(token)
    
def main():
    program = "(begin (define r 10) (* pi (* r r)))"
    parse(program)

if __name__ == '__main__':
    main()