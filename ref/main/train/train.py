import flooride as fd
import json
import time
from pathlib import Path
from random import uniform, randint, choices, choice
from math import floor

def LoadBar(amount, length=50):
	bar_point = length / amount
	bar = 0
	while amount > 0:
		amount -= 1
		bar += bar_point
		print("\b"*(length+14),
			"█"*floor(bar),
			" "*(length-floor(bar)),
			f"{bar/length*100:6.2f}%",
			end="", flush=True)
		yield ...

def similarity(knowledge, tokens, input, ans):
	AnsLen, InputLen = len(ans), len(input)
	LenSim = 1.0 - abs(AnsLen - InputLen) / max(AnsLen, InputLen)
	StructSim, MeaningSim = 0, 0
	MeaningWordsI, StructWordsI, MeaningWordsA, StructWordsA = [], [], [], []
	for tokenI, tokenA in zip(input, ans):
		if not tokenI[0] == "X":
			StructWordsI.append(tokenI)
			MeaningWordsI.append("X")
		else:
			MeaningWordsI.append(tokenI)
			StructWordsI.append("X")
		if not tokenA[0] == "X":
			StructWordsA.append(tokenA)
			MeaningWordsA.append("X")
		else:
			MeaningWordsA.append(tokenA)
			StructWordsA.append("X")
	StructSim_point = 1 / (len(StructWordsA) - StructWordsA.count("X") + 0.01)
	MeaningSim_point = (len(MeaningWordsA) - MeaningWordsA.count("X"))
	for tokenI, tokenA in zip(StructWordsI, StructWordsA):
		if tokenI == "X" or tokenA == "X":
			continue
		elif tokenA == tokenI:
			StructSim += StructSim_point
	for tokenI, tokenA in zip(MeaningWordsI, MeaningWordsA):
		if tokenI == "X" or tokenA == "X":
			continue
		MeaningSim += fd.math.taylor(tokens[knowledge[1][tokenA[1:]]].GetEmbeddings(), tokens[knowledge[1][tokenI[1:]]].GetEmbeddings()) / MeaningSim_point

	return round(LenSim*0.1 + StructSim*0.45 + MeaningSim*0.45, 5)

def change(knowledge, tokens, PrevPatterns):
	differences = {"len" : 0, "struct" : 0, "meaning" : 0}
	for i, (ans, _) in enumerate(PrevPatterns):
		if i == 0:
			continue
		LenDiff = len(ans) - len(PrevPatterns[i-1][0])
		StructDiff = 1
		MeaningDiff = 1
		StructDiff_point = 1 / (len(ans) - ans.count("X") + 0.01)
		for tokenA, tokenP in zip(ans, PrevPatterns[i-1][0]):
			if tokenA[0] == "X" and tokenP[0] == "X":
				MeaningDiff -= 1 - fd.math.taylor(tokens[knowledge[1][tokenA[1:]]].GetEmbeddings(), tokens[knowledge[1][tokenP[1:]]].GetEmbeddings())
			else:
				if tokenA == tokenP:
					StructDiff -= StructDiff_point

		differences["len"] += LenDiff
		differences["struct"] += StructDiff
		differences["meaning"] += MeaningDiff

	return differences

if __name__ == "__main__":
	PATTERNS_PATH = Path(__file__).parent/"patterns.json"
	LABELED_TRAIN_PATH = Path(__file__).parent/"labeled_train.json"
	TOKENS_PATH = str(Path(__file__).parent.parent/"knowledge"/"tokens.flrd")
	CONJUNCTIONS_PATH = Path(__file__).parent/"conjunctions.txt"
	UNI_WORDS_PATH = Path(__file__).parent.parent/"knowledge"/"uni_words.txt"
	TEMP = 0.2
	CHANCE_MULTI = 1/TEMP
	knowledge = {}
	TrainingData = {}
	conjunctions = []
	Uniwords = []

	with open(PATTERNS_PATH, "r") as file:
		knowledge = json.load(file)
	with open(LABELED_TRAIN_PATH, "r") as file:
		TrainingData = json.load(file)
	with open(CONJUNCTIONS_PATH, "r") as file:
		conjunctions = file.read().strip().split(",")
		conjunctions = [key for key, value in knowledge[1].items() if value in conjunctions]
	with open(UNI_WORDS_PATH, "r") as file:
		UniWords = file.read().strip().split(",")
		UniWords = [key for key, value in knowledge[1].items() if value in UniWords]
	tokens = {}
	fd.mat.lay(TOKENS_PATH)
	mats = fd.mat.GetMats()
	for mat in mats:
		tokens[mat.GetWord().decode()] = mat

	epoches = [0, "N"]
	while True:
		epoches = [input("epochs: "), "N"]
		if epoches[0] == "max":
			epoches = [1_000_000, "M"]
			break
		elif not epoches[0].isdigit():
			print("enter num")
			continue
		else:
			epoches[0] = int(epoches[0])
			break
	HighestAccuracy = 0
	EpochIndex = 0
	StartTime = time.time()
	print("="*110)
	LoadingBar = LoadBar(epoches[0], 100)
	for _ in range(epoches[0]):
		FinalPrompt = []
		FinalAnswer = []
		for prompt, answer in TrainingData.items():
			response = []
			SplittedPrompt = prompt.split()
			SplittedAnswer = answer.split()
			buffer = []
			for token in SplittedPrompt:
				if not token in knowledge[1].values():
					knowledge[0] += 1
					knowledge[1][str(knowledge[0])] = token
					if not token in UniWords:
						tokens[token] = fd.mat.MakeMat(token.encode("utf-8"), [], [round(uniform(-10,10), 5) for _ in range(3)])
				VectorizedToken = str(*[k for k, v in knowledge[1].items() if v == token])
				if token in conjunctions:
					FinalPrompt.append(buffer)
					buffer = []
					continue
				if not VectorizedToken in UniWords:
					buffer.append(f"X{VectorizedToken}")
					continue
				buffer.append(VectorizedToken)
			FinalPrompt.append(buffer)
			buffer = []

			for token in SplittedAnswer:
				if not token in knowledge[1].values():
					knowledge[0] += 1
					knowledge[1][str(knowledge[0])] = token
					if not token in UniWords:
						tokens[token] = fd.mat.MakeMat(token.encode("utf-8"), [], [round(uniform(-10,10), 5) for _ in range(3)])
				VectorizedToken = str(*[k for k, v in knowledge[1].items() if v == token])
				if token in conjunctions:
					FinalAnswer.append(Buffer)
					buffer = []
					continue
				if not VectorizedToken in UniWords:
					buffer.append(f"X{VectorizedToken}")
					continue
				buffer.append(VectorizedToken)
			FinalAnswer.append(buffer)

			for finalP, finalA in zip(FinalPrompt, FinalAnswer):
				MeaningWords = [token for token in finalP if token[0] == "X"]
				for token in MeaningWords:
					MeaningWordsEmbeddings = [tokens[knowledge[1][token[1:]]].GetEmbeddings() for token in MeaningWords]
				ref = [sum([embedding[i] for embedding in MeaningWordsEmbeddings]) / len(MeaningWords) for i in range(fd.mat.inspect()[0])]
				RefClosestWords = sorted([(token, fd.math.taylor(tokens[word].GetEmbeddings(), ref)) for token, word in knowledge[1].items()], key=lambda pair: pair[1])
				ClosestSim = 0
				ClosestPatternV = []
				ClosestPatternK = ""
				for patternK, patternV in knowledge[2].items():
					sim = similarity(knowledge, tokens, finalP, patternK)
					if sim > ClosestSim:
						ClosestSim = sim
						ClosestPatternV = patternV
						ClosestPatternK = patternK
				if ClosestSim < 0.45 or not ClosestPatternK:
					ClosestPatternK = finalP

				PrevSim = 0
				PrevPatterns = []
				if ClosestPatternV:
					PrevSim = ClosestPatternV[1]
					PrevPatterns = ClosestPatternV[2]
				else:
					ClosestPatternV = [" ".join([choice(list(knowledge[1].keys())) for _ in range(3)]), 0, []]
				ResponseBuffer = ClosestPatternV[0].split() if len(ClosestPatternV[0]) > 1 else list(ClosestPatternV[0])
				for i, token in enumerate(ResponseBuffer):
					chance = randint(1,100)
					if chance >= PrevSim * 100:
						ResponseBuffer[i] = choice(list(knowledge[1].keys()))
					if ClosestPatternV[2]:
						diff = change(knowledge, tokens, ClosestPatternV[2] + [[ResponseBuffer, 0]])
						if diff["len"] > 0:
							del ResponseBuffer[randint(0, len(ResponseBuffer)-1)]
						elif diff["len"] < 0:
							ResponseBuffer.append(choice(list(knowledge[1].keys())))
						if chance <= diff["struct"] * 100:
							ResponseBuffer[randint(0,len(ResponseBuffer)-1)] = choice(list(knowledge[1].keys()))
						if chance <= diff["meaning"] * 100:
							ResponseBuffer[randint(0,len(ResponseBuffer)-1)] = choice(list(knowledge[1].keys()))
				if not ClosestPatternV[0]:
					for _ in range(randint(0,5)):
						ResponseBuffer.append(choice(list(knowledge[1])))
				for i, token in enumerate(ResponseBuffer):
					if not token in UniWords:
						ResponseBuffer[i] = "X" + choice(list(knowledge[1].keys()))
				response.append(ResponseBuffer)

				SimTemp =  similarity(knowledge, tokens, ResponseBuffer, finalA)
				while len(PrevPatterns) > 4:
					del PrevPatterns[0]
				PrevPatterns.append([ResponseBuffer, SimTemp])
				ClosestPatternK_str = " ".join(ClosestPatternK) if not isinstance(ClosestPatternK, str) else ClosestPatternK
				ResponseBuffer_str = " ".join(ResponseBuffer)
				if ClosestPatternK_str in knowledge[2] and knowledge[2][ClosestPatternK_str] and knowledge[2][ClosestPatternK_str][1] > SimTemp:
					continue
				knowledge[2][ClosestPatternK_str] = [ResponseBuffer_str, SimTemp, PrevPatterns]

			sim = 0
			for seg in response:
				sim += similarity(knowledge, tokens, seg, finalA) / len(response)

			if sim > HighestAccuracy:
				HighestAccuracy = sim

		EpochIndex += 1
		next(LoadingBar)
		if epoches[1] == "M" and sim == 1.0:
			print(f"\ncorrect in {EpochIndex} epoches")
			break
	EndTime = time.time()
	print()
	print("="*110)
	print("highest accuracy: ", HighestAccuracy)
	print("took: ", f"{round(EndTime-StartTime, 2):,.2f}s")

	with open(PATTERNS_PATH, "w") as file:
		json.dump(knowledge, file)
	fd.mat.roll(TOKENS_PATH)