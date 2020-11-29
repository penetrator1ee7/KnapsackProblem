import math as m
KEY_LENGTH = 10


def get_SG_key():
    sum = 0
    i = 1
    n = 0
    skey = [0 in range(KEY_LENGTH)]
    while i <= KEY_LENGTH:
        sk = int(input('Insert ' + str(i) + '`th super-growing key.\n'))
        if sk > sum:
            skey.insert((i - 1), sk)
            sum = sum + skey[i - 1]
            i += 1
        else:
            print(str(sk) + ' is not a super-growing key to previous keys.Write another key.\n')
    return sum, skey


def get_N(s):
    n = 0
    while m.gcd(n, s) != 1:
        n = int(input('Insert N number, which must be mutually simple to ' + str(s) + '\n'))
        if m.gcd(n, s) != 1:
            print(n, 'is not mutually simple to', s)
    return n


def to_int(num):
    if num[0] == 'b':
        num = int(num[1:], 2)
    elif len(num) > 1 and num[1] == 'x':
        num = int(num[2:], 16)
    else:
        num = int(num)
    return num


def slice_msg(m):
    M = []
    i = 0
    max_piece = (2 ** KEY_LENGTH) - 1
    while m > max_piece:
        piece = (m & max_piece)
        M.insert(i, piece)
        m = m >> KEY_LENGTH
        i += 1
    M.insert(i, m)
    M.reverse()
    return M


def cipher_gen(message, public_key):
    i = 0
    result = 0
    while i < KEY_LENGTH:
        if (message & (1 << KEY_LENGTH-i-1)) != 0:
            result = result + public_key[i]
        i += 1
    return result


def number_decipher(num, key):
    i = 0
    message = 0
    while i < KEY_LENGTH:
        if num >= key[KEY_LENGTH - 1 - i]:
            num = num - key[KEY_LENGTH - 1 - i]
            message = message + (1 << i)
        i += 1
    return message


def main():
    print('Type the function you want this app to run.\n -keygen to generate public key.\n'
          ' -cipher to cipher you message with public key.\n -decipher to decipher message with secret key.')
    mode = input()
    if mode == '-keygen':
        keygen()
    elif mode == '-cipher':
        cipher()
    elif mode == '-decipher':
        decipher()
    else:
        print('Unrecognised command.\n')
        main()
    return 1


def keygen():
    n = 0
    sum, secret_key = get_SG_key()

    s = int(input('Insert S number, which must be greater, than ' + str(sum) + '\n'))

    n = get_N(s)

    key = [0 in range(KEY_LENGTH)]
    i = 0
    while i < KEY_LENGTH:
        k = (secret_key[i] * n) % s
        key.insert(i, k)
        i += 1

    key.pop(-1)
    print('Your public key is:\n', key)
    return 1


def cipher():
    key = [0 in range(KEY_LENGTH)]
    i = 0
    while i < KEY_LENGTH:
        key.insert(i, int(input('Insert ' + str(i + 1) + '`th key.\n')))
        i += 1

    msg = input('Insert number to cipher. Use prefix b for binary number, 0x for hex number, no prefix for decimal.\n')
    msg = to_int(msg)
    M = slice_msg(msg)
    i = 0
    ciphered_msg = [0 in range(len(M) - 1)]
    while i < len(M):
        ciphered_msg.insert(i, cipher_gen(M[i], key))
        i += 1
    ciphered_msg.pop(-1)
    print(ciphered_msg)
    return 1


def decipher():
    sum, secret_key = get_SG_key()
    s = int(input('Insert S number, which must be greater, than ' + str(sum) + '\n'))
    n = get_N(s)
    inversed = pow(n, -1, s)
    msg = input('Insert numbers to decipher, splitted by "," sign.\n')
    msg = msg.replace(' ', '')
    msg = msg.split(',')
    i = 0
    for number in msg:
        msg.insert(i, (int(number) * inversed) % s)
        msg.pop(i + 1)
        i += 1
    i = 0
    for number in msg:
        msg.insert(i, number_decipher(number, secret_key))
        msg.pop(i + 1)
        i += 1
    output_str = ''
    for number in msg:
        tmp = "{0:b}".format(number)
        while len(tmp) < KEY_LENGTH:
            tmp = '0' + tmp
        output_str = output_str + tmp
    print('binary = ', output_str,'decimal = ', int(output_str, 2))
    return 1


if __name__ == '__main__':
    main()

