import flooride as fd
import json
from pathlib import Path
from random import uniform, randint, choice

if __name__ == "__main__":
	PATTERNS_PATH = Path(__file__).parent/"patterns.json"
	LABELED_TRAIN_PATH = Path(__file__).parent/"labeled_train.json"
	TOKENS_PATH = str(Path(__file__).parent.parent/"knowledge"/"tokens.flrd")
	CONJUNCTIONS_PATH = Path(__file__).parent/"conjunctions.txt"
	UNI_WORDS_PATH = Path(__file__).parent.parent/"knowledge"/"uni_words.txt"
	knowledge = {}
	data = {}
	conjunctions = []
	Uniwords = []

	with open(PATTERNS_PATH, "r") as file:
		knowledge = json.load(file)
	with open(LABELED_TRAIN_PATH, "r") as file:
		data = json.load(file)
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

	for prompt, answer in data.items():
		response = []
		FinalPrompt = []
		FinalAnswer = []
		SplittedAnswer = answer.split()
		SplittedPrompt = prompt.split()
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

		
		epoches = 0
		while True:
			epoches = input("epochs: ")
			if not epoches.isdigit():
				print("enter num")
				continue
			else:
				epoches = int(epoches)
				break
		bundle = 1
		while True:
			bundle = input("bundle size: ")
			if not bundle.isdigit():
				print("enter num")
				continue
			else:
				bundle = int(bundle)
				break
		HighestAccuracy = 0
		BundleIndex = 0
		print("="*40)
		for _ in range(epoches):
			for finalP, finalA in zip(FinalPrompt, FinalAnswer):
				MeaningWords = [token for token in finalP if token[0] == "X"]
				for token in MeaningWords:
					MeaningWordsEmbeddings = [tokens[knowledge[1][token[1:]]].GetEmbeddings() for token in MeaningWords]
				ref = [sum([embedding[i] for embedding in MeaningWordsEmbeddings]) / len(MeaningWords) for i in range(fd.mat.inspect()[0])]
				ClosestSim = 0
				ClosestPatternV = []
				ClosestPatternK = ""
				for patternK, patternV in knowledge[2].items():
					sim = round(((2*len(patternK)*len(finalP)) / (len(patternK)**2 + len(finalP)**2))**2, 3)
					MinLen = min(len(patternK), len(finalP))
					for i in range(2, MinLen):
						if patternK[i-1] == finalP[i-1]:
							continue
						elif patternK[i-1] in finalP[i-2:i]:
							sim -= sim / MinLen / 3
						else:
							sim -= sim / MinLen
					sim = round(sim, 3)
					if sim > ClosestSim:
						ClosestSim = sim
						ClosestPatternV = patternV
						ClosestPatternK = patternK
				if not ClosestPatternK:
					ClosestPatternK = finalP

				response = []
				ResLen = 0
				PrevSim = 0.1
				if ClosestPatternV:
					PrevSim = ClosestPatternV[2] 
					ResLen = ClosestPatternV[0]
				else:
					ResLen = randint(3, 10)
				ResLen += uniform(((-3/PrevSim)**0.9).real, ((3/PrevSim)**0.9).real)
				ResLen = round(ResLen.real)
				for _ in range(ResLen):
					response.append(choice(UniWords + [f"X{i+1}" for i in range(knowledge[0])]))

				sim = round(((2*len(response)*len(finalA)) / (len(response)**2 + len(finalA)**2))**2, 3)
				MinLen = min(len(response), len(finalA))
				for i in range(MinLen):
					if response[i] == finalA[i]:
						continue
					elif 0 < i < MinLen and response[i] in finalA[i-1:i+1]:
						sim -= sim / MinLen / 3
					else:
						sim -= sim / MinLen
				sim = round(sim, 3)

			BundleIndex += 1
			if BundleIndex == bundle:
				print("final prompt: ", FinalPrompt)
				print("final answer: ", FinalAnswer)
				print("closest pattern (key) found: ", ClosestPatternK)
				print("closest pattern (value) found: ", ClosestPatternV)
				print("closest similarity found: ", ClosestSim)
				print("response length: ", ResLen)
				print("response: ", response)
				print("similarity: ", sim)
				print("="*40)
				BundleIndex = 0

			if sim > HighestAccuracy:
				HighestAccuracy = sim

			ClosestPatternK_str = " ".join(ClosestPatternK) if not isinstance(ClosestPatternK, str) else ClosestPatternK 
			if ClosestPatternK_str in knowledge[2] and knowledge[2][ClosestPatternK_str] and knowledge[2][ClosestPatternK_str][2] > sim:
				continue
			knowledge[2][ClosestPatternK_str] = [ResLen, response, sim] if not sim == 0.0 else 0.01
	print("highest accuracy: ", HighestAccuracy)

	with open(PATTERNS_PATH, "w") as file:
		json.dump(knowledge, file)
	fd.mat.roll(TOKENS_PATH)