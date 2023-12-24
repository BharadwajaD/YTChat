class Chat():

    chat = []

    def __init__(self):
        pass

    def chat_insert(self, question, answer):
        self.chat.append({'question': question, 'answer': answer})

class DataStore():

    store = {}
    idx = 0

    def new_user(self):
        self.idx += 1
        self.store[self.idx] = Chat()
        return self.idx

    def get_user(self, uid):
        return self.store.get(int(uid))


    def __str__(self):
        return self.store

