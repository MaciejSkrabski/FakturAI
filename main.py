# %%

import numpy as np
import pytesseract
import argparse
import matplotlib as mpl
from os import path
from matplotlib import pyplot as plt
from connectivity import Firebase
from image_manipulation import (
    to_greyscale,
    simple_thresh,
    binarize,
    plt_gray,
    open_image,
    )
from regular_expressions import RegularExpressions
from class_xml import Invoice

mpl.rcParams['figure.dpi'] = 300


def tesseract_read(im_path, method='otsu', lang="pol", is_plot=False):
    im = open_image(im_path)
    grey = to_greyscale(np.asarray(im, dtype='float32'))/255
    thresh = simple_thresh(grey, method)
    binarized = binarize(grey, thresh)
    if is_plot:
        plt_gray(grey)
        plt.show()
        plt_gray(binarized)
        plt.show()

    text = pytesseract.image_to_string(binarized, lang=lang)
    return text


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('plik',
                        help='nazwa/ścieżka pliku z którego program ma czytać')
    parser.add_argument('--email', '-m',
                        help="Zaloguj się tym adresem email"
                             " (zarejestrowanym wcześniej w"
                             " aplikacji mobilnej).")
    parser.add_argument('--lokalny', '-l', action='store_true',
                        help="Przełącznik, użycie powoduje ignorowanie"
                             " \'--email\'. Obraz będzie wczytany z"
                             "lokalizacji na tym komputerze.",
                        required=False)
    parser.add_argument('--wyjscie', '-w',
                        help="Nazwa/ścieżka do której program ma zapisać"
                             " plik wyjściowy o formacie zgodnym z JPK."
                             " Domyślnie ta sama nazwa/ścieżka co \'plik\'.")
    parser.add_argument('--rysuj', '-r', action='store_true',
                        help="Użycie spowoduje rysowanie obrazków."
                             "Dobry sposób na porównanie jakości"
                             "progowania z argumentu -p")
    parser.add_argument('--progowanie', '-p', type=str, default='otsu',
                        choices=['srednia', 'mediana', 'li', 'otsu'],
                        help='Określa metodę progowania.'
                             ' Do wyboru: srednia, mediana,'
                             ' otsu, li. Domyślnie: otsu.')

    args = parser.parse_args()
    metoda = {
        'srednia': 'mean',
        'mediana': 'median',
        'li': 'li',
        'otsu': 'otsu',
    }[args.progowanie]

    if args.email and not args.lokalny:
        fb = Firebase.getInstance()
        fb.login(args.email)
        local = path.join('pobrane', args.plik)
        fb.get_img(args.plik)

    if args.lokalny or not args.email:
        local = args.plik

    if args.wyjscie:
        output = args.wyjscie
    else:
        output = local

    text = tesseract_read(local, method=metoda, is_plot=args.rysuj)
    invoice = Invoice()
    re_obj = RegularExpressions()

    invoice.id = re_obj.get_match(text, 'id')
    invoice.date = re_obj.get_match(text, 'dates')
    invoice.set_nips(re_obj.get_match(text, 'nips'))
    invoice.amount = re_obj.get_match(text, 'amount')

    invoice.to_file(output)


# %%
