import math
import numpy as np


def naloga3(vhod: list, n: int) -> tuple[list, str]:
    izhod = []
    crc = ""
    m = int(math.log2(n))
    k = n - m - 1
    I = np.identity(m, dtype=np.uint8)
    H = generateHamming(n, m)
    crc = calculate_crc8(vhod)

    # Reshape H to 2D before concatenating
    H = np.array(H, dtype=np.uint8).reshape(-1, m)
    H = np.concatenate((H, I))

    while len(vhod) > 0:
        sporocilo = vhod[:n]
        vhod = vhod[n:]
        y = sporocilo[:-1]
        paritetni = int(np.remainder(np.sum(sporocilo), 2))

        s = int(("".join([str(i) for i in np.remainder(
            np.matrix(y).dot(H), 2)[0].tolist()[0]])), 2)

        if paritetni == 1 and s != 0:
            stolpec = 0

            for i in range(len(H)):
                temp = int(("".join([str(i) for i in H[i]])), 2)
                if temp == s:
                    stolpec = i
                    break

            if y[stolpec] == 0:
                y[stolpec] = 1
            else:
                y[stolpec] = 0

        for i in range(k):
            izhod.append(y[i])

    return (izhod, crc)


def generateHamming(n, m):
    H = []

    for i in range(1, n):
        if (math.log2(i) % 1 == 0):
            continue
        num = bin(i)[2:]
        num = str(num.zfill(m))
        arr = []

        for i in range(len(num)):
            arr.append(int(num[i]))

        H.append(arr)

    return H


def calculate_crc8(data: bytes):
    crc = 0xFF   # Initial CRC value filled with 8 bits of ones
    poly = 0x9B  # Polynomial for XOR operation

    for byte in data:
        msb = (crc & 0x80) >> 7
        if byte ^ msb == 0:      # If XOR result is 0, shift the CRC to the left
            crc = (crc << 1) & 0xFF
        else:                     # If XOR result is 1, XOR CRC with polynomial after shifting
            crc = ((crc << 1) ^ poly) & 0xFF

    return format(crc, '02X')


'''
if __name__ == "__main__":
    # Define your test case here
    input_data = [0,
                  0,
                  1,
                  1,
                  1,
                  1,
                  0,
                  0,
                  0,
                  0,
                  1,
                  1,
                  0,
                  1,
                  1,
                  1,
                  1,
                  1,
                  0,
                  0,
                  0,
                  0,
                  1,
                  1,
                  1,
                  1,
                  1,
                  1,
                  1,
                  1]
    n = 3

    # Call the function with your test case
    result = naloga3(input_data, n)
    print("Output:", result)
'''
