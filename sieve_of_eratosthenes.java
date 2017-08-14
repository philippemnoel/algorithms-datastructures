/*
 * sieve_of_eratosthenes.java
 *
 * Language: Java
 *
 * Program to print all primes smaller than or equal to a given number n using
 * Sieve of Eratosthenes
 */

import java.util.Scanner;

class Sieve_of_eratosthenes {
  void sieve_of_eratosthenes(int n) {
    // initialize boolean array with all entries as true
    // entries in primes will be false if not a prime, else true
    boolean primes[] = new boolean[n + 1];
    for (int i = 0; i < n; i++)
      primes[i] = true;

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
    for (int p = 2; p <= n; p++) {
      if (primes[p])
        System.out.print(p + " ");
    }
  }

  // helper function to filter for non-integer inputs
  static int filter_function(String str) throws Exception {
    int n = Integer.parseInt(str);
    if (n < 2)
      throw new Exception();
    return n;
  }

  public static void main(String args[]) {
    // initialize variable
    int n = 0;

    // prompt user for integer input >= 2
    Scanner scan = new Scanner(System.in);
    System.out.print("Enter a valid integer above 1: ");
    while (n < 2) {
      try {
        n = filter_function(scan.nextLine());
      } catch (Exception e) {
        System.out.print("Invalid input, please try again: ");
        n = 0;
      }
    }

    // output primes
    System.out.print("Following are the prime numbers ");
    System.out.println("smaller than or equal to " + n + ":");
    Sieve_of_eratosthenes g = new Sieve_of_eratosthenes();
    g.sieve_of_eratosthenes(n);
    System.out.println();
  }
}
