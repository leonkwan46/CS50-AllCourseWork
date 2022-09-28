#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

int getLetterNum(string text) {
    int LetterNum=0;
    for (int i=0, length=strlen(text); i<length; i++) {
        if (isalpha(text[i])) {
            LetterNum++;
        }
    }
    return LetterNum;
}

int getWordNum(string text) {
    int WordNum=1;
    for (int i=0, length=strlen(text); i<length; i++) {
        if (text[i] == ' ') {
            WordNum++;
        }
    }
    return WordNum;
}

int getSentenceNum(string text) {
    int SentenceNum=0;
    for (int i=0, length=strlen(text); i<length; i++) {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?') {
            SentenceNum++;
        }
    }
    return SentenceNum;
}

int getGrade(int NumLetter, int NumSentence, int NumWord) {
    float L = NumLetter/ (float) NumWord * 100;
    float S = NumSentence/ (float) NumWord * 100;
    float index = 0.0588 * L - 0.296 * S - 15.8;
    int Grade = round(index);
    if (Grade<1) {
        printf("Before Grade 1\n");
    } else if (Grade>=16) {
        printf("Grade 16+\n");
    } else {
        printf("Grade %i\n", Grade);
    }
    return Grade;
}

int main(void)
{
    string text;
    do {
    text = get_string("Text: ");
    } while (strlen(text) < 1);

    int NumLetter = getLetterNum(text);
    int NumWord = getWordNum(text);
    int NumSentence = getSentenceNum(text);
    int Grade = getGrade(NumLetter, NumSentence, NumWord);

}

