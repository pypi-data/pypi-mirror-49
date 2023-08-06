'''
Package nanoid-dictionary provides ready-to-use
alphabets.
'''
import re


def prevent_misreadings(unsafe_chars, alphabet):
    '''
    prevent_misreadings removes all unsafe chars
    case-insensitively from a given string.
    '''
    return re.compile(
        f'[{unsafe_chars}]', re.IGNORECASE
    ).sub('', alphabet)


lookalikes = '1l0o'
lowercase = 'abcdefghijklmnopqrstuvwxyz'
numbers = '0123456789'
uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

alphabet_std = '_-' + numbers + lowercase + uppercase
human_alphabet = prevent_misreadings(lookalikes, alphabet_std)

__all__ = ['alphabet_std',
           'human_alphabet',
           'lookalikes',
           'lowercase',
           'numbers',
           'prevent_misreadings',
           'uppercase']

if __name__ == '__main__':
    print('Standard alphabet:\t', alphabet_std)
    print('Human oriented alphabet:', human_alphabet)
