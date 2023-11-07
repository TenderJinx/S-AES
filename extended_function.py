from S_AES import encrypt, decrypt


def ASCII_S_AES(hex_array, key, inv=False):
	changed_array = []
	concat = True
	for array in hex_array:
		if concat:
			temp = array << 8
			concat = False
		else:
			temp |= array
			concat = True
			changed_array.append(temp)
	if inv:
		return [decrypt(array, key) for array in changed_array]
	return [encrypt(array, key) for array in changed_array]


def extended_function(input_text, key, inv=False):
	"""
	:param input_text: 待加密的string
	:param key: 密钥
	:param inv: 是否为逆运算, 默认为False
	:return: 加密后的string
	"""
	# 将字符串转换为 ASCII 编码的数组
	ascii_array = [ord(char) for char in input_text]
	if len(ascii_array) % 2:
		ascii_array.append(32)
	cipher_array = ASCII_S_AES(ascii_array, key, inv)
	# 返回聚合在一起的字符串''.join(chr(char) for char in cipher_array)
	ascii_array_ = []
	for chars in cipher_array:
		ascii_array_.append(chars >> 8)
		ascii_array_.append(chars & 0xFF)
	return ''.join(chr(char) for char in ascii_array_)


if __name__ == '__main__':
	# 第三关: 扩展功能
	input_text = "Hello world!"
	key = 0b1111010101110000
	ciphertext = extended_function(input_text, key)
	print(ciphertext)
	text = extended_function(ciphertext, key, True)
	print(text)
