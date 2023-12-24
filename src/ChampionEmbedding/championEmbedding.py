import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize, word_tokenize
import warnings
from transformers import BertModel

warnings.filterwarnings(action = 'ignore')

import gensim
from gensim.models import Word2Vec


sample = open("./src/ChampionEmbedding/aatrox.txt")
s = sample.read()

# Replaces escape character with space
f = s.replace("\n", " ")

data = []

# iterate through each sentence in the file
for i in sent_tokenize(f):
	temp = []
	
	# tokenize the sentence into words
	for j in word_tokenize(i):
		temp.append(j.lower())

	data.append(temp)

# Create CBOW model
model1 = gensim.models.Word2Vec(data, min_count = 1, 
							vector_size = 100, window = 20)

# Print results
print("most similar words to aatrox : ", model1.wv.most_similar(positive=['aatrox']))

# Create Skip Gram model
model2 = gensim.models.Word2Vec(data, min_count = 1, vector_size = 100,
											window = 20, sg = 1)

# Print results
print("most similar words to aatrox : ", model2.wv.most_similar(positive=['aatrox']))
	