# %%
import pyrebase
from os import path, mkdir
from getpass import getpass
# %%
# %%


class Firebase():
    __instance = None
    firebaseConfig = {
        'apiKey': "AIzaSyDFxpIbMoz4oMhZByDpq_XqOoO4mjA9gKM",
        'authDomain': "inzynierka-ea1a4.firebaseapp.com",
        'databaseURL': "https://inzynierka-ea1a4.firebaseio.com",
        'projectId': "inzynierka-ea1a4",
        'storageBucket': "inzynierka-ea1a4.appspot.com",
        'messagingSenderId': "702615989279",
        'appId': "1:702615989279:web:2274d328c61247cc53392a",
        'measurementId': "G-ZQFCSH3TER"}

    def __init__(self):
        '''artificially private constructor'''
        if Firebase.__instance is not None:
            raise Exception('SINGLETON REINITIALIZATION!'
                            ' Please don\'t do that.')
        else:
            self.firebase = pyrebase.initialize_app(Firebase.firebaseConfig)
            self.storage = self.firebase.storage()
            self.auth = self.firebase.auth()
            self._user = None

            Firebase.__instance = self

    @staticmethod
    def getInstance():
        if Firebase.__instance is None:
            Firebase()
        return Firebase.__instance

    def login(self, email):
        password = getpass(f'Proszę podać hasło dla konta {email}'
                           ' i potwierdzić klawiszem ENTER:')
        try:
            user = self.auth.sign_in_with_email_and_password(email, password)
            self._user = self.auth.get_account_info(
                user['idToken'])['users'][0]['localId']
        except Exception as e:
            print("Błąd logowania. Upewnij się, że podajesz właściwe dane",
                  "oraz że nawiązanie połączenia jest możliwe.",
                  e)

    def get_img(self, image_name):
        if self._user is None:
            raise Exception("Użytkownik niezalogowany."
                            " Niemożliwe dalsze działanie.")

        output_path = path.join('pobrane', image_name)
        try:
            if not path.exists('pobrane'):
                mkdir('pobrane')
            image_path = f'images/{self._user}/{image_name}'
            self.storage.child(image_path).download(output_path)
        except OSError as oserror:
            print("Błąd biblioteki OSError. Upewnij się, że masz"
                  " uprawnienia do tej ścieżki.\n"
                  f"{oserror}")
        except IOError as ioerror:
            print("IOERROR Błąd przy tworzeniu ścieżki zapisu obrazka.",
                  "Upewnij się, że podajesz właściwą ścieżkę i że",
                  "masz uprawnienia dostępu do niej.\n"
                  f"{ioerror}")

    


if __name__ == '__main__':
    fb = Firebase.getInstance()
    fb.login('tegoproszenieusuwac@test.pl')
    filename = 'test.jpg'
    fb.get_img(filename, 'out/testowy.jpg')
    fb.get_img(filename, '/home/malbik/to/jest/???/zła/;,.,.<>[]/ścieżka.jpg')
# %%
