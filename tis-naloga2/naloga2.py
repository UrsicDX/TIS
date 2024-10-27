def naloga2(input_list, mode):
    dictionary_size = 256
    max_dictionary_size = 4096
    dictionary = {}
    output = []

    if mode == 0:  # Encoding

        dictionary = {chr(i): i for i in range(dictionary_size)}
        w = ""
        for c in input_list:
            wc = w + c
            if wc in dictionary:
                w = wc
            else:
                output.append(dictionary[w])
                if len(dictionary) < max_dictionary_size:
                    dictionary[wc] = dictionary_size
                    dictionary_size += 1
                w = c
        if w:
            output.append(dictionary[w])
        R = len(input_list) * 8 / (len(output) * 12)

    elif mode == 1:  # Decoding

        dictionary = {i: chr(i) for i in range(dictionary_size)}
        prev_code = input_list[0]
        sequence = dictionary[prev_code]

        output.extend(sequence)
        for code in input_list[1:]:
            if code in dictionary:
                sequence = dictionary[code]
            elif code == dictionary_size:
                sequence = dictionary[prev_code] + dictionary[prev_code][0]
            else:
                raise ValueError(
                    f"Error: {code}")

            output.extend(sequence)

            if len(dictionary) < max_dictionary_size:
                dictionary[dictionary_size] = dictionary[prev_code] + sequence[0]
                dictionary_size += 1
            prev_code = code
        R = len(output) * 8 / (len(input_list) * 12)

    return (output, R)


"""
test_input = [
    "B",
    "R",
    "B",
    "R",
    "R",
    "R",
    "R",
    "R"
]
"""
# decoded_output, R = naloga2(test_input, 0)
# print("Decoded Output:", decoded_output)
# print("Compression Ratio:", R)
