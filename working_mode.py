import random
from S_AES import encrypt, decrypt

IV = random.randint(0, 65536)


def CBC(plaintext, key, IV, inv=False):
	# 将字符串转为ascii码并两两拼接
	ascii_array = [ord(char) for char in plaintext]
	if len(ascii_array) % 2:
		ascii_array.append(32)
	text_blocks = [None] * (len(ascii_array) // 2)
	concat = True
	for i, array in enumerate(ascii_array):
		if concat:
			temp = array << 8
			concat = False
		else:
			temp |= array
			concat = True
			text_blocks[(i-1)//2] = temp
	
	if inv:
		for i, text in enumerate(text_blocks):
			text_blocks[i] = decrypt(text, key) ^ IV
			IV = text
	else:
		for i, text in enumerate(text_blocks):
			IV = encrypt(text ^ IV, key)
			text_blocks[i] = IV
	
	# ascii_blocks = []
	for i, chars in enumerate(text_blocks):
		ascii_array[2*i] = chars >> 8
		ascii_array[2*i+1] = chars & 0xFF
	
	return ''.join(chr(char) for char in ascii_array)
	
	
if __name__ == '__main__':
	# 第五关: 工作模式
	input_text = "Hello world!"
	
	cipher_text = CBC(input_text, 0x1234, IV)
	print(cipher_text)
	
	text = CBC(cipher_text, 0x1234, IV, True)
	print(text)
	
	changed_cipher_text = ''.join([*cipher_text[:4], cipher_text[5], cipher_text[4], *cipher_text[6:]])
	print(changed_cipher_text)
	
	changed_text = CBC(changed_cipher_text, 0x1234, IV, True)
	print(changed_text)
