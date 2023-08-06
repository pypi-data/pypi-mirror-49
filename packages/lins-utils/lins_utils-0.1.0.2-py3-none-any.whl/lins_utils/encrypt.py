
#baseada em TFuncoesGerais.ASCIIEncrypt
#criptografa e descriptografa com base em uma chave
def ascii_encrypt(data, cipher):
    new_data = ''
    if len(data) > 0:
        z = len(cipher)  
        for pos,c in enumerate(data):
            code = ord(cipher[pos % z])
            if ord(c) >= 128:
                c2 = chr(ord(c) ^ (code & 127))
            elif ord(c) >= 64:
                c2 = chr(ord(c) ^ (code & 63))
            elif ord(c) >= 32:
                c2 = chr(ord(c) ^ (code & 31))
            new_data += c2
        return new_data