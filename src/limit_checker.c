#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    if (argc != 4) {
        fprintf(stderr, "usage: %s <value> <lower> <upper>\n", argv[0]);
        return 1;
    }

    int value = atoi(argv[1]);
    int lower = atoi(argv[2]);
    int upper = atoi(argv[3]);

    if (value < lower) {
        printf("LOW\n");
        return 2;
    }

    if (value > upper) {
        printf("HIGH\n");
        return 3;
    }

    printf("OK\n");
    return 0;
}
