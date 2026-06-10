from re import search, findall, sub
from functools import reduce


def es_numero(token):
    try:
        float(token)
        return True
    except ValueError:
        return False

es_operador = lambda token: token in {'+', '-', '*', '/', '^'}

def procesar_operacion(operacion: str, tk_cantidad = 3) -> list:
    """
    Tokeniza la expresion matematica, separa numeros y operadores en una lista
    """
    tokens = findall(r"\d+\.\d+|\d+|[+\-*/^()]", operacion)
    operadores = {'+', '-', '*', '/', '^'}

    if not tokens:
        return []

    # Unir '-' como signo negativo cuando aplica
    resultado = []
    i = 0
    while i < len(tokens):
        token = tokens[i]

        if token == '-' and (i == 0 or tokens[i - 1] in operadores or tokens[i - 1] == '('):
            if i + 1 < len(tokens) and es_numero(tokens[i + 1]):
                resultado.append('-' + tokens[i + 1])
                i += 2
                continue
            else:
                return []

        resultado.append(token)
        i += 1

    tokens = resultado

    # Validar paréntesis balanceados
    balance = 0
    for t in tokens:
        if t == '(':
            balance += 1
        elif t == ')':
            balance -= 1
            if balance < 0:
                return []
    if balance != 0:
        return []

    # Validaciones básicas de orden
    for j in range(len(tokens) - 1):
        actual = tokens[j]
        siguiente = tokens[j + 1]

        if actual in operadores and siguiente in operadores:
            return []

        if (es_numero(actual) or actual == ')') and siguiente == '(':
            return []

        if actual == ')' and es_numero(siguiente):
            return []

    if tokens[0] in {'*', '/', '^', ')'}:
        return []
    if tokens[-1] in operadores or tokens[-1] == '(':
        return []

    # Respetar cantidad mínima solicitada
    if len(tokens) < tk_cantidad:
        return []

    return tokens


def resolver_operadores(tokens: list, operadores_objetivo: set | list) -> list:
        """
        Busca y resuelve un grupo específico de operadores de izquierda a derecha,
        actualizando la lista de tokens hasta que no quede ninguno de esos operadores.
        """
        # 1. El 'while' revisa si ALGÚN operador objetivo sigue vivo en la lista
        while any(op in tokens for op in operadores_objetivo):
            
            # 2. Recorremos la lista para encontrar el primero de izquierda a derecha
            for i, token in enumerate(tokens):
                if token in operadores_objetivo:
                    
                    # 3. Extraemos las tres partes (izquierda, operador, derecha)
                    num_izq = tokens[i - 1]
                    operador = tokens[i]
                    num_der = tokens[i + 1]
                    
                    # 4. Calculamos usando tu función existente
                    resultado = calcular_2_valores(operador, num_izq, num_der)
                    
                    # 5. Reemplazamos esos 3 elementos originales por el resultado
                    tokens[i - 1 : i + 2] = [resultado]
                    
                    # 6. Rompemos el 'for' porque la lista cambió de tamaño, 
                    # y dejamos que el 'while' vuelva a empezar de forma segura.
                    break
                    
        return tokens


def calcular_2_valores(operador: str, num1: int | float, num2: int | float) -> float:
    """Resuelve una operacion aritmetica de 2 valores """
    if not operador or  not num1 or not num2:
        return 0
    
    if operador == "^":
        if int(num1) > 1000 and int(num2) > 1000:
            return float('inf')

    num1, num2 = float(num1), float(num2)

    suma = lambda n1, n2: n1 + n2
    resta = lambda n1, n2: n1 - n2
    multipl = lambda n1, n2: n1 * n2
    div = lambda n1, n2: n1 / n2
    exp = lambda n1, n2: n1 ** n2

    try:
        if operador == "+": resultado = num1 + num2
        elif operador == "-": resultado = num1 - num2
        elif operador == "*": resultado = num1 * num2
        elif operador == "/":
            if num2 == 0: raise ZeroDivisionError("División por cero")
            resultado = num1 / num2
        elif operador == "^":
            # Aquí es donde ocurre el overflow
            resultado = num1 ** num2
        else:
            return num1, num2
            
        return round(float(resultado), 5)

    except OverflowError:
        return float('inf') # Retornamos 'infinito' como indicador de overflow
    except ZeroDivisionError as e:
        print(f"Error matemático: {e}")
        return 0.0


def calcular_valores(expresion: str | list) -> float:
    # 1. Recibir la expresión ya tokenizada si es un string
    if isinstance(expresion, str):
        expresion = procesar_operacion(expresion, 3)
    
    # 2. Si la expresión está vacía, devolver error o lista vacía
    if not expresion or expresion == []:
        raise ValueError(f"Sintaxis inválida en la expresión: {expresion}")

    token = None
    tokens =  []
    idx_open = None
    idx_close = None
    # 3. Resolver primero los paréntesis más internos
    for t in expresion:
        if es_numero(t):
            token = float(t)
            tokens.append(t)
        else:
            tokens.append(t)

    while "(" in tokens:
        for tpos, tval in enumerate(tokens):
            #   Buscar el último '(' y el siguiente ')'
            if tval == "(":
                idx_open = tpos

            if tval == ")":
                idx_close = tpos
                break

        if idx_open is not None and idx_close is not None:
            sub_expresion = tokens[idx_open + 1:idx_close]

            resultado_interno = calcular_valores(sub_expresion)
            tokens[idx_open:idx_close + 1] = [resultado_interno]
    
    # 1. Resolvemos todas las potencias
    tokens = resolver_operadores(tokens, {'^'})
    
    # 2. Resolvemos multiplicaciones y divisiones (misma prioridad)
    tokens = resolver_operadores(tokens, {'*', '/'})
    
    # 3. Resolvemos sumas y restas (misma prioridad)
    tokens = resolver_operadores(tokens, {'+', '-'})
    
    resultado = tokens 
    # 4. Al final, la lista 'tokens' tendrá un único valor. Lo devolvemos.
    if len(tokens) == 1:
        resultado = float(tokens[0])
        return round(resultado, 5)
    else:
        return tokens # Por si algo falló y quedaron elementos

    #    Tomar todo lo que está dentro
    #    Llamar recursivamente a calcular_valores() con ese sub-bloque
    #    Reemplazar '( ... )' por su resultado

    # 4. Resolver operadores por prioridad
    #    Primero '^'
    #    Luego '*' y '/'
    #    Luego '+' y '-'

    # 5. Para cada operador encontrado:
    #    - Tomar número de la izquierda
    #    - Tomar operador
    #    - Tomar número de la derecha
    #    - Calcular con calcular_2_valores()
    #    - Reemplazar esos 3 tokens por el resultado

    # 6. Repetir hasta que solo quede un número

    # 7. Devolver el valor final como float

  
def calcular_input():
    """
    Opera la operacion aritmetica introducida
    """
    try:
        operacion = input("Introduce la operacion:\n")
    except KeyboardInterrupt:
        print("\nTe saliste de la input")
        return

    try:
        operacion = procesar_operacion(operacion)
        x = [print(i, end=" ") for i in operacion]

        if operacion == []:
            print("\nEntrada No Valida\n")
            return

        if "+" in operacion:
            resultado = round(float(operacion[0]) + float(operacion[2]), 5)

        elif "-" in operacion:
            resultado = round(float(operacion[0]) - float(operacion[2]), 5)

        elif "*" in operacion:
            resultado = round(float(operacion[0]) * float(operacion[2]), 5)

        elif "/" in operacion:
            resultado = round(float(operacion[0]) / float(operacion[2]), 5)

        elif "^" in operacion:
            resultado = round(float(operacion[0]) ** float(operacion[2]), 5)

        else:
            print("\nNo se pudo calcular")
            return

        print(f"\nEl resultado es: {resultado}\n")

    except TypeError as e:
        print(f"\nTypeError: {e}\n")

    except Exception as e:
        print(f"\nerror: {e}\n".upper())

    else:
        print("----Sin errores----\n")
