# %%
import pyrebase
import os


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
            Firebase.__instance = self

    @staticmethod
    def getInstance():
        if Firebase.__instance is None:
            Firebase()
        return Firebase.__instance

    def get_img(self, storage_path, output_path):
        pass


if __name__ == '__main__':
    fb = Firebase.getInstance()
    storage = fb.storage

    test_img_path = 'images/test/test[1].jpg'
    storage.child(test_img_path).download(
        os.path.join('images', 'test[1].jpg'))

# %%
