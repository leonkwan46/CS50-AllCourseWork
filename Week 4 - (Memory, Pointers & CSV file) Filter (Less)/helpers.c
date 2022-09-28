#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i=0; i < height; i++) {
        for (int j=0; j < width; j++) {
            float average2 = (image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.00;
            int average = round(average2);
            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i=0; i < height; i++) {
        for (int j=0; j < width; j++) {
              int sepiaRed = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
              int sepiaGreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
              int sepiaBlue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);
              if (sepiaRed > 255) {
                  sepiaRed = 255;
              }
              if (sepiaGreen > 255) {
                  sepiaGreen = 255;
              }
              if (sepiaBlue > 255) {
                  sepiaBlue = 255;
              }
              image[i][j].rgbtRed = sepiaRed;
              image[i][j].rgbtGreen = sepiaGreen;
              image[i][j].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i=0; i<height; i++) {
        for (int j=0; j<(width/2); j++) {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];

    for (int i=0; i <height; i++) {
        for (int j=0; j<width; j++) {
            float counter = 0.00;
            int totalRed=0, totalGreen=0, totalBlue=0;

            for (int x=-1; x<2; x++) {
                for (int y=-1; y<2; y++) {
                    int curX = i + x;
                    int curY = j + y;

                    if ((curX >= 0 && curX < height) && (curY >= 0 && curY < width)) {
                    totalRed += image[curX][curY].rgbtRed;
                    totalGreen += image[curX][curY].rgbtGreen;
                    totalBlue += image[curX][curY].rgbtBlue;
                    counter++;
                    }
                }
            }
            temp[i][j].rgbtRed = round(totalRed/counter);
            temp[i][j].rgbtGreen = round(totalGreen/counter);
            temp[i][j].rgbtBlue = round(totalBlue/counter);
        }
    }

    for (int i=0; i <height; i++) {
        for (int j=0; j<width; j++) {
            image[i][j].rgbtRed = temp[i][j].rgbtRed;
            image[i][j].rgbtGreen = temp[i][j].rgbtGreen;
            image[i][j].rgbtBlue = temp[i][j].rgbtBlue;
        }
    }
    return;
}
