# %%
string = 'haba/baba.txt'
# %%
from os import path, mkdir


class Invoice:
    def __init__(self):
        self.id = False
        self.date = False
        self._amount = False
        self.tax = False
        self.before_tax = False
        self.company_nip = False
        self.station_nip = False

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if value:
            self._amount = self.to_locale(value)
            no_tax = round(value / 1.23, 2)
            self.before_tax = self.to_locale(no_tax)
            self.tax = self.to_locale(value - no_tax)

    def if_exists(self, value):
        return value if value else 'false'

    def to_locale(self, floating_point_number):
        return "{:.2f}".format(round(floating_point_number, 2))

    def set_nips(self, nips):
        if nips:
            self.station_nip = nips[0]
            if len(nips) > 1:
                self.company_nip = nips[1]

    def to_file(self, name):
        try:
            base = path.splitext(name)[0].strip()
            if path.basename(base) == '':
                raise OSError('Podaj pełną ścieżkę razem z nazwą pliku')
            dirname = path.dirname(base)
            if not path.isdir(dirname):
                mkdir(dirname)
            name = base + '.xml'
            with open(name, 'w') as file:
                file.write(self.to_xml_item())
        except IOError as ioerror:
            print('Wystąpił błąd podczas zapisywania pliku xml.',
                  'Upewnij się że posiadasz konieczne uprawnienia',
                  'do zapisu w tym miejscu.\n', ioerror)
        except OSError as oserror:
            print('Wystąpił błąd modułu os.',
                  'Upewnij się że podana ścieżka jest prawidłowa.\n', oserror)

    def to_xml_item(self):
        return ('<Faktura>\n'
                '  <KodWaluty>PLN</KodWaluty>\n'
                f'  <P_1>{self.if_exists(self.date)}</P_1>\n'
                f'  <P_2A>{self.if_exists(self.id)}</P_2A>\n'
                # '  <P_3A>false</P_3A>\n'
                # '  <P_3B>false</P_3B>\n'
                # '  <P_3C>false</P_3C>\n'
                # '  <P_3D>false</P_3D>\n'
                f'  <P_4B>{self.if_exists(self.station_nip)}</P_4B>\n'
                f'  <P_5B>{self.if_exists(self.company_nip)}</P_5B>\n'
                # '  <P_13_1>{self.if_exists(self.before_tax)}</P_13_1>\n'
                # '  <P_14_1>{self.if_exists(self.tax)}</P_14_1>\n'
                # '  <P_14_1W>{self.if_exists(self.tax)}</P_14_1W>\n'
                # '  <P_13_2>0.00</P_13_2>\n'
                # '  <P_14_2>0.00</P_14_2>\n'
                # '  <P_14_2W>0.00</P_14_2W>\n'
                # '  <P_13_3>0.00</P_13_3>\n'
                # '  <P_14_3>0.00</P_14_3>\n'
                # '  <P_14_3W>0.00</P_14_3W>\n'
                # '  <P_13_6>0.00</P_13_6>\n'
                # '  <P_13_7>0.00</P_13_7>\n'
                f'  <P_15>{self.if_exists(self.amount)}</P_15>\n'
                # '  <P_16>false</P_16>\n'
                # '  <P_17>false</P_17>\n'
                # '  <P_18>false</P_18>\n'
                # '  <P_18A>false</P_18A>\n'
                # '  <P_19>false</P_19>\n'
                # '  <P_20>false</P_20>\n'
                # '  <P_21>false</P_21>\n'
                # '  <P_22>false</P_22>\n'
                # '  <P_23>false</P_23>\n'
                # '  <P_106E_2>false</P_106E_2>\n'
                # '  <P_106E_3>false</P_106E_3>\n'
                # '  <RodzajFaktury>VAT</RodzajFaktury>\n'
                '</Faktura>')


if __name__ == '__main__':
    xml = Invoice()
    print(xml.to_xml_item())
    xml.amount = 12.3
    xml.date = '1997-04-03'
    xml.set_nips(['111-111-11-11', '222-222-22-22'])
    xml.to_file('try_me')

# %%
