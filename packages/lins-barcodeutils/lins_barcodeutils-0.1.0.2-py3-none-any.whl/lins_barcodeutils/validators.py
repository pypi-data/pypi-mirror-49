

def calculate_check_digit(segment):
    k = 2
    soma = 0
    start = len(segment)-1
    for i in range(start, -1, -1):
        soma = (soma + (ord(segment[i]) - ord('0')) * k)
        k += 1
        if k > 9:
            k = 2
    digit = 11 - (soma % 11)
    if digit >= 10:
        digit = 0
    return chr(digit + ord('0'))


def validate_check_digit(barcode):
    check_digit = barcode[-1:]
    barcode = barcode[:-1]
    return calculate_check_digit(barcode) == check_digit
