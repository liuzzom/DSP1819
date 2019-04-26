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
	print("X[0]: " + str(sequence[0]))

	if sequence[0] == 1 or sequence[0] == (number - 1):
		return False

	for i in range(1, r + 1):
		sequence.append(exp(sequence[i - 1], 2, number))  # x[i] = x[i-1]^2 % n
		print("X[" + str(i) + "]: " + str(sequence[i]))

		if (i < r) and sequence[i] == 1:
			return True

		if (i < r) and (sequence[i]) == (number - 1):
			return False

	return True

def main():
	# n = 48112959837082048697
	n = 41
	print(rabin(n))


if __name__ == '__main__':
	main()
