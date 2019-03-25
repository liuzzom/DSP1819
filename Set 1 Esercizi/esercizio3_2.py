import numpy as np
import math
import random
from string import ascii_uppercase
import re


# lista contenente le lettere in maiuscolo.
alphabet = [letter for letter in ascii_uppercase]

# Preproccessing del testo

def stringToNumpyArray(string):
	""" Converte una stringa in un array numpy contenente i numeri relativi alle varie lettere
	:param string: stringa da convertire
	"""
	letters = [alphabet.index(letter) for letter in string] # conversione da lettere a numeri
	letters = np.array(letters)
	return letters

def numpyArrayToString(array):
	""" Converte un array numpy in una stringa di testo
	:param array: array da convertire
	"""

	letters = array.tolist()
	letters = [alphabet[i] for i in letters] # conversione da numeri a lettere
	text = "".join(letters) # creazione stringa unica
	return text

def preprocessing(text):
	""" Rimozione dei caratteri speciali e conversione in maiuscolo
	:param text: testo da preprocesssare
	"""

	text = text.upper() # conversione in maiuscolo
	text = re.sub(r"['\",.;:_@#()”“’—?!&$\n]+\ *", " ", text) # conversione dei caratteri speciali in uno spazio
	text = text.replace("-", "") # conversione del carattere - in uno spazio
	text = text.replace(" ", "") # rimozione spazi
	return text

# Generazione della chiave
def mcd(a, b):
  """Restituisce il Massimo Comune Divisore tra a e b
  :param a: primo numero
  :param b: secondo numero
  """
  while b:
  	a, b = b, a%b
  return a

def getKey(blockDim):
	""" Creazione della chiave
	:param blockDim: dimensione m della matrice mxm
	:return: una matrice mxm invertibile
	"""
	det = 0
	while det <= 0 or (mcd(det, len(alphabet)) != 1):
		key = np.random.randint(26, size=(blockDim, blockDim))
		det = np.linalg.det(key)

	return key

# Encryption del Plaintext

def getBlocks(textArray, blockDim):
	""" Suddivisione del testo, già codificato, in blocchi di dimensione m. Se necessario, vengono aggiunte delle A di padding
	:param textArray: testo sotto forma di array numpy
	:param blockDim: dimensione dei blocchi
	:return: array numpy di blocchi
	"""
	# aggiunta di padding nel caso sia necessario
	paddingElementsNeeded = math.ceil(textArray.size/blockDim) * blockDim - textArray.size
	for i in range(paddingElementsNeeded):
		textArray = np.append(textArray, 0)

	blocks = []
	while textArray.size > 0:
		blocks.append(textArray[:blockDim]) # inserisce un blocco
		textArray = textArray[blockDim:] # accorcia l'array di un blocco

	return np.array(blocks)

def rowVectToColVect(rowVect):
	""" Conversione di un vettore riga in un vettore colonna
	:param rowVect: vettore riga da convertire
	:return: vettore colonna
	"""
	colVect = []
	for i in range(rowVect.size):
		colVect.append([rowVect[i]])
	return np.array(colVect)

def dotModN(a, b, n):
	""" Prodotto modulo n tra due matrici a e b
	:param a:
	:param b:
	:param n:
	"""
	result = np.dot(a, b) # prodotto tra le due matrici
	for i in range(np.size(result, 0)):
		for j in range(np.size(result, 1)):
			result[i][j] %= n

	return result

def encrypt(text, key):
	""" Encryption del messaggio
	:param text: testo da cifrare
	:param key: chiave
	:return: testo cifrato sotto forma di stringa
	"""
	textArray = stringToNumpyArray(text)
	ciphertext = []

	blocks = getBlocks(textArray, np.size(key, 0))

	for i in range(np.size(blocks, 0)):
		c_i = rowVectToColVect(blocks[i])
		c_i = dotModN(key, c_i, len(alphabet)) # calcolo delll'i-esimo bocco di ciphertext
		c_i = c_i.flatten()
		for letter in c_i:
			ciphertext.append(letter)

	return numpyArrayToString(np.array(ciphertext))

# Decryption del messaggio

def invModN(num, n):
	""" Inverso moltiplicativo modulo n di num
	"""
	if num == 0:
		return None
	inv = 1
	while inv < max(num, n):
		if (num*inv)%n == 1:
			return inv
		inv += 1
	return None


def minor(arr, i, j):
	"""Sottomatrice di matrix, ottenuta rimuovendo la riga i e la colonna j"""
	return arr[np.array(list(range(i)) + list(range(i + 1, arr.shape[0])))[:, np.newaxis], np.array(list(range(j)) + list(range(j + 1, arr.shape[1])))]

def invMatModN(matrix, n):
	invDet = invModN(round(np.linalg.det(matrix)), 26)
	result = np.zeros(shape=(np.size(matrix, 0), np.size(matrix, 1)), dtype=int)

	for i in range(np.size(matrix, 0)):
		for j in range(np.size(matrix, 1)):
			result[i][j] = ((-1)**((i+1)+(j+1)) * round(np.linalg.det(minor(matrix, j, i))) * invDet) % n

	return np.array(result)


def decrypt(ciphertext, key):
	""" Decryption di un ciphertext data una key
	:param ciphertext:
	:param key:
	:return: una stringa di testo
	"""
	ciphertextArray = stringToNumpyArray(ciphertext)
	plaintext = []

	blocks = getBlocks(ciphertextArray, np.size(key, 0))
	inverseKey = invMatModN(key, 26)

	for i in range(np.size(blocks, 0)):
		p_i = rowVectToColVect(blocks[i])
		p_i = dotModN(inverseKey, p_i, len(alphabet)) # calcolo delll'i-esimo bocco di ciphertext
		p_i = p_i.flatten()
		# creazione di una lista contenente le lettere (codificate in numeri)
		for letter in p_i:
			plaintext.append(letter)

	return numpyArrayToString(np.array(plaintext))

# Attacco Known-Plaintext

def getPStarAndCStar(PTblocks, CTblocks, n):
	""" Genera due matrici P* e C* (in relazione a P*), di dimensione nxn in modo tale che P* sia invertibile modulo 26
	"""
	pStar = np.zeros(shape=(n, n), dtype=int)
	cStar = np.zeros(shape=(n, n), dtype=int)
	index = 0
	det = 0

	"""
	Si generano matrici fino a quando si ottiene una matrice P* nxn invertibile.
	P* è invertibile se il suo determinante è positivo e se esso è coprimo con 26
	"""
	while det <= 0 or (mcd(det, len(alphabet)) != 1):
		"""
		Genera n numeri random su cui prendere i blocchi
		l'ultimo blocco è volutamente escluso, dato che protrebbe contenere caratteri di padding
		"""
		chosenBlocks = random.sample(range(np.size(PTblocks, 0)), n)
		chosenBlocks.sort()
		for i in chosenBlocks:
			pStar[index] = PTblocks[i]
			cStar[index] = CTblocks[i]
			index += 1
		pStar = pStar.transpose()
		cStar = cStar.transpose()
		det = round(np.linalg.det(pStar)) # calcolo del determinante
		index = 0
	return (pStar, cStar)

def attack(plaintext, ciphertext, blockDim):
	plaintextArray = stringToNumpyArray(plaintext)
	plaintextBlocks = getBlocks(plaintextArray, blockDim)
	ciphertextArray = stringToNumpyArray(ciphertext)
	ciphertextBlocks = getBlocks(ciphertextArray, blockDim)

	pStar, cStar = getPStarAndCStar(plaintextBlocks, ciphertextBlocks , blockDim)
	"""
	La chiave K è data da: K = C* x P*^-1
	Si calcola prima l'inverso modulo 26 della matrice P* e successivamente si calcola il prodotto
	"""
	inversePStar = invMatModN(pStar, 26)
	key = dotModN(cStar, inversePStar, 26)

	return key

def main():
	textFile = open("./Sound_of_Silence_Lyrics.txt")
	text = textFile.read()
	text = preprocessing(text)
	print("Plaintext\n-----\n" + text + "\n-----\n")

	blockDim = int(input("Insert k value: "))
	key = getKey(blockDim)
	print("Key\n-----\n" + str(key) + "\n-----\n")

	ciphertext = encrypt(text, key)
	print("Ciphertext\n-----\n" + ciphertext + "\n-----\n")

	plaintext = decrypt(ciphertext, key)
	print("Plaintext\n-----\n" + plaintext + "\n-----\n")

	newKey = attack(plaintext, ciphertext, blockDim)

	if(np.array_equal(key, newKey)):
		print("Key Found\n-----")
		print("Key\n-----\n" + str(newKey) + "\n-----\n")

if __name__ == '__main__':
    main()