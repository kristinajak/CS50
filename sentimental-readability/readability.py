from cs50 import get_string


def main():

    # Get input from the user
    text = get_string("Text: ")

    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    # Calculating index
    index = round(0.0588 * (letters * 100 / words) - 0.296 * (sentences * 100 / words) - 15.8)

    # Evaluating grades
    if index < 1:

        print("Before Grade 1")

    elif index > 16:

        print("Grade 16+")

    else:

        print(f"Grade {index}")


def count_letters(text):
    # Calculating number of letters

    letters = 0
    for i in range(0, len(text)):
        if text[i] >= 'A' and text[i] <= 'z':
            letters += 1
    return letters


def count_words(text):
    # Calculating number of words

    words = 0
    for i in range(0, len(text)):
        if text[i] == ' ':
            words += 1
    return words + 1


def count_sentences(text):
    # Calculating number of sentences

    sentences = 0
    for i in range(0, len(text)):
        if text[i] in ['.', '?', '!']:
            sentences += 1
    return sentences


main()
