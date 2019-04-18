# Funzione che dato un numero, lo divide in parte pari e parte dispari
def numberDecomposition(n):
	decimal = False
	originalNumber = n
	count = 0
	div = 0
	
	while decimal == False:
		div = n / 2
		if div.is_integer():
			count = count + 1
			n = div
		else:
			decimal = True
	
	pari = 2 ** count
	dispari = originalNumber / pari
	return count, int(dispari)

def rabin(number):
	x = 2
	r, m = numberDecomposition(number - 1)
	
	print("r:" + str(r) + " m:" + str(m))
	sequence = []
	sequence.append((x ** m) % number)
	print(sequence[0])
	
	if (sequence[0] == 1):
		return False
	
	for i in range(1, r + 1):
		sequence.append((sequence[i - 1] ** 2) % number)
		print(sequence[i])
		
		if ((i < r) and sequence[i] == 1):
			return True
		
		if ((i < r) and (sequence[i]) == number - 1):
			return False
	
	return True

def main():
	rabin(41)

if __name__ == '__main__':
    main()