import flooride as fd
import json
from pathlib import Path
from random import uniform

def recognize(input, output):
    ...

if __name__ == "__main__":
    PATTERNS_PATH = Path(__file__).parent/"patterns.json"
    LABELED_TRAIN_PATH = Path(__file__).parent/"labeled_train.json"
    TOKENS_PATH = str(Path(__file__).parent.parent/"knowledge"/"tokens.flrd")
    knowledge = None
    data = None

    with open(PATTERNS_PATH, "r") as file:
        knowledge = json.load(file)
    with open(LABELED_TRAIN_PATH, "r") as file:
        data = json.load(file)
    tokens = {}
    fd.mat.lay(TOKENS_PATH)
    mats = fd.mat.GetMats()
    for mat in mats:
        tokens[mat.GetWord().decode()] = mat

    for prompt, answer in data.items():
        VectorizedPrompt = []
        VectorizedAnswer = []
        for token in prompt.split():
            if not token in knowledge[1].values():
                knowledge[0] += 1
                knowledge[1][knowledge[0]] = token
                fd.mat.MakeMat(token.encode("utf-8"), [], [round(uniform(-10,10), 5) for _ in range(3)])
            VectorizedPrompt.append(*[num for num in knowledge[1] if knowledge[1][num] == token])
        for token in answer.split():
            if not token in knowledge[1].values():
                knowledge[0] += 1
                knowledge[1][knowledge[0]] = token
            VectorizedAnswer.append(*[num for num in knowledge[1] if knowledge[1][num] == token])
        print(VectorizedPrompt)
        print(VectorizedAnswer)
        response = []
        ComparePrompt = " ".join(map(str, VectorizedPrompt))
        if ComparePrompt in knowledge[2]:
            for num in knowledge[2][ComparePrompt]:
                response.append(knowledge[1][num])
        else:
            differences = {}
            for pattern in knowledge[2]:
                if not len(pattern.split()) == len(VectorizedPrompt):
                    continue
                diff = []
                for token1, token2 in zip(pattern.split(), VectorizedPrompt):
                    diff.append(round(fd.math.taylor(tokens[knowledge[1][token1]].GetEmbeddings(), tokens[knowledge[1][token2]].GetEmbeddings()), 4))
                differences[pattern] = (sum(diff) / len(diff))
            SmallestDiff = 0
            for key, value in differences.items():
                if value > SmallestDiff:
                    SmallestDiff = value
                    response = knowledge[2][key]
        print(response)

    with open(PATTERNS_PATH, "w") as file:
        json.dump(knowledge, file)

    recognize(input("prompt: "), 0)