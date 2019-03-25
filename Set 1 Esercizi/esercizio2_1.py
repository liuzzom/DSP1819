from string import ascii_lowercase
import math


def entropy(probabilities):
	"""
	:param probabilities: lista contenente una distribuzione di probabilità
	:return: valore dell'entropia relativa alla distribuzione in input
	"""
	entropy = 0.0

	for i in range(len(probabilities)): 
		entropy += probabilities[i] * math.log(probabilities[i], 2)

	entropy = -(entropy)
	return entropy

def main():

	# english letter frequencies
	en_lett_probs = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702,
									 0.02228, 0.02015, 0.06094, 0.06966, 0.00153,
									 0.00772, 0.04025, 0.02406, 0.06749, 0.07507,
					 				 0.01929, 0.00095, 0.05987, 0.06327, 0.09056,
					 				 0.02758, 0.00978, 0.02360, 0.00150, 0.01974, 0.00074]

	en_lett_entropy = entropy(en_lett_probs)

	print("en_lett_entropy: " + str(en_lett_entropy))

	rand_lett_probs = [1/26 for letter in ascii_lowercase]
	rand_lett_entropy = entropy(rand_lett_probs)

	print("rand_lett_entropy: " + str(rand_lett_entropy))

	p_a = 1/26

	# Calcolo della divergenza nel caso in cui la scimmia batte a caso sulla tastiera
	divergence = 0.0
	for i in range(len(rand_lett_probs)):
		a = en_lett_probs[i]
		b = math.log((a/p_a), 2)
		divergence += (a*b)

	print("divergence: " + str(divergence))

if __name__ == '__main__':
    main()