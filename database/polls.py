from firebase_admin import firestore
import database.users

def create_poll(title: str, isAnonymous: bool, clauses: list, userId: str):
    db = firestore.client()
    dictionary = {
        'title': title,
         'isAnonymous': isAnonymous,
         'clauses': clauses,
         'createdBy': userId,
         'whoVoted': []
         }
    for i in clauses: 
        dictionary[i] = 0
    db.collection('polls').add(
        dictionary
    )
    
    
def loadPoll(pollId):
    print('loading poll...')
    db = firestore.client()
    check = db.collection('polls').stream()
    for i in check:
        if i.id == pollId:
            return i.to_dict()
        
def updatePoll(pollId : str, answers: list, username: str):
    uid = database.users.getUserId(username)
    db = firestore.client()
    poll_ref = db.collection('polls').document(pollId)
    poll = loadPoll(pollId)
    poll['whoVoted'].append(uid)
    for i in answers:
        poll[i] += 1
    poll_ref.set(
        poll, merge=True
    )
