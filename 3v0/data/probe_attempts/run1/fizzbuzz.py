import sys
def main():
    if len(sys.argv) < 2:
        print("usage: fizzbuzz.py N"); sys.exit(1)
    n = int(sys.argv[1])
    for i in range(1, n + 1):
        if i % 15 == 0: print("FizzBuzz")
        elif i % 3 == 0: print("Fizz")
        elif i % 5 == 0: print("Buzz")
        else: print(i)
main()
