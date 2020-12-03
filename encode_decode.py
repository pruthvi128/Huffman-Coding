import heapq as hq
import os


class EncodeDecode:
    def __init__(self, path):
        self.path = path
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

    class HeapNode:
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        def __lt__(self, other):
            return self.freq < other.freq

    # compression:
    def freq_dictionary(self, text):
        freq_dict = {}
        for char in text:
            if char not in freq_dict:
                freq_dict[char] = 0
            freq_dict[char] += 1
        return freq_dict

    def create_heap(self, freq):
        for key in freq:
            node = self.HeapNode(key, freq[key])
            hq.heappush(self.heap, node)

    def concat_nodes(self):
        while len(self.heap) > 1:
            node1 = hq.heappop(self.heap)
            node2 = hq.heappop(self.heap)
            concat = self.HeapNode(None, node1.freq + node2.freq)
            concat.left = node1
            concat.right = node2
            hq.heappush(self.heap, concat)

    def create_helper(self, root, current_code):
        if root is None:
            return

        if root.char is not None:
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        self.create_helper(root.left, current_code + "0")
        self.create_helper(root.right, current_code + "1")

    def make_codes(self):
        root = hq.heappop(self.heap)
        current_code = ""
        self.create_helper(root, current_code)

    def text_encoded(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text

    def add_padd(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def create_array(self, padded_text):
        if len(padded_text) % 8 != 0:
            print("Encoded text not padded properly")
            exit(0)
        b = bytearray()
        for i in range(0, len(padded_text), 8):
            byte = padded_text[i:i + 8]
            b.append(int(byte, 2))
        return b

    def compress(self):
        file, file_extension = os.path.splitext(self.path)
        compose_path = file + "_compressed" ".bin"
        with open(self.path, 'r+') as file, open(compose_path, 'wb') as output:
            message = file.read()
            message = message.rstrip()
            frequency = self.freq_dictionary(message)
            self.create_heap(frequency)
            self.concat_nodes()
            self.make_codes()
            encoded_text = self.text_encoded(message)
            padded_encoded_text = self.add_padd(encoded_text)
            b = self.create_array(padded_encoded_text)
            output.write(bytes(b))

        return compose_path

    # decompression
    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)
        padded_encoded_text = padded_encoded_text[8:]
        encoded_text = padded_encoded_text[:-1 * extra_padding]

        return encoded_text

    def text_decode(self, encoded_text):
        current_code = ""
        decoded_text = ""
        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                character = self.reverse_mapping[current_code]
                decoded_text += character
                current_code = ""
        return decoded_text

    def decompress(self, input_path):
        file, file_extension = os.path.splitext(self.path)
        decompose_path = file + "_decompressed" + ".txt"
        with open(input_path, 'rb') as file, open(decompose_path, 'w') as output:
            bit_string = ""
            byte = file.read(1)
            while len(byte) > 0:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)
            compressed_text = self.remove_padding(bit_string)
            decompressed_text = self.text_decode(compressed_text)
            output.write(decompressed_text)
        return decompose_path
