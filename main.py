from encode_decode import EncodeDecode

file_path = "sample.txt"
h = EncodeDecode(file_path)

# Call compress function and preform compression
compose_path = h.compress()
print(f"Compressed file - {compose_path}")

# call decompress function and preform decompression
decompose_path = h.decompress(compose_path)
print(f"Decompressed file - {decompose_path}")
