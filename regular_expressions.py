import re


class RegularExpressions():
    '''
    Class for storing regular expressions as fields with methods
    returning found matches.
    '''
    def __init__(self):
        self.regex = {
            'nips': [r'\d{10}',
                     r'\d{3}-\d{3}-\d{2}-d{2}',
                     r'\d{3}-\d{2}-\d{2}-d{3}'],

            'dates': ['[0-3][0-9]-[0-3][0-9]-20[1-2][0-9]',
                      '20[1-2][0-9]-[0-3][0-9]-[0-3][0-9]'],

            'amount': [r'([0-9]+)[.,][0-9]{2}', ],
        }

    def get_match(self, text, expression):
        '''
        returns an array of all found matches of regular expression
        '''
        if expression not in self.regex:
            raise Exception('Szukasz złego pola')

        found = []
        for n in self.regex[expression]:
            compiled = re.compile(n)
            found.extend(compiled.findall(text))
        return found


if __name__ == '__main__':
    