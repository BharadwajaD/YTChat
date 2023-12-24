class Chat:
    def __init__(self):
        self.messages = []

    def add_message(self, question, answer):
        self.messages.append({'question': question, 'answer': answer})

    def __str__(self):
        st = ""
        for msg in self.messages:
            st += msg['question'] + msg['answer']
        return st

class DataStore:

    def __init__(self):
        self.data = {}
        self.current_user_id = 0

    def insert_user(self):

        self.current_user_id += 1
        user_id = self.current_user_id
        self.data[user_id] = Chat()

        return user_id

    def insert_message(self, user_id, question, answer):
        if user_id not in self.data:
            self.data[user_id] = Chat()

        self.data[user_id].add_message(question, answer)

    def get_chat(self, user_id):
        return self.data.get(user_id, None)

    def __str__(self):
        st = ""
        for k, v in self.data.items():
            st += str(k) + v.__str__()+'\n'
        return st
