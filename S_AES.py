def text_to_nibbles(text):
	return [(text >> 12) & 0xF, (text >> 4) & 0xF, (text >> 8) & 0xF, text & 0xF]


def nibbles_to_text(nibbles):
	return (nibbles[0] << 12) | (nibbles[1] << 4) | (nibbles[2] << 8) | nibbles[3]


def GF_add(text, key):
	return [i ^ j for i, j in zip(text, key)]


S_box = {
	0x0: 0x9, 0x1: 0x4, 0x2: 0xA, 0x3: 0xB,
	0x4: 0xD, 0x5: 0x1, 0x6: 0x8, 0x7: 0x5,
	0x8: 0x6, 0x9: 0x2, 0xA: 0x0, 0xB: 0x3,
	0xC: 0xC, 0xD: 0xE, 0xE: 0xF, 0xF: 0x7,
}

inv_S_box = {v: k for k, v in S_box.items()}


def sub_nibbles(nibbles):
	return [S_box[n] for n in nibbles]


def inv_sub_nibbles(nibbles):
	return [inv_S_box[n] for n in nibbles]


def shift_rows(state):
	return [*state[:2], state[3], state[2]]


def GF_mult(x, y):
	result = 0
	while y > 0:
		if y & 1:
			result ^= x
		y >>= 1
		x <<= 1
		if x & 0x10:
			x ^= 0x13
	return result


def mix_columns(nibbles):
	return [nibbles[0] ^ GF_mult(4, nibbles[2]), nibbles[1] ^ GF_mult(4, nibbles[3]),
	        nibbles[2] ^ GF_mult(4, nibbles[0]), nibbles[3] ^ GF_mult(4, nibbles[1])]


def inv_mix_columns(nibbles):
	return [GF_mult(9, nibbles[0]) ^ GF_mult(2, nibbles[2]), GF_mult(9, nibbles[1]) ^ GF_mult(2, nibbles[3]),
	        GF_mult(9, nibbles[2]) ^ GF_mult(2, nibbles[0]), GF_mult(9, nibbles[3]) ^ GF_mult(2, nibbles[1])]


RCON = [0x80, 0x30]


def key_expansion(key):
	extended_key = [None] * 6
	extended_key[0] = (key >> 8) & 0xFF
	extended_key[1] = key & 0xFF
	
	for i in range(2, 6):
		temp = extended_key[i - 1]
		if i % 2 == 0:
			temp = (S_box[temp & 0x0F] << 4) | S_box[(temp >> 4) & 0x0F]
			temp = temp ^ RCON[(i - 2) // 2]
		extended_key[i] = extended_key[i - 2] ^ temp
	
	return [(extended_key[0] << 8) | extended_key[1],
	        (extended_key[2] << 8) | extended_key[3],
	        (extended_key[4] << 8) | extended_key[5]]


def encrypt(plaintext, key):
	if key > 65536 or key < 0:
		raise ValueError("密钥格式错误")
	if plaintext > 65536 or plaintext < 0:
		raise ValueError("明文格式错误")
	# Assuming plaintext and key are 16-bit integers
	state = text_to_nibbles(plaintext)
	
	round_keys = key_expansion(key)
	for i, text in enumerate(round_keys):
		round_keys[i] = text_to_nibbles(text)
	
	# Initial round
	state = GF_add(state, round_keys[0])
	
	# Main round
	state = sub_nibbles(state)
	state = shift_rows(state)
	state = mix_columns(state)
	state = GF_add(state, round_keys[1])
	
	# Final round
	state = sub_nibbles(state)
	state = shift_rows(state)
	state = GF_add(state, round_keys[2])
	
	# Return the ciphertext
	return nibbles_to_text(state)


def decrypt(ciphertext, key):
	if key > 65536 or key < 0:
		raise ValueError("密钥格式错误")
	if ciphertext > 65536 or ciphertext < 0:
		raise ValueError("密文格式错误")
	# Assuming ciphertext is a list of 4 nibbles and key is a 16-bit integer
	state = text_to_nibbles(ciphertext)
	
	round_keys = key_expansion(key)
	for i, text in enumerate(round_keys):
		round_keys[i] = text_to_nibbles(text)
	
	# Initial round with the last round key
	state = GF_add(state, round_keys[2])
	
	# Inverse final round
	state = shift_rows(state)
	state = inv_sub_nibbles(state)
	
	# Inverse main round
	state = GF_add(state, round_keys[1])
	state = inv_mix_columns(state)
	state = shift_rows(state)
	state = inv_sub_nibbles(state)
	
	# Add round key 0
	state = GF_add(state, round_keys[0])
	
	# Return the plaintext
	return nibbles_to_text(state)


if __name__ == '__main__':
	text = 0b1001001110101100
	key = 0b1111010101110000
	print(key)
	print(text)
	
	ciphertext = encrypt(text, key)
	print(ciphertext)
	
	plaintext = decrypt(ciphertext, key)
	print(plaintext)
