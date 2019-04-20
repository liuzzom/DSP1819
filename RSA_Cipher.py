# -*- coding: utf-8 -*-
import re
import numpy.random as rand
from string import ascii_lowercase
import math

alphabet = [letter for letter in ascii_lowercase]
alphabet.insert(0, ' ')

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

def mcd(a, b):
  """Restituisce il Massimo Comune Divisore tra a e b
  :param a: primo numero
  :param b: secondo numero
  """
  while b:
  	a, b = b, a%b
  return a

def extendedEuclideanAlg(a, b):
	"""
	Calcolo dei coefficienti x e y dell'identità di Bezout e del MCD
	:param a:
	:param b:
	:return: x, y e d tali che MCD(a, b) = d = ax + by
	"""
	x0, x1, y0, y1 = 0, 1, 1, 0
	while a != 0:
		q, b, a = b // a, a, b % a
		y0, y1 = y1, y0 - q * y1
		x0, x1 = x1, x0 - q * x1
	return x0, y0, b

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
		number = rand.randint(min, max + 1)
	
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
	
	sequence = [(x ** m) % number]
	
	if sequence[0] == 1:
		return False
	
	for i in range(1, r + 1):
		sequence.append((sequence[i - 1] ** 2) % number)  # x[i] = x[i-1]^2 % n
		
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


def encoding(char):
	"""
	:param char: Carattere da codificare
	:return: Stringa contenente le 2 cifre (con eventuale padding) della codifica del carattere in input
	"""
	encodedChar = alphabet.index(char)
	
	if encodedChar < 10:
		encodedChar = "0" + str(encodedChar)
		return encodedChar
	
	return str(encodedChar)

def decoding(number):
	return alphabet[number]

def stringEncoding(string):
	encoded = ""
	
	for i in range(len(string)):
		encoded += encoding(string[i])
	
	return encoded

def stringDeconding(string):
	decoded = ""
	
	for i in range(0, len(string), 2):
		decoded += decoding(int(string[i:i + 2]))
		
	return decoded

def generateModule(k, times):
	"""
	:param k: dimensione in bit di p e q
	:param times: numero di test di Miller-Rabin da fare
	:return: modulo n = p * q, p, q
	"""
	if times == "":
		p = generatePrime(k)
		q = generatePrime(k)
		while p == q:
			q = generatePrime(k)
			
	else:
		p = generatePrime(k, int(times))
		q = generatePrime(k, int(times))
		while p == q:
			q = generatePrime(k, int(times))
		
	return p * q, p, q

def getExponents(phi):
	e = rand.randint(low=phi//2, high=phi-phi//4)
	while mcd(e, phi) != 1:
		e = rand.randint(low=phi//2, high=phi-phi//4)
	
	x, y, gcd = extendedEuclideanAlg(phi, e)
	
	while y < 0:
		y += phi
	
	return e, y

def textPreprocessing(text):
	""" Rimozione dei caratteri speciali e conversione in maiuscolo
		:param text: testo da preprocesssare
		"""
	
	text = text.lower()  # conversione in maiuscolo
	text = re.sub(r"['\",.;:_@#()”“’—?!&$\n]+\ *", " ", text)  # conversione dei caratteri speciali in uno spazio
	text = text.replace("-", "")  # conversione del carattere - in uno spazio
	text = ' '.join(text.split())
	return text

def getBlocks(text, blockSize):
	"""
	Divisione del testo in blocchi per l'encryption
	:param text: testo da suddividere
	:param blockSize: dimensione dei blocchi
	:return: array contenente i blocchi
	"""
	# aggiunta di padding nel caso sia necessario
	paddingElementsNeeded = math.ceil(len(text) / blockSize) * blockSize - len(text)
	for i in range(paddingElementsNeeded):
		text = text + '0' # come carattere di padding viene utilizzato lo spazio

	blocks = []
	while len(text) > 0:
		blocks.append(text[:blockSize]) # inserisce un blocco
		text = text[blockSize:] # accorcia l'array di un blocco
		
	return blocks

def encrypt(plaintext, publicKey):
	"""
	Encryption di un blocco di plaintext
	:param plaintext: blocco di plaintext
	:param publicKey: chiave pubblica
	:return: blocco di ciphertext
	"""
	e, n = publicKey
	
	return str(exp(int(plaintext), e, n))

def decrypt(ciphertext, privateKey):
	"""
	Decryption di un blocco di ciphertext
	:param ciphertext: blocco di ciphertext
	:param privateKey: chiave privata
	:return: blocco di plaintext
	"""
	d, n = privateKey
	
	plaintext = exp(int(ciphertext), d, n)
	
	print(plaintext)
	
	
	# inserimento di leading zero se persi durante l'elevamento a potenza
	while len(str(plaintext)) < (len(str(n)) - 1):
		plaintext = '0' + str(plaintext)
	
	return str(plaintext)

def CRTDecrypt(ciphertext, privateKey, p, q):
	"""
	Decryption di un blocco fatto tramite il CRT
	:param ciphertext: blocco di ciphertext
	:param privateKey: chiave privata
	:param p: parte del modulo RSA n
	:param q: parte del modulo RSA n
	:return: blocco di plaintext
	"""
	d, n = privateKey
	
	mp = exp(int(ciphertext), d, p)
	mq = exp(int(ciphertext), d, q)
	
	# calcolo degli inversi tramite algoritmo di euclide esteso
	pInv, qInv, _ = extendedEuclideanAlg(p, q)
	
	# conversione degli inversi in numeri positivi
	while pInv < 0:
		pInv += q
	
	while qInv < 0:
		qInv += p
		
	# calcolo del plaintext
	m = (mp * q * qInv + mq * p * pInv) % n
	
	
	# inserimento di leading zero se persi durante l'elevamento a potenza
	while len(str(m)) < (len(str(n)) - 1):
		m = '0' + str(m)
	
	return str(m)

def main():
	print("Welcome!\n-----\n")
	
	plaintext = input("Insert the string to encrypt: ")
	k = int(input("Insert the value of k: "))
	times = input("Number of Miller-Rabin test execution (or enter for default value): ")
	print("\n-----\n")
	
	# Plaintext Preprocessing
	plaintext = textPreprocessing(plaintext)
	print("plaintext: " + plaintext)
	print("using " + str(k) + " bits for p and q")
	print("Miller-Rabin test done " + str(times) + " times\n-----\n")

	# Generazione del modulo RSA
	n, p, q = generateModule(k, times)
	phi = (p - 1) * (q - 1)
	print("n:" + str(n))
	print("p:" + str(p))
	print("q:" + str(q))
	print("phi:" + str(phi))
	print("\n-----\n")
	
	# Generazione delle chiavi
	e, d = getExponents(phi)
	print("e:"+ str(e))
	print("d:" + str(d))
	print("\n-----\n")
	
	publicKey = (e, n)
	privateKey = (d, n)
	
	# Codifica del plaintext e divisione in blocchi. In questo modo è possibile utilizzare un n "non abbastanza grande"
	encodedPlaintext = stringEncoding(plaintext)
	blockSize = len(str(n)) - 1
	plainBlocks = getBlocks(encodedPlaintext, blockSize)
	cipherBlocks = []
	
	# encryption
	for block in plainBlocks:
		cipherBlocks.append(encrypt(block, publicKey))
	
	print(encodedPlaintext)
	print(plainBlocks)
	print(cipherBlocks)
	print("\n-----\n")
	
	# decryption tramite approccio tradizionale
	testBlocks = []
	for block in cipherBlocks:
		testBlocks.append(decrypt(block, privateKey))
	
	testString = ''.join(testBlocks)
	print(testBlocks)
	print(testString)
	print("decrypted plaintext using normal decryption:" + stringDeconding(testString))
	print("\n-----\n")
	
	# decryption tramite
	testBlocks = []
	for block in cipherBlocks:
		testBlocks.append(CRTDecrypt(block, privateKey, p, q))
	
	testString = ''.join(testBlocks)
	print("decrypted plaintext using CRT speedup:" + stringDeconding(testString))
	print("\n-----\n")


if __name__ == '__main__':
	main()

