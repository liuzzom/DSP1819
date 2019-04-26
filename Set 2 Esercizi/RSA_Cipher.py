# -*- coding: utf-8 -*-
import re
import random as rand
from string import ascii_lowercase
import math

alphabet = [letter for letter in ascii_lowercase]
alphabet.insert(0, ' ')

# Algoritmo di esponenziazione modulare veloce

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

# Calcolo dell'MCD tramite algoritmo di Euclide

def mcd(a, b):
  """Restituisce il Massimo Comune Divisore tra a e b
  :param a: primo numero
  :param b: secondo numero
  """
  while b:
  	a, b = b, a%b
  return a

# Calcolo dell'MCD e dei coefficienti dell'identità di Bezout tramite algoritmo di Eculide esteso

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

# Generazione dei numeri primi tramite Test di Miller-Rabin

def initialTest(number):
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
	:return: Genera un numero di k bit non divisibile per i primi 100 divisori banali
	"""
	# un numero di k bit è compreso tra 2^(k-1) e 2^k - 1
	number = 0

	while not initialTest(number):
		number = rand.getrandbits(k)
		# Si setta il MSB e il LSB a 1 e ci si assicura che il numero sia di k bit
		number |= (1 << (k-1)) | 1

		break

	# print("generated: " + str(number))
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
	# print("r: " + str(r) + " m: " + str(m))

	sequence = [exp(x, m, number)]
	# print(sequence[0])

	if sequence[0] == 1 or sequence[0] == (number - 1):
		return False

	for i in range(1, r + 1):
		sequence.append(exp(sequence[i - 1], 2, number))  # x[i] = x[i-1]^2 % n
		# print(sequence[i])

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

def generatePrime(bits, times=4):
	primeFlag = False

	while not primeFlag:
		number = numberGeneration(bits)
		primeFlag = isPrime(number, times)

	return number

# Encoding e Decoding di Messaggi

def encoding(char):
	"""
	:param char: Carattere da codificare
	:return: Stringa contenente le 2 cifre (con eventuale padding) della codifica del carattere in input
	"""
	encodedChar = alphabet.index(char) + 10

	return str(encodedChar)

def decoding(number):
	return alphabet[number - 10]

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

# Generazione Modulo RSA

def generateModule(k, times):
	"""
	:param k: dimensione in bit di p e q
	:param times: numero di esecuzioni del test di Miller-Rabin
	:return: modulo n = p * q, p, q
	"""
	if times == "":
		p = generatePrime(k)
		q = generatePrime(k)
		while p == q:
			q = generatePrime(k) # in modo che p e q non siano uguali

	else:
		p = generatePrime(k, int(times))
		q = generatePrime(k, int(times))
		while p == q:
			q = generatePrime(k, int(times))

	return p * q, p, q

# Generazione di e, d per la creazione delle chiavi

def getExponents(phi):
	e = rand.randrange(phi//2, phi-phi//4)
	while mcd(e, phi) != 1:
		e = rand.randrange(phi//2, phi-phi//4)

	x, y, gcd = extendedEuclideanAlg(phi, e)

	while y < 0:
		y += phi

	return e, y

# Preproccessing del testo

def textPreprocessing(text):
	""" Rimozione dei caratteri speciali e conversione in maiuscolo
		:param text: testo da preprocesssare
		"""

	text = text.lower()  # conversione in maiuscolo
	text = re.sub(r"['\",.;:_@#()”“’—?!&$\n]+\ *", " ", text)  # conversione dei caratteri speciali in uno spazio
	text = text.replace("-", "")  # conversione del carattere - in uno spazio
	text = ' '.join(text.split())
	return text

# Encryption

def encrypt(plaintext, publicKey):
	"""
	Encryption di un blocco di plaintext
	:param plaintext: blocco di plaintext
	:param publicKey: chiave pubblica
	:return: blocco di ciphertext
	"""
	e, n = publicKey

	return str(exp(int(plaintext), e, n))

# Decryption

def decrypt(ciphertext, privateKey):
	"""
	Decryption di un blocco di ciphertext
	:param ciphertext: blocco di ciphertext
	:param privateKey: chiave privata
	:return: blocco di plaintext
	"""
	d, n = privateKey
	plaintext = exp(int(ciphertext), d, n)

	return str(plaintext)

def CRTParamsCalc(ciphertext, privateKey, p, q):
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
		
	return mp, mq, pInv, qInv

def CRTDecrypt(privateKey, p, q, mp, mq, pInv, qInv):
	"""
	Decryption di un blocco fatto tramite il CRT
	:param ciphertext: blocco di ciphertext
	:param privateKey: chiave privata
	:param p: parte del modulo RSA n
	:param q: parte del modulo RSA n
	:return: blocco di plaintext
	"""
	d, n = privateKey

	# calcolo del plaintext
	m = (mp * q * qInv + mq * p * pInv) % n

	return str(m)

def getRandomPlaintext(length=20):
	return ''.join(rand.choice(alphabet) for i in range(length))

def main():
	print("Welcome!\n-----\n")

	# Generazione casuale di messaggi
	length = int(input("Insert message length: "))
	plaintexts = []
	for i in range(100):
		string = getRandomPlaintext(length)
		textPreprocessing(string)
		plaintexts.append(string)
	
	# Inserimento Parametri per la generazione del modulo
	k = int(input("Insert the value of k: "))
	times = input("Number of Miller-Rabin test execution (or enter for default value): ")
	print("message length: " + str(length))
	print("using " + str(k) + " bits for p and q")
	if times == "":
		print("Miller-Rabin test will be done 4 times")
	else:
		print("Miller-Rabin test will be done " + str(times) + " times")
	print("\n-----\n")
	
	# Generazione del modulo RSA
	n, p, q = generateModule(k, times)
	phi = (p - 1) * (q - 1)
	print("n:" + str(n))
	print("p:" + str(p))
	print("q:" + str(q))
	print("phi:" + str(phi))
	print("\n-----\n")
	
	
	if n <= int(stringEncoding(plaintexts[0])):
		print("ERROR: You have to use a bigger value for k")
		return
	
	# Generazione delle chiavi
	e, d = getExponents(phi)
	print("e:" + str(e))
	print("d:" + str(d))
	print("\n-----\n")
	
	publicKey = (e, n)
	privateKey = (d, n)

	# Encryption
	ciphertexts = []
	for plaintext in plaintexts:
		plaintext = stringEncoding(plaintext)
		ciphertexts.append(encrypt(plaintext, publicKey))
		
	# Decryption
	decryptionResults = []
	for ciphertext in ciphertexts:
		mp, mq, pInv, qInv = CRTParamsCalc(ciphertext, privateKey, p, q) # Precalcolo dei valori della formula CRT
		# decryptionResults.append(stringDeconding(decrypt(ciphertext, privateKey))) # Decryption Standard
		decryptionResults.append(stringDeconding(CRTDecrypt(privateKey, p, q, mp, mq, pInv, qInv))) # CRT Decryption

	for i in range(len(plaintexts)):
		if not plaintexts[i] == decryptionResults[i]:
			print("ERROR: Decryption Fail" + plaintexts[i] + " -> " + decryptionResults[i])
			return

	print("SUCCESS")

if __name__ == '__main__':
	main()
