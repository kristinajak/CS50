#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size
    int n;
    do
    {
        n = get_int("Start size: ");
    }
    while (n < 9);

    // TODO: Prompt for end size
    int y;
    do
    {
        y = get_int("End size: ");
    }
    while (y < n);

    // TODO: Calculate number of years until we reach threshole
    int count = 0;
    while (n < y)
    {
        n = n + (n / 3) - (n / 4);
        count++;
    }
    // TODO: Print number of years
    printf("Years: %i\n", count);
}
