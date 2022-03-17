from firebase_admin import firestore
def create_user(password: str, username: str):
    """function that creates user"""
    db = firestore.client()
    check = db.collection('users').where('username', '==', username).stream()
    for i in check:
        if password != i.to_dict()['password']:
            return False
        return True
    
    db.collection('users').add({'password': password, 'username': username})
    return True

def checkUser(username: str, password: str):
    db = firestore.client()
    check = db.collection('users').where('username', '==', username).stream()
    for i in check:
        if password != i.to_dict()['password']:
            return False
        return True

def getUserId(username: str):
    db = firestore.client()
    check = db.collection('users').where('email', '==', username).stream()
    for i in check:
        return i.id
