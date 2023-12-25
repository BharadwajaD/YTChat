from transformers import pipeline

class QAModel():

    def __init__(self):
        self.qa_model = pipeline('question-answering')

    def answer(self, context, question):
        print("context: ", context, "\nquestion: ", question)
        return self.qa_model(context=context, question=question)['answer']
