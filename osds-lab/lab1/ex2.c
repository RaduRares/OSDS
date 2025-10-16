#include <stdio.h>
#include <sys/mman.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h> 
#include <errno.h>

int main() {

	/* Open an executable file here */
	/* ... */
	int fd = open("./bin/foo.bin", O_RDONLY| O_CLOEXEC);

	long page = sysconf(_SC_PAGESIZE);
	int len = 74 ;// atat e functia din dummy
	size_t allocare= ((len + (size_t)page - 1) / (size_t)page) * (size_t)page; // pentru a face paginare

	void *ptr = mmap(NULL,allocare,PROT_READ | PROT_WRITE,MAP_PRIVATE | MAP_ANONYMOUS,-1,0);
	/* Fill in the details here! */
	
	size_t off = 0;
    while (off < len) {
        ssize_t r = read(fd, (char*)ptr + off, len - off);
        if (r < 0) {
            if (errno == EINTR) continue;
            perror("read");
            munmap(ptr, allocare);
            close(fd);
            return 1;
        }
        if (r == 0) break;
        off += (size_t)r;
    }
    if (off != len) {
        fprintf(stderr, "short read: got %zu expected %zu\n", off, len);
        munmap(ptr, allocare);
        close(fd);
        return 1;
    }

    printf("mapped at %p len=%zu alloc_len=%zu\n", ptr, len, allocare);
    fflush(stdout);

    if (mprotect(ptr, allocare, PROT_READ | PROT_EXEC) != 0) {
        perror("mprotect");
        munmap(ptr, allocare);
        close(fd);
        return 1;
    }

    close(fd);

    /* call the loaded code */
    ( (void(*)(void)) ptr )();

    munmap(ptr, allocare);
	/* Copy the bytes here */
	/* ... */

	/* This monster casts ptr to a function pointer with no args and calls it. Basically jumps to your code. */
	(*(void(*)()) ptr)();
}
