from GenAns import QAModel

class Chat:
    def __init__(self):
        self.messages = []
        self.qa_model = QAModel() # use pool

    def add_context(self, context):
        self.qa_model.add_context(context)
        self.messages.append({'Context': context})

    def add_message(self, question):
        answer = self.qa_model.answer(question)
        self.messages.append({question, answer})
        return answer

    def __str__(self):
        st = ""
        for msg in self.messages:
            st += msg['question'] + msg['answer']
        return st

class DataStore:

    def __init__(self):
        self.data = {}
        self.current_user_id = 0

    def insert_user(self, context):

        self.current_user_id += 1
        user_id = str(self.current_user_id)
        self.data[user_id] = Chat()
        self.data[user_id].add_context(context)

        return user_id

    def insert_message(self, uid, question):
        user_id = str(uid)
        if user_id not in self.data:
            self.data[user_id] = Chat()

        answer = self.data[user_id].add_message(question)
        return answer


    def get_chat(self, user_id):
        return self.data.get(user_id, None)

    def __str__(self):
        st = ""
        for k, v in self.data.items():
            st += str(k) + v.__str__()+'\n'
        return st
