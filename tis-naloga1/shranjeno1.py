import math
from collections import Counter

def preprocess_text(text):
    #print(''.join(filter(str.isalpha, text)).upper())
    return ''.join(filter(str.isalpha, text)).upper()

def calculate_probabilities(text, p):
    counts = Counter()

    if p == 0:
        counts = Counter(text)
    else:
        for i in range(len(text) - p):
            seq = text[i:i+p+1]
            counts[seq] += 1

    total = sum(counts.values())
    probabilities = {seq: count / total for seq, count in counts.items()}
    #print(probabilities)
    return probabilities

def calculate_entropy(probabilities, p):
    if p == 0:
        return -sum(prob * math.log2(prob) for prob in probabilities.values())
    else:
        entropy = 0
        context_counts = Counter()
        for seq in probabilities:
            context = seq[:-1]
            context_counts[context] += probabilities[seq] * sum(probabilities.values())
        
        entropy = 0
        for seq, prob in probabilities.items():
            context = seq[:-1]
            context_prob = context_counts[context] / sum(context_counts.values())
            conditional_prob = prob / context_prob
            entropy -= prob * math.log2(conditional_prob)
        #print(entropy)
        return entropy


def naloga1(besedilo, p) -> float:
    processed_text = preprocess_text(besedilo)
    probabilities = calculate_probabilities(processed_text, p)
    H = calculate_entropy(probabilities, p)
    return H
