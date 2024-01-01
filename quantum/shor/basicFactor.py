# Import necessary libraries
import streamlit as st
from sympy import nextprime

# Function to find prime factors
def prime_factors(n):
    factors = []
    # Check for even factors
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    # Check for odd factors
    for i in range(3, int(n**0.5) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n //= i
    # If n becomes a prime number > 2
    if n > 2:
        factors.append(n)
    return factors

# Function to generate prime numbers close to n
def generate_primes(n):
    primes = [nextprime(n), nextprime(n, 2)]
    return primes

# Streamlit app
st.title("Prime Factorization and Generation")

# Number input
number = st.number_input("Enter a number", min_value=2, step=1, format='%d')

# Button to start factorization
if st.button("Find Prime Factors"):
    factors = prime_factors(number)
    st.write("Prime factors of", number, "are:", factors)

# Button to generate primes and composite
if st.button("Generate Primes and Composite"):
    primes = generate_primes(number)
    composite = primes[0] * primes[1]
    st.write("Primes close to", number, "are:", primes)
    st.write("Composite of the primes is:", composite)