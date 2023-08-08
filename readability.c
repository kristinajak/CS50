#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    //Get input from the user
    string text = get_string("Text: ");

    //Number of letters
    int letters = count_letters(text);

    //Number of words
    int words = count_words(text);

    //Number of sentences
    int sentences = count_sentences(text);

    //Printing index
    int index = round(0.0588 * ((double)letters * 100 / words) - 0.296 * ((double)sentences * 100 / words) - 15.8);
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

int count_letters(string text)
{
    int letters = 0;
    //Counting number of letters
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] >= 'A' && text[i] <= 'z')
        {
            letters++;
        }
    }
    return letters;
}

int count_words(string text)
{
    //Counting number of words
    int words = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == ' ')
        {
            words++;
        }
    }
    return words + 1;
}

int count_sentences(string text)
{
    //Counting number of sentences
    int sentences = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == '.' || text[i] == '?' || text[i] == '!')
        {
            sentences++;
        }
    }
    return sentences;
}