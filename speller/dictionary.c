// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

int count_words = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int index = hash(word);
    node *p = table[index];

    while (p != NULL)
    {
        if (strcasecmp(p->word, word) == 0)
        {
            return true;
        }

        p = p->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    int length = strlen(word);
    int hash_number = 0;
    int sum = 0;
    for (int i = 0; i < length; i++)
    {
        sum += toupper(word[i]);
        hash_number = sum % N;
    }
    return hash_number;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    //Open the dictionary file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("Cannot open the dictionary\n");
        return false;
    }

    //Initializing table and setting all data to NULL - table is empty

    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }

    //Read string from the dictionary file until the EOF
    char tmp_word[LENGTH + 1];
    while (fscanf(file, "%s", tmp_word) != EOF)
    {
        //Allocate memory
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            printf("Cannot allocate the memory/n");
            return false;
        }

        //Copying the word into the node
        strcpy(n->word, tmp_word);
        n->next = NULL;

        //At the particular hash location
        int index = hash(tmp_word);
        if (table[index] == NULL)
        {
            table[index] = n;
            n->next = NULL;
        }
        else
        {
            n->next = table[index];
            table[index] = n;
        }
        count_words++;
    }
    fclose(file);
    return true;
}



// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return count_words;

}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *p = table[i];
        while (p != NULL)
        {
            node *delete = p;
            p = p->next;
            free(delete);
        }
        table[i] = NULL;
    }
    return true;
}
