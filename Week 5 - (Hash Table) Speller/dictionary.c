// Implements a dictionary's functionality
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <cs50.h>
#include <string.h>
#include <strings.h>

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

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    node *n = table[hash(word)];
    while (n != NULL) {
        if (strcasecmp(word, n->word) == 0) {
            return true;
        }
        n = n->next;
    }
    return false;
}

//counter for size()
int counter = 0;

// Hashes word to a number
// Reference: https://youtu.be/W8xO00s5jyk
unsigned int hash(const char *word)
{
    int hashValue = 0;
    int lenght = strlen(word);
    for (int i=0; i<lenght; i++) {
        hashValue += tolower(word[i]);
    }
    return hashValue%N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    if (file == NULL) {
        return false;
    }

    char word[LENGTH+1];
    while (fscanf(file, "%s", word) != EOF) {
        node *n = malloc(sizeof(node));
        if (n == NULL) {
            return false;
        }
        strcpy(n->word, word);

        int index =  hash(word);
        if (table[index] == NULL) {
            table[index] = n;
            n->next = NULL;
        } else {
            n->next = table[index];
            table[index] = n;
        }
    counter++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return counter;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i=0; i<N; i++) {
        while (table[i] != NULL) {
            node *temp = table[i];
            table[i] = table[i]->next;
            free(temp);
        }
    }
    return true;
}
