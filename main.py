from encode_decode import Huffman

file_path = "sample.txt"

h = Huffman(file_path)

compose_path = h.compress()
print(compose_path)

decompose_path = h.decompress(compose_path)
print(decompose_path)
