from transformers import pipeline

class QAModel():

    def __init__(self):
        # using gpt api will be more better and faster but needs money :(
        self.qa_model = pipeline('question-answering', model='timpal0l/mdeberta-v3-base-squad2')

    def answer(self, context, question):
        return self.qa_model(context=context, question=question)['answer']
