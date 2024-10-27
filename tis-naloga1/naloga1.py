import math
from collections import Counter


def preprocess_text(text):
    filtered_text = ''.join(filter(str.isalpha, text)).upper()
    return filtered_text


def izrac_verjetnost(text, p):
    if p == 0:
        counts = Counter(text)
    else:
        counts = Counter(text[i:i+p+1] for i in range(len(text) - p))

    total = sum(counts.values())
    verjetnost = {k: v / total for k, v in counts.items()}
    # print(verjetnost)
    return verjetnost


def izrac_entropy(verjetnost):
    return -sum(p * math.log2(p) for p in verjetnost.values())


def naloga1(besedilo, p):
    processed_text = preprocess_text(besedilo)
    # drugace racunamo za p = 0 in ce je p vecji
    if p > 0:
        verjetnost_p = izrac_verjetnost(processed_text, p-1)
        entropy_p = izrac_entropy(verjetnost_p)

    else:
        entropy_p = 0  # ne odstevamo nic tuki

    verjetnost_pn = izrac_verjetnost(processed_text, p)
    entropy_pn = izrac_entropy(verjetnost_pn)

    # odstevamo eno od druge (ali nic)
    H = entropy_pn - entropy_p
    return H
