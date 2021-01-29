# %%
import re


class RegularExpressions:
    '''
    Class for storing regular expressions as fields with methods
    returning found matches.
    '''
    def __init__(self):
        self.regex = {
            'nips': r'(\b\d{10}\b|\b\d{3}-\d{3}-\d{2}-\d{2}\b|'
                    r'\b\d{3}-\d{2}-\d{2}-\d{3}\b)',

            'dates': r'(\b[0-3][0-9]-[0-3][0-9]-20[1-2][0-9]\b|'
                     r'\b20[1-2][0-9]-[0-3][0-9]-[0-3][0-9]\b)',

            'amount': r'\b\d+[,.]\d{2}\b',
            'id': r'\b(\d{13}\b|'
                  r'\d{6}-20[1-2][0-9]-\d{3}|'
                  r'\d{6}-\d{2}-\d{4}[A-Za-z]|'
                  r'\d{4}/[A-Za-z]/\d{3}/[1-2]\d)\b',
        }

    def get_match(self, text, expression):
        '''
        returns an array of all found matches of regular expression.
        possible expression: nips, dates, amount
        '''
        if expression not in self.regex:
            raise Exception('Szukasz złego pola')

        compiled = re.compile(self.regex[expression])
        if expression in ['id', 'dates']:
            found = compiled.search(text)
            if found:
                return found.group(0)

        found = compiled.findall(text)

        if found:
            if expression == 'nips':
                return list(set(found))[:2]
            elif expression == 'amount':
                return max(list(map(float, [element.replace(',', '.')
                                            for element in found])))
        return None


if __name__ == '__main__':
    exp = RegularExpressions()
    print(exp.get_match("haba 23,54 31.37 4baba", "amount"))
    print(exp.get_match('nip  8374910024 972-086-54-31 zera 111-111-11-11',
                        'nips'))
    print(exp.get_match('gfhf 022245-19-0550W ogdr74735746 1234567890123 hry '
                        '123456-2021-123 othfo 1234/H/123/20', 'id'))
# %%
