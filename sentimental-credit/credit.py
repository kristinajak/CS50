from cs50 import get_string

# Imput from the user
number = get_string("Credit card number: ")
total_digits = len(number)


def main():

    # Sum of all results to get Luhn's number

    result = validity(n1) + remaining(n2)

# If valid according to Luhn, checking the type of card

    if int(repr(result)[-1]) == 0:

        if total_digits == 15 and (int(str(number)[:2]) == 34 or 37):
            print("AMEX")

        elif total_digits == 16 and (int(str(number)[:2]) in range(51, 56)):
            print("MASTERCARD")

        elif (total_digits == 13 or 16) and int(str(number)[:1]) == 4:
            print("VISA")

    else:
        print("INVALID")

# Every other digit, starting with the number’s second-to-last digit


def n1(number):

    num = int(number)

# Initializing a list

    n1 = []

    while num > 0:

        # Getting every second digit from the end

        digit = num % 100
        digit = int(digit / 10)
        n1.append(digit)

        num = int(num / 100)

    return n1

# Remaining digits


def n2(number):

    num = int(number)

# Initializing a list

    n2 = []

    while num > 0:

        # Getting remaining digits

        digit = num % 10
        n2.append(digit)

        num = int(num / 100)

    return n2

# Calculations with n1


def validity(n1):

    all_added = 0

# Multipication by 2

    for element in n1(number):
        digit_x_2 = int(element) * 2

        total_sum_of_digits = 0
        sum_of_digits = 0

# Sum of multiplied elements

        for element in str(digit_x_2):
            sum_of_digits += int(element)

# Total of all digits

        total_sum_of_digits += sum_of_digits
        all_added += total_sum_of_digits

    return all_added

# Calculations with n2


def remaining(n2):

    sum = 0
    for element in n2(number):
        sum += int(element)
    return sum


main()
