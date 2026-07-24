from random import choices, choice, uniform
from pathlib import Path
from difflib import get_close_matches
import flooride as fd
import time
import json

ROOT = Path(__file__).parent.parent
TOKENS_PATH = str(ROOT/"main"/"knowledge"/"tokens.flrd")
UNI_WORDS_PATH = ROOT/"main"/"knowledge"/"uni_words.txt"
IRREGULAR_WORDS_PATH = ROOT/"main"/"knowledge"/"irregular_words.json"
TRAIN_PATH = ROOT/"main"/"train"/"train.txt"

TEMP = 0.3
CHANCE_MULTI = 1 / TEMP
LR = 0.1
VALID_CHAR = {"a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q",
				"r","s","t","u","v","w","x","y","z"," ","."}

with open(TRAIN_PATH, "r") as file:
	text = file.read()
text = text.lower().strip().split(".")
print(text)

def filter(text):
	FinalText = []
	for sentence in text:
		filtered = sentence
		for letter in sentence:
			if letter not in VALID_CHAR:
				filtered = filtered.replace(letter, "")
		FinalText.append(filtered)
	return FinalText

def GenRef(tokens):
	return [sum([knowledge[token].GetEmbeddings()[i] for token in tokens if token in knowledge]) / len(tokens) for i in range(3)]

def CalcChance(vect):
	return [abs(item ** CHANCE_MULTI) for item in vect]
   
def generate(prompt, StartText="the", ref=None):
	# QuestionWords = ["what", "who", "where", "when", "how"]

	# thinking = True
	# question = None
	# subject = ""
	# action = ""
	# while thinking:
	# 	thinking = False

	predicted = StartText
	sentance = predicted + " "
	finished = False
	token = 0
	while not finished:
		if token == 10:
			break
		if predicted in knowledge:
			if not ref:
				NextWord = predict(predicted)
			else:
				differences = [(word, taylor(knowledge[word.decode()].GetEmbeddings(), ref)) for word in knowledge[predicted].GetNext()]
				token += 1
				if differences:
					SortedDifferences = sorted(differences, key=lambda word: word[1])
				else:
					finished = True
					break
				NextWord = choice(SortedDifferences[:len(SortedDifferences) // 3 + 1])[0].decode()
			if NextWord != "":
				predicted = NextWord
				sentance += predicted + " "
			else:
				finished = True
		else:
			finished = True
	return sentance[:-1] + "."

def taylor(embedding1, embedding2):
	return fd.math.taylor(embedding1, embedding2)

def predict(word1):
	NextChoices = knowledge[word1].GetNext()
	if NextChoices:
		difference = [taylor(knowledge[word1].GetEmbeddings(), knowledge[word2].GetEmbeddings()) for word2 in NextChoices]
		return choices(NextChoices, weights=CalcChance(difference))[0]
	return ""

def NlpFilter(prompt):
	vowels = ["a", "e", "i", "o", "u"]
	EsEnd1 = ["s", "x", "z", "o"]
	EsEnds2 = ["ss", "sh", "ch"]
	result = []
	if not prompt:
		return 0
	for sentance in prompt:
		TempResult = []
		for word in sentance.split():
			if word in UniWords:
				continue
			if word in IrregularWords:
				TempResult.append(IrregularWords[word])
				continue
			if word[-3:] == "ies":
				TempResult.append(word[:-3] + "y")
			elif word[-2:] == "es":
				if word[-4:-2] in EsEnds2 or word[-3] in EsEnd1:
					TempResultesult.append(word[:-2])
				else:
					TempResult.append(word)
			elif word[-1] == "s":
				TempResult.append(word[:-1])
			elif word[-3:] == "ing":
				if word[-4] == "y" or word[-4] == "w" or word[-4] == "x":
					TempResult.append(word[:-3])
				elif word[-4] == word[-5] and word[-6] in vowels and not word[-7] in vowels:
					TempResult.append(word[:-4])
				else:
					TempResult.append(word)
			elif word[-3:] == "ied":
				TempResult.append(word[:-3] + "y")
			elif word[-2:] == "ed":
				if word[-4] == word[-3]:
					TempResult.append(word[:-3])
				else:
					TempResult.append(word[:-2])
			else:
				TempResult.append(word)
		TempResult = untypofy(TempResult)
		TempResult.append("<end>")
		for token in TempResult:
			result.append(token)
	return result

def untypofy(prompt):
	return [get_close_matches(word, knowledge.keys(), n=1, cutoff=0.3)[0] if not word in knowledge else word for word in prompt]

fd.mat.lay(KNOWLEDGE_PATH)
mats = fd.mat.GetMats()
fd.mat.trash(KNOWLEDGE_PATH)
knowledge = {}
for mat in mats:
	knowledge[mat.GetWord().decode()] = mat

UniWords = []
with open(UNI_WORDS_PATH, "r") as file:
	UniWords = file.read().strip().split(",")

IrregularWords = {}
with open(IRREGULAR_WORDS_PATH, "r") as file:
	IrregularWords = json.load(file)

print(knowledge)

if __name__ == "__main__":
	while True:
		epoch = input("epoches: ") 
		if epoch.isdecimal():
			epoch = int(epoch)
			break
		else:
			print("enter num")
	start = time.perf_counter()
	for i in range(epoch):
		FirstIter = True
		for sentance in filter(text):
			WordsInSentence = sentance.split()
			if not WordsInSentence:
				continue 
			for word in WordsInSentence:
				if word not in knowledge:
					knowledge[word] = fd.mat.MakeMat(word.encode("utf-8"), [], [round(uniform(-10,10), 5) for _ in range(3)])
				if FirstIter:
					LastWord = word
					FirstIter = False
					continue
				if word.encode("utf-8") not in knowledge[LastWord].GetNext():
					knowledge[LastWord].sow(word)
				for j in range(fd.mat.inspect()[0]):
					knowledge[LastWord].restyle("e", str(knowledge[LastWord].GetEmbeddings()[j] + round((knowledge[word].GetEmbeddings()[j] - knowledge[LastWord].GetEmbeddings()[j]) * LR, 3)), j)
					mag = sum([knowledge[LastWord].GetEmbeddings()[k] ** 2 for k in range(3)]) ** 0.5
					knowledge[LastWord].restyle("e", str(round(knowledge[LastWord].GetEmbeddings()[j] / mag, 3)), j)
				LastWord = word
		FirstIter = True
		print(f"finished {i+1} epoch")
	end = time.perf_counter()
	
	TimeTook = (end - start) * 1000
	print(f"| trained: {epoch} epochs | took: {TimeTook:.3f}ms |")
	print(knowledge)
	
	running = True
	while running:
		prompt = [token for token in NlpFilter(filter(input("you: ").split("."))) if token != ""]
		print("prompt: ", prompt)
		if prompt:
			start = time.perf_counter()
			response = generate(prompt, ref=GenRef(prompt))
			end = time.perf_counter()
			print(f"blanc(thought for: {(end-start)*1000:.3f}ms): {response}")
			running = False
		else:
			print("enter something")

	fd.mat.roll(KNOWLEDGE_PATH)