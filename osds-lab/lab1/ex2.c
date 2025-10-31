#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <unistd.h>

int main() {

	/* Open an executable file here */
	/* ... */
    FILE * f = fopen("./bin/dummy","rb");
    long offset = 0x1106; // pt ca e no-pie orice program incepe de la 4000 si am scazut adresa functiei - 0x4000 
    size_t size= 0x4A;//am avut o problema mare ca nu am luat si octetul de return si in loc de 74 am citit 73 de octeti
   //0x40114f - 0x401106 =  0x49 + 1 
    fseek(f,offset,SEEK_SET);
	/* Fill in the details here! */
	void *ptr = mmap(NULL,size, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_ANONYMOUS | MAP_PRIVATE,-1,0);
    fread(ptr,1,size,f);
    fclose(f);
	/* Copy the bytes here */
	/* ... */

	/* This monster casts ptr to a function pointer with no args and calls it. Basically jumps to your code. */
	(*(void(*)()) ptr)();
    munmap(ptr,size);
    return 0;
}