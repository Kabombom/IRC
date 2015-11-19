#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int main(int argc, char *argv[]) {
    printf("Hello!\n");
    if (fork() == 0) {
        printf("I am your son and my PID is %d\n", getpid());
    }
    else {
        printf("Luke,\nI am your father and my PID is  %d\n", getpid());
    }
    return 0;
}
