class SHA256:    
    def get_binary(self, input):
        """
        SHA256 algorithm operates on binary data, so this function converts the input string into its binary representation.
        Each character is converted to its ASCII value and then to an 8-bit binary string.
        """
        if type(input) != str:
            input = str(input)
        result = ""
        for characters in input:
            value = ord(characters)
            byte_val = ""
            for i in range(8):
                byte_val = str(int(value % 2)) + byte_val
                value = value // 2
            result += byte_val
        return result

    def padding(self, binary_input):
        """
        The padding function prepares the binary input for processing by the SHA256 algorithm. It appends a '1' bit to the end of the input, followed by enough '0' bits to make the length of the input congruent to 448 modulo 512. Finally, it appends a 64-bit representation of the original input length.
        Args:
            binary_input (str): The binary string representation of the input data to be padded.
        Returns:
            str: The padded binary string ready for processing by the SHA256 algorithm.
        """
        original_len = len(binary_input)
        result = binary_input + "1"
        while len(result) % 512 != 448:
            result += "0"
        length_bin = format(original_len, '064b')
        result += length_bin
        return result

    def rotate_right(self, word, n):
        """
        Performs a right rotation on a 32-bit binary word by n positions. The bits that are shifted out on the right are reintroduced on the left.
        Args:
            word (str): A 32-bit binary string to be rotated.
            n (int): The number of positions to rotate the bits to the right.
        Returns:
            str: The resulting binary string after the right rotation.
        """
        return word[32 - n:] + word[0:32 - n]

    def shift_right(self, word, n):
        """
        Performs a right shift on a 32-bit binary word by n positions. The bits that are shifted out on the right are discarded, and the leftmost n bits are filled with zeros.
        Args:
            word (str): A 32-bit binary string to be shifted.
            n (int): The number of positions to shift the bits to the right.
        Returns:
            str: The resulting binary string after the right shift.
        """
        return "0" * n + word[0:32 - n]

    def xor(self, word1, word2):
        """
        Performs a bitwise XOR operation between two binary strings of equal length. The result is a new binary string where each bit is '1' if the corresponding bits of the input strings are different, and '0' if they are the same.
        Args:
            word1 (str): The first binary string for the XOR operation.
            word2 (str): The second binary string for the XOR operation, which must be of the same length as word1.
        Returns:
            str: The resulting binary string after the XOR operation.
        """
        result = "".join("0" if word1[i] == word2[i] else "1" for i in range(len(word1)))
        return result

    def addition_32(self, word1, word2):
        """
        Performs addition of two 32-bit binary words modulo 2^32. The result is a new 32-bit binary string that represents the sum of the two input words, with any overflow beyond 32 bits discarded.
        Args:
            word1 (str): The first 32-bit binary string to be added.
            word2 (str): The second 32-bit binary string to be added, which must be of the same length as word1.
        Returns:
            str: The resulting 32-bit binary string after the addition operation.
        """
        res = (int(word1, 2) + int(word2, 2)) % 4294967296
        return format(res, "032b")

    def ch(self, e, f, g):
        res = "".join(f[i] if e[i] == "1" else g[i] for i in range(len(e)))
        return res

    def maj(self, a, b, c):
        res = ""
        for i in range(len(a)):
            count = int(a[i]) + int(b[i]) + int(c[i])
            res += "1" if count >= 2 else "0"
        return res

    def sigma0(self, w):
        return self.xor(self.xor(self.rotate_right(w, 7), self.rotate_right(w, 18)), self.shift_right(w, 3))

    def sigma1(self, w):
        return self.xor(self.xor(self.rotate_right(w, 17), self.rotate_right(w, 19)), self.shift_right(w, 10))

    def S0(self, w):
        return self.xor(self.xor(self.rotate_right(w, 2), self.rotate_right(w, 13)), self.rotate_right(w, 22))

    def S1(self, w):
        return self.xor(self.xor(self.rotate_right(w, 6), self.rotate_right(w, 11)), self.rotate_right(w, 25))

    def hash(self, text):
        K_hex = [
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
            0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
            0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
            0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
            0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
            0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
        ]
        K = [format(k, '032b') for k in K_hex]

        H_hex = [
            0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
            0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
        ]
        h_vars = [format(h, '032b') for h in H_hex]
        h0, h1, h2, h3, h4, h5, h6, h7 = h_vars

        padded = self.padding(self.get_binary(text))
        
        for i in range(0, len(padded), 512):
            block = padded[i:i+512]
            words = [block[j:j+32] for j in range(0, 512, 32)]
            
            for j in range(16, 64):
                val = self.addition_32(self.addition_32(self.sigma1(words[j-2]), words[j-7]), self.addition_32(self.sigma0(words[j-15]), words[j-16]))
                words.append(val)

            a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7

            for j in range(64):
                t1 = self.addition_32(self.addition_32(self.addition_32(h, self.S1(e)), self.addition_32(self.ch(e, f, g), K[j])), words[j])
                t2 = self.addition_32(self.S0(a), self.maj(a, b, c))
                a, b, c, d, e, f, g, h = self.addition_32(t1, t2), a, b, c, self.addition_32(d, t1), e, f, g

            h0 = self.addition_32(h0, a)
            h1 = self.addition_32(h1, b)
            h2 = self.addition_32(h2, c)
            h3 = self.addition_32(h3, d)
            h4 = self.addition_32(h4, e)
            h5 = self.addition_32(h5, f)
            h6 = self.addition_32(h6, g)
            h7 = self.addition_32(h7, h)

        result_hex = "".join(hex(int(x, 2))[2:].zfill(8) for x in [h0, h1, h2, h3, h4, h5, h6, h7])
        return result_hex