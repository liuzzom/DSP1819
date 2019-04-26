# -*- coding: utf-8 -*
import random as rand

def exp(base, exponent, module):
	"""
	Calcolo del valore di (base^exponent) % module
	:param base:
	:param exponent:
	:param module:
	:return: d tale che d = (base^exponent) % module
	"""
	digits = bin(exponent) # rappresentazione binaria dell'esponente
	digits = digits[2:] # rimozione di "0b"

	d = 1

	for i in range(len(digits)):
		d = (d**2) % module

		if int(digits[i]) == 1:
			d = (d * base) % module

	return d

def initialTest(number):
	"""
	Verifica se il numero in input ha dei "divisori banali", in questo modo si cerca di effettuare meno volte il test di Miller-Rabin
	:param number:
	:return: False se il numero ha dei divisori banali, altrimenti True
	"""
	if number % 2 == 0:
		return False

	end = 100001
	if end > number:
		end = number

	for i in range(3, end, 2):
		if number % i == 0:
			return False

	return True

def numberGeneration(k):
	"""
	Genera un numero potenzialmente primo di k bit
	:param k: numero di bit del numero da generare
	:return: Genera un numero di k bit non divisibile per 1 < x < 100001
	"""
	# un numero di k bit è compreso tra 2^(k-1) e 2^k - 1
	number = 0

	while not initialTest(number):
		number = rand.getrandbits(k)
		# Si setta il MSB e il LSB a 1 e ci si assicura che il numero sia di k bit
		number |= (1 << (k-1)) | 1

		break

	print("generated: " + str(number))
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

	while number % 2 == 0:
		number = number // 2
		count = count + 1

	return count, number


def rabin(number):
	"""
	Esegue il test di Miller-Rabin. Se esso restituisce True, il numero è sicuramente composto, altrimenti potrebbe essere primo
	:param number:
	:return: True, se il numero è composto; False se il numero è probabilmente primo
	"""
	x = 2
	r, m = numberDecomposition(number - 1)
	print("r: " + str(r) + " m: " + str(m))

	sequence = [exp(x, m, number)]
	print(sequence[0])

	if sequence[0] == 1 or sequence[0] == (number - 1):
		return False

	for i in range(1, r + 1):
		sequence.append(exp(sequence[i - 1], 2, number))  # x[i] = x[i-1]^2 % n
		print(sequence[i])

		if (i < r) and sequence[i] == 1:
			return True

		if (i < r) and (sequence[i]) == (number - 1):
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

	# k = int(input("Insert the value of k: "))
	# times = input("Number of MillerRabin test execution (or enter for default value): ")

	k = 100
	times = 4

	if times == "":
		number = generatePrime(k)
		print("The generated number " + str(number) + " is prime")
	else:
		number = generatePrime(k, int(times))
		print("The generated number " + str(number) + " is prime")

if __name__ == '__main__':
    main()
