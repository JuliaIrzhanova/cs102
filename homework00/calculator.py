import typing as tp
import math

def calc(num_1: float, num_2: float, command: str = "") -> tp.Union[float, str]:
    if command == "+":
        return num_1+num_2
    elif command == '-':
        return num_1 - num_2
    elif command == '/':
        if num_2 == 0:
            return f"На ноль делить нельзя."
        else:
            return num_1/num_2
    elif command == '*':
        return num_1 * num_2
    elif command == '^':
        return num_1 ** num_2
    elif command == '^2':
        return num_1**2
    elif command == 'sin':
        return math.sin(num_1)
    elif command == 'cos':
        return math.cos(num_1)
    elif command == 'tg':
        return math.tan()
    elif command == 'ln':
        if num_1<=0:
            return 'Ошибка'
        else:
            return math.log(num_1)
    elif command == 'lg':
        if num_1<=0:
            return 'Ошибка'
        else:
            return math.log10(num_1)
    else:
        return f"Неизвестный оператор: {command!r}."
if __name__ == "__main__":
    while True:
        COMMAND = input("Введите операцию > ")
        if COMMAND.isdigit() and int(COMMAND) == 0:
            break
        if  COMMAND == '^2' or COMMAND == 'sin' or COMMAND == 'cos' or COMMAND == 'tg' or COMMAND == 'ln' or COMMAND == 'lg':
            NUM_1 = float(input( "Число > "))
            print(calc(NUM_1,0,COMMAND))
        else:
            NUM_1 = float(input("Первое число > "))
            NUM_2 = float(input("Второе число > "))
            print(calc(NUM_1, NUM_2, COMMAND))
