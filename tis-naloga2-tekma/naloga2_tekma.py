import os
import time


def apply_rle(input_bytes):
    if not input_bytes:
        return b''

    compressed = []
    last_byte = input_bytes[0]
    count = 1

    for byte in input_bytes[1:]:
        if byte == last_byte:
            count += 1
            if count == 255:  # Max count for a single byte.
                compressed.extend([last_byte, count])
                count = 0
        else:
            if count:
                compressed.extend([last_byte, count])
            last_byte = byte
            count = 1
    compressed.extend([last_byte, count])  # Add the last run.

    return bytes(compressed)


def compress(input_bytes):
    dict_size = 256
    dictionary = {bytes([i]): i for i in range(dict_size)}
    w = b''
    result = []
    bit_stream = []

    for byte in input_bytes:
        wc = w + bytes([byte])
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            if dict_size < 65536:  # 2^16, an arbitrary choice of max dict size
                dictionary[wc] = dict_size
                dict_size += 1
            else:
                pass
            w = bytes([byte])

    if w:
        result.append(dictionary[w])

    for code in result:
        bits = bin(code)[2:].rjust(12, '0')  # 12-bit codes
        bit_stream.extend(int(bit) for bit in bits)

    compressed_bytes = bytearray()
    for i in range(0, len(bit_stream), 8):
        byte = bit_stream[i:i+8]
        compressed_bytes.append(int(''.join(map(str, byte)), 2))

    return bytes(compressed_bytes)


def decompress(compressed_bytes):
    dict_size = 256
    dictionary = {i: bytes([i]) for i in range(dict_size)}
    bit_stream = []
    for byte in compressed_bytes:
        bits = bin(byte)[2:].rjust(8, '0')
        bit_stream.extend(map(int, bits))

    codes = []
    for i in range(0, len(bit_stream), 12):  # 12-bit codes
        code_bits = bit_stream[i:i+12]
        if len(code_bits) < 12:
            break
        code = int(''.join(map(str, code_bits)), 2)
        codes.append(code)

    w = bytes([codes.pop(0)])
    result = [w]
    for k in codes:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[:1]
        else:
            raise ValueError('Bad compressed k: %s' % k)
        result.append(entry)

        if dict_size < 32768 and (w + entry[:1]) not in dictionary.values():
            dictionary[dict_size] = w + entry[:1]
            dict_size += 1

        w = entry

    return b''.join(result)


def naloga2_tekma(dat_vhod, dat_izhod, nacin):
    start_time = time.time()
    if nacin == 0:  # Compression
        with open(dat_vhod, 'rb') as f:
            input_data = f.read()
        compressed_data = compress(input_data)
        with open(dat_izhod, 'wb') as f:
            f.write(compressed_data)
        compression_ratio = len(input_data)/len(compressed_data)
    else:  # Decompression
        with open(dat_vhod, 'rb') as f:
            compressed_data = f.read()
        decompressed_data = decompress(compressed_data)
        with open(dat_izhod, 'wb') as f:
            f.write(decompressed_data)
        compression_ratio = len(compressed_data)/len(decompressed_data)
    end_time = time.time()
    time_used = end_time - start_time

    return compression_ratio, time_used


'''
test_dir = 'testni-nabor'
output_dir = 'output'

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(test_dir):
    file_path = os.path.join(test_dir, filename)
    compressed_file_path = os.path.join(output_dir, filename + '.compressed')
    decompressed_file_path = os.path.join(
        output_dir, filename + '.decompressed')

    # testing
    compression_info, time_to_compress = naloga2_tekma(
        file_path, compressed_file_path, 0)
    compression_ratio = compression_info
    print(f"File: {filename}")

    print(f"Compression ratio: {compression_ratio:.2f}")
    print(f"Time used to compress: {time_to_compress:.4f} seconds")

    decompression_info, time_to_decompress = naloga2_tekma(
        compressed_file_path, decompressed_file_path, 1)
    print(f"Time used to decompress: {time_to_decompress:.4f} seconds")
    print()
'''
