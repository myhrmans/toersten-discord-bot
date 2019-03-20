import sys
from itertools import cycle
import base64




def xor_strings(s, t):
    """xor two strings together"""
    if isinstance(s, str):
        # Text strings contain single characters
        return b"".join(chr(ord(a) ^ ord(b)) for a, b in zip(s, cycle(t)))
    else:
        # Python 3 bytes objects contain integer values in the range 0-255
        return bytes([a ^ b for a, b in zip(s, cycle(t))])
        

def main():
    
    inputKey = sys.argv[1]
    inputMessage = sys.argv[2]

    key = base64.encodestring(bytes(inputKey, encoding="UTF-8"))
    cipherText = xor_strings(base64.encodestring(bytes(inputMessage, encoding="UTF-8")), key)
    
    print('cipherText:', cipherText)
    
    decText = base64.decodestring(xor_strings(cipherText, key)).decode("UTF-8")
    print('decrypted: {}'.format(decText))

    # verify
    if base64.decodestring(xor_strings(cipherText, key)).decode("UTF-8") == inputMessage:
        print('Unit test passed')
    else:
        print('Unit test failed')


if __name__ == "__main__":
    main()