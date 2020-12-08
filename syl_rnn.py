import re
import glob

remove = ['\u200e', '[', ']', '(', ')', '\x98', '́', '\r', ';']
replace = {
    '»': '"',
    '«': '"',
    '“': '"',
    '„': '"',
    '...': '…',
    '—': '-',
}
signs = ['.', ',', '"', '…', '-', '\n', '?', '!', ':']
vowels = 'а у о ы и э я ю ё е ь'.split(' ')
consonants = 'б в г д ж з й к л м н п р с т ф х ц ч ш щ ъ'.split(' ')


def preprocess_str(string):
    string = string.lower()
    for x in remove:
        string = string.replace(x, '')
    for key, value in replace.items():
        string = string.replace(key, value)
    string = re.sub(r'[. ]{2,}', '. ', string)
    string = re.sub(r' +', ' ', string)
    return string


def split_to_syllables(text):
    syllables = []
    cur_syl = ''
    v_in_cur_syl = False
    for l in text:
        if l in signs or l == ' ':
            syllables.append(cur_syl)
            syllables.append(l)
            cur_syl = ''
            v_in_cur_syl = False
        else:
            if l in vowels and v_in_cur_syl:
                if cur_syl[-1] in consonants:
                    syllables.append(cur_syl[:-1])
                    cur_syl = cur_syl[-1] + l
                else:
                    syllables.append(cur_syl)
                    cur_syl = l
            elif l in vowels and not v_in_cur_syl:
                v_in_cur_syl = True
                cur_syl += l
            else:
                cur_syl += l
    syllables.append(cur_syl)
    return list(filter(lambda x: x, syllables))


chars = set()
for path in glob.glob('poems/*.txt'):
    with open(path, 'rb') as f:
        text = preprocess_str(f.read().decode('utf-8'))
    chars.update(text.split(' '))
    syls = split_to_syllables(text)
    print(syls)
    print('' in syls)
    break
