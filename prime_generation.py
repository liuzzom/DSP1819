# -*- coding: utf-8 -*-
import numpy as np


def numberGeneration(k):
	"""
	Genera un numero potenzialmente primo di k bit
	:param k: numero di bit del numero da generare
	:return: Genera un numero di k bit non divisibile per 2, 3 e 5
	"""
	# un numero di k bit è compreso tra 2^(k-1) e 2^k - 1
	min = 2 ** (k - 1)
	max = (2 ** k) - 1
	number = 0
	
	while number % 2 == 0 or number % 3 == 0 or number % 5 == 0:
		number = np.random.randint(min, max + 1)
	
	print("generated " + str(number))
	return number


def numberDecomposition(n):
	"""
	Decomposizione di un numero in forma 2^r * m
	:param n:
	:return: r, m tali che n = 2^r * m
	"""
	originalNumber = n
	count = 0
	number = n
	
	while True:
		number = number / 2
		if number.is_integer():
			count = count + 1
		else:
			break
	
	pari = 2 ** count
	dispari = originalNumber / pari
	return count, int(dispari)


def rabin(number):
	"""
	Esegue il test di Miller-Rabin. Se esso restituisce True, il numero è sicuramente composto, altrimenti potrebbe essere primo
	:param number:
	:return: True, se il numero è composto; False se il numero è probabilmente positivo
	"""
	x = 2
	r, m = numberDecomposition(number - 1)
	print("r:" + str(r) + " m:" + str(m))
	
	sequence = [(x ** m) % number]
	print(sequence[0])
	
	if sequence[0] == 1:
		return False
	
	for i in range(1, r + 1):
		sequence.append((sequence[i - 1] ** 2) % number)  # x[i] = x[i-1]^2 % n
		print(sequence[i])
		
		if (i < r) and sequence[i] == 1:
			return True
		
		if (i < r) and (sequence[i]) == number - 1:
			return False
	
	return True


def isPrime(number, times):
	"""
	:param number: Numero da testare
	:param times: Numero di verifiche tramite test di Miller-Rabin
	:return:
	"""
	for i in range(times):
		if rabin(number):
			return False
	
	return True


def generatePrime(bits, times=2):
	primeFlag = False
	
	while not primeFlag:
		number = numberGeneration(bits)
		primeFlag = isPrime(number, times)
	
	return number

def main():
	
	k = int(input("Insert the value of k: "))
	times = input("Number of MillerRabin test execution (or enter for default value): ")

	if times == "":
		number = generatePrime(k)
		print("The generated number " + str(number) + " is prime")
	else:
		number = generatePrime(k, int(times))
		print("The generated number " + str(number) + " is prime")
	
	
if __name__ == '__main__':
    main()