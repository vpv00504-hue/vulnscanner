#include <stdio.h>
#include <string.h>

int main() {
    char buf[20];

    printf("Enter your name: ");

    // ✅ Safe input (limits size)
    if (fgets(buf, sizeof(buf), stdin) != NULL) {

        // Remove newline character safely
        buf[strcspn(buf, "\n")] = '\0';

        printf("Hello, %s\n", buf);
    } else {
        printf("Input error!\n");
    }

    return 0;
}