from firebase_admin import firestore
import database.users

class DatabasePoll:
    def __init__(self) -> None:
        self.db = firestore.client()
        self.usersDB = database.users.DatabaseUser()
        
    def create_poll(self, title: str, isUnique: bool, clauses: list, userId: str):
        dictionary = {
            'title': title,
            'isUnique': isUnique,
            'clauses': clauses,
            'createdBy': userId,
            'whoVoted': []
            }
        for i in clauses: 
            dictionary[i] = 0
        doc_ref = self.db.collection('polls').add(
            dictionary
        )
        return doc_ref[1].id
        
        
    def loadPoll(self, pollId):
        check = self.db.collection('polls').stream()
        for i in check:
            if i.id == pollId:
                return i.to_dict()
            
    def updatePoll(self, pollId : str, answers: list, username: str):
        uid = self.usersDB.getUserId(username)
        poll_ref = self.db.collection('polls').document(pollId)
        poll = self.loadPoll(pollId)
        poll['whoVoted'].append(uid)
        for i in answers:
            poll[i] += 1
        poll_ref.set(
            poll, merge=True
        )
