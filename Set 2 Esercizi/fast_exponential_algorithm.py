def exp(base, exponent, module):
	digits = bin(exponent)
	digits = digits[2:]

	d = 1

	for i in range(len(digits)):
		d = (d**2) % module

		if int(digits[i]) == 1:
			d = (d * base) % module

	return d


def main():
	a = 3
	m = 11
	n = 10
	result = exp(a, m, n)
	print(result)

if __name__ == '__main__':
	main()