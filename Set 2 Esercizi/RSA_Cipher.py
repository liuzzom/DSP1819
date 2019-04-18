# -*- coding: utf-8 -*-
import numpy as np

def numberGeneration(k):
	min = 2 ** (k-1)
	max = (2 ** k) - 1
	number = 0
	
	while number % 2 == 0 or number % 3 == 0 or number % 5 == 0:
		number = np.random.randint(min, max+1)
	
	print("generated " + str(number))
	return number

# Funzione che dato un numero, lo divide in parte pari e parte dispari
def numberDecomposition(n):
	decimal = False
	originalNumber = n
	count = 0
	div = 0
	
	while decimal == False:
		div = n/2
		if div.is_integer():
			count = count + 1
			n = div
		else:
			decimal = True
	
	pari = 2**count
	dispari = originalNumber/pari
	return count,int(dispari)

def rabin(number):
	x = 2
	r , m = numberDecomposition(number - 1)
	
	print("r:" + str(r) + " m:" + str(m))
	sequence = []
	sequence.append((x ** m) % number)
	print(sequence[0])
	
	if(sequence[0] == 1):
		return False
	
	for i in range(1, r + 1):
		sequence.append((sequence[i - 1] ** 2) % number)
		print(sequence[i])
		
		if((i < r) and sequence[i] == 1):
			return True
		
		if((i < r) and (sequence[i]) == number - 1 ):
			return False
	
	return True

def isPrime(number,times):
	for i in range(times):
		if rabin(number) == True:
			return False
	
	return True

def generatePrime(bits, times=2):
	primeFlag = False
	
	while primeFlag == False:
		number = numberGeneration(bits)
		primeFlag = isPrime(number,times)
	
	return number

def asciiEncoding(char):
	encodedChar = ord(char)
	
	if encodedChar < 10:
		encodedChar = "00" + str(encodedChar)
		return encodedChar
	
	if encodedChar < 100:
		encodedChar = "0" + str(encodedChar)
		return encodedChar
	
	return str(encodedChar)

def asciiDecoding(number):
	return chr(number)

def main():

	k = int(input("Insert the value of k: "))
	times = input("Number of MillerRabin test execution (or enter for default value): ")
	
	if times == "":
		number = generatePrime(k)
		print("The generated number " + str(number) + " is prime")
	else:
		number = generatePrime(k, int(times))
		print("The generated number " + str(number) + " is prime")
	
	test = "striga di test"
	encoding = ""
	decoding = ""
	
	for i in range(len(test)):
		encoding = encoding + asciiEncoding(test[i])
	
	for i in range(0, len(encoding), 3):
		decoding += asciiDecoding(int(encoding[i:i+3]))
	
	print(test)
	print(encoding)
	print(decoding)

if __name__ == '__main__':
	main()

