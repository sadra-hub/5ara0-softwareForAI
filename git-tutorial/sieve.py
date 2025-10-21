# <ASSIGNMENT 1.5: Document the sieve method>
def sieve(upper_limit):
    primes = [True]*(upper_limit + 1)
    primes[0] = primes[1] = False

    for (i, isprime) in enumerate(primes):
        if isprime:
            last_prime = i
            for n in range(i**2, upper_limit + 1, i):
                primes[n] = False
    
    return last_prime


if __name__ == "__main__":
    upper_limit = input("Upper limit: ")
    print(f"Highest prime up to (and including) limit: {sieve(int(upper_limit))}")