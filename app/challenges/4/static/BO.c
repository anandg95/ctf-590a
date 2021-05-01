#include <stdio.h>
#include <string.h>

int main(void)
{
    char buff[15];
    int pass = 0;
    gets(buff);
    
    /*
    if(strcmp(buff, "the_real_passcode"))
    {
        pass = 121
    }
    */

    if(pass == 121)
    {
        system("cat flag.txt");
    }
    else
    {
        printf("Incorrect!");
    }
    return 0;
}