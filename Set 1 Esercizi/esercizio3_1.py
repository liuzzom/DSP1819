import math
import re
import matplotlib.pyplot as plt

def getKGrams(str, k):
	""" Divisione del testo in blocchi di dimensione k
	:param str: testo da suddividere in blocchi
	:param k: dimensione dei blocchi
	"""

	# lista dei blocchi
	kGrams = []
	while str != "":
		# aggiunge il blocco alla lista
		kGrams.append(str[0:k])
		# accorcia la stringa di k caratteri
		str = str[k:]
	# riordinamento utile per future analisi
	kGrams.sort()
	return kGrams

def kGramsAnalysis(str, k):
	""" Analisi dei blocchi di dimensione k
	:param str: testo da suddividere in blocchi
	:param k: dimensione dei blocchi
	"""

	kGrams = getKGrams(str, k)

	kGramsFrequencies = []
	# informazioni sul blocco corrente
	current = kGrams[0]
	currentCount = 0

	"""
	Se il blocco è uguale a quello corrente, si incrementa il contatore
	Altrimenti, la coppia (blocco, freqeunza) viene messa nella lista
	"""
	for kGram in kGrams:
		if kGram == current:
			currentCount += 1
		else:
			kGramsFrequencies.append((current, currentCount))
			current = kGram
			currentCount = 1

	# per aggiungere l'ultima coppia (blocco, frequenza)
	if current:
		kGramsFrequencies.append((current, currentCount))

	return sorted(kGramsFrequencies, key=lambda elem: elem[1], reverse=True)

def createPlot(xData, yData, xLabel, yLabel, plotTitle):
	""" Creazione del grafico
	:param xData: Array di dati per l'asse x
	:param yData: Array di dati per l'asse y
	:param xLabel: etichetta per l'asse x
	:param yLabel: etichetta per l'asse y
	:param plotTitle: Titolo del grafico
	"""
	plt.bar(xData, yData)
	plt.xlabel(xLabel)
	plt.ylabel(yLabel)
	plt.title(plotTitle)
	plt.show()

def entropy(text, k, frequencies):
	""" Calcolo dell'entropia
	:param text: testo su cui calcolare l'entropia
	:param k: dimensione dei blocchi in cui il testo va suddiviso
	:param frequencies: lista di frequenze dei blocchi nel testo
	"""
	entropy = 0.0
	n = math.ceil(len(text)/k)

	for i in range(len(frequencies)):
		entropy += (frequencies[i]/n) * math.log((frequencies[i]/n), 2)

	entropy = -(entropy)
	return entropy

def indexOfCoincidence(text, k):
	""" Calcolo dell'indice di coincidenza
	:param text: testo su cui calcolare l'indice di coincidenza
	:param k: dimensione dei blocchi in cui il testo va suddiviso
	"""

	kGrams = kGramsAnalysis(text, k)
	ic = 0.0
	n = math.ceil(len(text)/k)
	print("number of k-grams: " + str(n))

	for kGram in kGrams:
		ic += (kGram[1]/n)*((kGram[1]-1)/(n-1))

	return ic

def main():
	# preprocessing del testo
	textFile = open("./Moby_Dick_chapter_one.txt", "r")
	text = textFile.read()
	text = text.upper()
	text = re.sub(r"['\",.;:_@#()”“’—?!&$\n]+\ *", " ", text)
	text = text.replace("-", "")
	text = text.replace(" ", "")



	for i in range(1, 5):
		kGrams = kGramsAnalysis(text, i)
		kGramsNum = math.ceil(len(text)/i)
		print("k: " + str(i))

		if i == 1:
			# analisi delle singole lettere del testo
			lettersAnalysis = kGramsAnalysis(text, 1)
			createPlot([i[0] for i in lettersAnalysis], [i[1]/kGramsNum for i in lettersAnalysis], "Letters", "Frequency", "Letters Analysis")
		elif i == 4:
			top10KGrams = kGrams[:10]
			top10KGramsKeys = [i[0] for i in top10KGrams]
			top10KGramsValues = [i[1]/kGramsNum for i in top10KGrams]
			createPlot(top10KGramsKeys, top10KGramsValues, "K-Grams", "Frequency", str(i) + "-Grams Analysis")
		else:
			top15KGrams = kGrams[:15]
			top15KGramsKeys = [i[0] for i in top15KGrams]
			top15KGramsValues = [i[1]/kGramsNum for i in top15KGrams]
			createPlot(top15KGramsKeys, top15KGramsValues, "K-Grams", "Frequency", str(i)+"-Grams Analysis")


		print("entropy: " + str(entropy(text, i, [j[1] for j in kGrams])))
		print("index of coincidence: " + str(indexOfCoincidence(text, i)))
		print("")

if __name__ == '__main__':
	main()