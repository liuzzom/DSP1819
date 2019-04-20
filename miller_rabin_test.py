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
		sequence.append((sequence[i - 1] ** 2) % number) # x[i] = x[i-1]^2 % n
		print(sequence[i])
		
		if (i < r) and sequence[i] == 1:
			return True
		
		if (i < r) and (sequence[i]) == number - 1:
			return False
	
	return True


def main():
	rabin(41)


if __name__ == '__main__':
	main()
