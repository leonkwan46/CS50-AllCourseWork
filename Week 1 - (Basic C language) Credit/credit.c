#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long cardNum=0;
    int length=0;


    do {
        cardNum = get_long("Enter Card Number: ");
    } while (cardNum<0);

    long visa=cardNum, amex=cardNum, master=cardNum;

    int pos1=0, pos2=0, pos3=0, pos4=0, pos5=0, pos6=0, pos7=0, pos8=0;
    int pos11=0, pos22=0, pos33=0, pos44=0, pos55=0, pos66=0, pos77=0, pos88=0;

    pos1 = ((cardNum%100)/10*2);
    pos2 = ((cardNum%10000)/1000*2);
    pos3 = ((cardNum%1000000)/100000*2);
    pos4 = ((cardNum%100000000)/10000000*2);
    pos5 = ((cardNum%10000000000)/1000000000*2);
    pos6 = ((cardNum%1000000000000)/100000000000*2);
    pos7 = ((cardNum%100000000000000)/10000000000000*2);
    pos8 = ((cardNum%10000000000000000)/1000000000000000*2);

    pos1 = ((pos1%100)/10) + (pos1%10);
    pos2 = ((pos2%100)/10) + (pos2%10);
    pos3 = ((pos3%100)/10) + (pos3%10);
    pos4 = ((pos4%100)/10) + (pos4%10);
    pos5 = ((pos5%100)/10) + (pos5%10);
    pos6 = ((pos6%100)/10) + (pos6%10);
    pos7 = ((pos7%100)/10) + (pos7%10);
    pos8 = ((pos8%100)/10) + (pos8%10);

    int sum1 =  pos1+pos2+pos3+pos4+pos5+pos6+pos7+pos8;
    pos11 = (cardNum%10);
    pos22 = ((cardNum%1000)/100);
    pos33 = ((cardNum%100000)/10000);
    pos44 = ((cardNum%10000000)/1000000);
    pos55 = ((cardNum%1000000000)/100000000);
    pos66 = ((cardNum%100000000000)/10000000000);
    pos77 = ((cardNum%10000000000000)/1000000000000);
    pos88 = ((cardNum%1000000000000000)/100000000000000);

    int sum2 =  pos11+pos22+pos33+pos44+pos55+pos66+pos77+pos88;
    int sum3 = sum1 + sum2;

    if ((sum3%10)!=0) {
        printf("%s\n", "INVALID");
        return 0;
    }

    while (cardNum >0){
        cardNum/=10;
        length++;
    }

    while (visa>=10) {
        visa /= 10;
        }

    if (visa == 4 && (length == 13 || length == 16)) {
        printf("%s\n", "VISA");
        return 0;
    }

    while (amex >= 10000000000000) {
        amex /= 10000000000000;
    }
    if (length == 15 && (amex == 34 || amex == 37)) {
        printf("%s\n", "AMEX");
        return 0;
    }

    while (master >= 100000000000000) {
        master /= 100000000000000;
    }
    if (length == 16 && (master == 51 || master == 52 || master == 53 || master == 54 || master == 55)) {
        printf("%s\n", "MASTERCARD");
        return 0;
    }
    else{
        printf("%s\n", "INVALID");
        return 0;
    }
}
