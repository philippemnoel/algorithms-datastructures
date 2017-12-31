#include <stdio.h>
#include <stdlib.h>

int factorial(int n) {
  if (n < 1) {
    printf("%i\n", 1);
    return 1;
  }
  else {
    printf("%i\n", n);
    return n * factorial(n - 1);
  }
}

int main() {
  printf("%i\n", factorial(6));
  return 0;
}
