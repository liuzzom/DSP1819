import math
from string import ascii_lowercase
import numpy as np

alphabet = [letter for letter in ascii_lowercase]

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

def getSubstrings(text, m):
	""" Divide il testo in sottostringhe, ognuna di dimensione ceil(len(text)/m))
	Il testo viene diviso scrivendo "per colonne"
	:param text: testo da suddividere
	:param m: numero di righe in cui suddividere il testo
	:return: lista di sottostringhe scritte per colonna
	"""
	substrings = []

	for i in range(m):
		substrings.append("")

	index = 0
	for letter in text:
		substrings[index] = substrings[index] + letter
		index = (index + 1) % m

	return substrings

def computeLetterFrequencies(string):
	""" Calcola la frequenza delle varie lettere in una stringa. L'algoritmo è piuttosto primitivo
	:param string:
	:return: lista delle frequenze delle varie lettere
	"""
	frequencies = []

	for letter in alphabet:
		count = 0
		for i in string:
			if i == letter:
				count += 1
		frequencies.append(count)

	return frequencies

def coincidenceIndex(string, n):
	""" Calcola l'indice di coincidenza di una stringa di dimensione n
	:return: indice di coincidenza della stringa
	"""
	frequencies = computeLetterFrequencies(string)
	ic = 0

	for frequency in frequencies:
		ic += (frequency*(frequency-1)) / (n*(n-1))

	return ic

def coincidenceIndexTest(ciphertext, m):
	""" Test Sull'indice di coincidenza delle righe ottenute suddividendo :param text in :param m blocchi
	Se necessario, si utilizzano delle "a" di padding in modo che le sottotringhe abbiano tutte la stessa dimensione
	:return Sottostringhe del testo su cui fare future analisi
	"""
	text = ciphertext
	# calcola se serve fare padding
	padding = math.ceil(len(text)/m)*m - len(text)

	# aggiunge delle "a" di padding, se necessario
	if padding:
		for i in range(padding):
			text = text + "a"

	substrings = getSubstrings(text, m)
	coincidenceIndexes = []

	for i in range(len(substrings)):
		coincidenceIndexes.append(coincidenceIndex(substrings[i], len(text)/m))

	print(coincidenceIndexes)
	return substrings

def shiftEncryption(string, k):
	""" Shift Encryption di :param string di :param k.
	:return: Stringa dove ogni lettera subisce uno shift di k posizioni
	"""
	stringArray = stringToNumpyArray(string)
	shiftedStringArray = [None] * len(stringArray)

	for i in range(len(stringArray)):
		shiftedStringArray[i] = (stringArray[i] + k) % 26

	shiftedString = numpyArrayToString(np.array(shiftedStringArray))
	return shiftedString

def findKeyElement(substring):
	"""
	Prende in input la stringa :param substring, su cui si suppone che sia risultato di uno shift encryption di paramentro k
	Si cerca quel valore k che massimizza il prodotto scalare tra il vettore frequenze della stringa risultato di uno shift encryption k e il vettore delle frequenze delle lettere della lingua inglese
	:return: i-esima lettera della chiave di encryption
	"""
	# frequenze delle lettere nella lingua inglese
	en_lett_freqs = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702,
									 0.02228, 0.02015, 0.06094, 0.06966, 0.00153,
									 0.00772, 0.04025, 0.02406, 0.06749, 0.07507,
									 0.01929, 0.00095, 0.05987, 0.06327, 0.09056,
									 0.02758, 0.00978, 0.02360, 0.00150, 0.01974, 0.00074]

	maxDotProd = 0
	maxKey = None

	for letter in alphabet:
		letterValue = alphabet.index(letter)
		shiftedSubString = shiftEncryption(substring, letterValue) # shift encryption basato sull' i-esima lettera dell'alfabeto
		dotProd = np.dot(computeLetterFrequencies(shiftedSubString), en_lett_freqs) # calcolo del prodotto scalare
		if dotProd > maxDotProd:
			maxDotProd = dotProd
			maxKey = letter

	return maxKey

def findKey(subStrings):
	""" Date delle :param subStrings, su cui si suppone che ogni strnga sia frutto di uno shift encryption,
	:return: la chiave contenente le componenti utilizzate per cifrare il messaggiRs
	"""
	key = ""

	for i in range(len(subStrings)):
		key = key + str(findKeyElement(subStrings[i]))

	return key

def main():
	ciphertext = "kbrvdlikdihpbxhzenugntvnrfydttvvuihviwikvltgvmgfdgrtkbecfhgjmzvvrnpqthvujwegmgeyfofgebjvtlvvqveccsrzifmevxnuggxyvnvewmxvijrnbmsnvfnplbrrgyagbkekzhtupkmccpbkkxhvtfntmwmklhskbmsftwhrgttcrwrkvaiisugjzhsdkbrukkivenugvwmjgfnamwlvivnvpksfduafxbgbvxhrokewwcgkwglvivnvpksfdqnntmsfkbruifiwrgvnqtvjtlnytmlzjnvomkirucaitxeefprtbaisfqycvwxyvhgcsxeuzprcteswpihczxhvrxvcutpzmy"
	candidates = [2, 4, 8] # divisori di 8, che è l'MCD(200, 72), ottenuti tramite il metodo di Kasinsky

	print("Substrings Coincidence Indexes\n-----")
	for candidate in candidates:
		print("candidate:" + str(candidate))
		substrings = coincidenceIndexTest(ciphertext, candidate)
	print("-----\n")


	key = findKey(substrings)
	print("Key\n-----\n" + key + "\n-----")


if __name__ == '__main__':
    main()