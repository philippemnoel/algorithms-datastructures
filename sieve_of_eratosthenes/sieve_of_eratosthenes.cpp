/*
 * sieve_of_eratosthenes.c
 *
 * Language: C++
 *
 * Program to print all primes smaller than or equal to a given number n using
 * Sieve of Eratosthenes.
 */

#include <bits/stdc++.h>

void sieve_of_eratosthenes(int n) {
  // initialize boolean array with all entries as true
  // entries in primes will be false if not a prime, else true
  bool primes[n + 1];
  memset(primes, true, sizeof(primes));

  // iterate over the array, checking for primes
  for (int p = 2; p * p <= n; p++) {
    // if primes[p] is true, then it is a prime
    if (primes[p]) {
      // update all multiples of p as not primes
      for (int i = p * 2; i <= n; i += p)
        primes[i] = false;
    }
  }

  // print all prime numbers for visual confirmation
  for (int p = 2; p <= n; p++)
    if (primes[p])
      std::cout << p << " ";
}

int main() {
  // initializing variables
  int n;
  std::string input;

  // prompt user for an integer >= 2
  std::cout << "Enter a valid integer above 1: ";
  while (getline(std::cin, input)) {
    std::stringstream ss(input);
    if (ss >> n) {
      if (ss.eof() && n > 1)
        break;
    }
    std::cout << "Invalid input, please try again." << std::endl;
  }

  // output primes
  std::cout << "Following are the prime numbers smaller than or equal to "
            << n << ":" << std::endl;
  sieve_of_eratosthenes(n);
  std::cout << std::endl;

  // render success
  return 0;
}
