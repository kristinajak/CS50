#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>


typedef uint8_t BYTE;
const int BLOCK_SIZE = 512;

int main(int argc, char *argv[])
{
    //Check command-line arguments
    if (argc != 2)
    {
        printf("Usage: ./recover filename\n");
        return 1;
    }

    //Check if the input file can be opened
    FILE *fp = fopen(argv[1], "r");
    if (fp == NULL)
    {
        printf("Cannot open the file\n");
        return 1;
    }

    BYTE buffer[BLOCK_SIZE];
    char photo[8];
    FILE *img;
    int photo_counter = 0;
    bool photo_found = false;

    while (fread(buffer, sizeof(BYTE), BLOCK_SIZE, fp) != 0)
    {
        //Check whether the criterias of jpg are met
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //Closing previous file if already opened
            if (photo_counter != 0)
            {
                fclose(img);
            }

            //Found the first photo
            photo_found = true;

            //Naming the photo and opening the file for writing
            sprintf(photo, "%03i.jpg", photo_counter);
            img = fopen(photo, "w");

            //Unable to create a file
            if (img == NULL)
            {
                printf("Unable to create a file\n");
                return 2;
            }

            //Writing to a file
            fwrite(buffer, sizeof(BYTE), BLOCK_SIZE, img);

            //Incrementing the number of photos
            photo_counter++;
        }

        //Continuing moving the bytes to current jpg
        else
        {
            if (photo_found)
            {
                fwrite(buffer, sizeof(BYTE), BLOCK_SIZE, img);
            }
        }
    }
    return 0;
    //Closing files
    fclose(fp);
    fclose(img);
}