/*
 * sieve_of_eratosthenes.c
 *
 * Language: C
 *
 * Program to print all primes smaller than or equal to a given number n using
 * Sieve of Eratosthenes
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void sieve_of_eratosthenes(int n) {
  // initialize boolean array with all entries as 1 (true)
  // entries in primes will be 0 (false) if not a prime, else true
  int primes[n + 1];
  memset(primes, 1, sizeof(primes));

  // iterate over the array, checking for primes
  for (int p = 2; p * p <= n; p++) {
    // if primes[p] is true, then it is a prime
    if (primes[p]) {
      // update all multiples of p as not primes
      for (int i = p * 2; i <= n; i += p)
        primes[i] = 0;
    }
  }

  // print all prime numbers for visual confirmation
  for (int p = 2; p <= n; p++) {
     if (primes[p])
       printf("%d ", p);
  }
  printf("\n");
}

// helper function to filter for non-integer inputs bigger than 1
int int_only(char line[]) {
  // calculating true input length
  int length = strlen(line) - 1;

  // filters for empty input or int smaller than 2
  if (length == 0 || atoi(line) < 2) {
    printf("Invalid input, please try again: ");
    return 0;
  }

  // check for non-digit character
  for (int i = 0; i < length; i++) {
    // input is not an int
    if (line[i] < '0' || line[i] > '9') {
      printf("Invalid input, please try again: ");
      return 0;
    }
  }

  // input is an int
  return 1;
}

int main() {
  // prompt user for integer input
  char line[4096];
  printf("Enter a valid integer above 1: ");
  do {
    fgets(line, sizeof(line), stdin);
  } while (int_only(line) == 0);

  // correct input received, formatting to int
  int n = atoi(line);

  // output primes
  printf("Following are the prime numbers smaller than or equal to %d:\n", n);
  sieve_of_eratosthenes(n);

  // render success
  return 0;
}
