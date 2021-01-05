# %%
import pyrebase
import os


class Firebase():
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
        self.firebase = pyrebase.initialize_app(Firebase.firebaseConfig)
        self.storage = self.firebase.storage()

    def __call__(self):
        return self.firebase


if __name__ == '__main__':
    storage = Firebase().storage
    test_img_path = 'images/test/test[1].jpg'
    storage.child(test_img_path).download(
        os.path.join('images', 'test[1].jpg'))

# %%
