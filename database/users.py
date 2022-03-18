from firebase_admin import firestore

class DatabaseUser:
    def __init__(self) -> None:
        self.db = firestore.client()
        
    def create_user(self, password: str, username: str):
        """function that creates user"""
        check = self.db.collection('users').where('username', '==', username).stream()
        for i in check:
            if password != i.to_dict()['password']:
                return False
            return True
        self.db.collection('users').add({'password': password, 'username': username, 'pollsCreated': []})
        return True

    def checkUser(self, username: str, password: str):
        check = self.db.collection('users').where('username', '==', username).stream()
        for i in check:
            if password != i.to_dict()['password']:
                return False
            return True

    def getUserId(self, username: str):
        check = self.db.collection('users').where('username', '==', username).stream()
        for i in check:
            return i.id
        
    def updateUser(self, uid: str, pollId: str):
        user_ref = self.db.collection('users').document(uid)
        updatedUser = user_ref.get().to_dict()
        updatedUser['pollsCreated'].append(pollId)
        user_ref.set(
            updatedUser, merge=True
        )
