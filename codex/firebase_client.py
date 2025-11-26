import firebase_admin
from firebase_admin import credentials, firestore
from django.conf import settings

# Configuraciones de Firebase.Str
if not firebase_admin._apps:
    cred = credentials.Certificate(str(settings.FIREBASE_SERVICE_ACCOUNT))
    firebase_admin.initialize_app(cred, {
        "projectId": settings.FIREBASE_PROJECT_ID,
    })

db = firestore.client()
