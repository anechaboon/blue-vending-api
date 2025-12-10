import firebase_admin
from firebase_admin import credentials, firestore

# โหลด service account JSON (ควรใช้ ENV ชี้ path)
cred = credentials.Certificate("serviceAccountKey.json")

# initialize app แค่ครั้งเดียว
try:
    firebase_admin.initialize_app(cred)
except ValueError:
    # app ถูก initialize ไปแล้ว (กัน error เวลา reload)
    pass

db = firestore.client()
