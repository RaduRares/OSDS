#include <stdio.h>
#include <stdlib.h>

// Nu includem string.h dar vom apela strcpy!
int main() {
    char buffer[100];
    char source[] = "Hacked via GOT!";
    
    printf("Before: %s\n", buffer);
    
    // strcpy nu este apelat în cod, dar îl vom apela!
    printf("GOT entry for printf: %p\n", &printf);
    
    return 0;
}