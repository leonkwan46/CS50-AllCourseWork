#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

int main(int argc, string argv[])
{

    if (argc != 2) {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    string key = argv[1];
    int input_length = strlen(key);
    for (int i = 0; i<input_length; i++) {
        if (!isalpha(key[i])) {
            printf("Usage: ./substitution key\n");
            return 1;
        }
    }

    if (input_length != 26) {
        printf("MUST CONTAIN 26 CHARACTERS.\n");
        return 1;
    }

    for (int i = 0; i < input_length; i++) {
        for (int j = i + 1; j < input_length; j++) {
            if (toupper(key[i]) == toupper(key[j])) {
                printf("Usage: ./substitution key\n");
                return 1;
            }
        }
    }

    //Get Plain text
    string plaintext = get_string("plaintext: ");

    for (int i = 0; i < input_length; i++) {
        if (islower(key[i])) {
            key[i] -= 32;
        }
    }

    printf("ciphertext: ");

    for (int i = 0; i < strlen(plaintext); i++) {
        if (isupper(plaintext[i])) {
            int letter = plaintext[i] - 65;
            printf("%c", key[letter]);
        } else if (islower(plaintext[i])) {
            int letter = plaintext[i] - 97;
            printf("%c", key[letter] + 32);
        } else printf("%c", plaintext[i]);
    }

    printf("\n");
    return 0;
}