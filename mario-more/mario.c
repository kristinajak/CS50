#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n < 1 || n > 8);

    // number of rows
    for (int i = 1; i < n + 1; i++)
    {
        for (int s = 0; s < n - i; s++)
        {
            printf(" "); // print spaces
        }
        for (int j = 0; j < i ; j++)
        {
            printf("#"); // print hashes
        }
        {
            printf("  "); //space between
        }
        for (int j = 0; j < i ; j++)
        {
            printf("#"); // print hashes
        }

        printf("\n"); // print next line
    }
}