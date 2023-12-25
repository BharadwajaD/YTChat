from transformers import pipeline
from openai import OpenAI
import os


class QAModel():

    # TODO: The 'openai.key' option isn't read in the client API. You will need to pass it when you instantiate the client, e.g. 'OpenAI(key='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')'
    key = os.environ.get('API_KEY')


    def __init__(self):

        self.client = OpenAI(api_key=self.key)

        self.prompt = """ I will give you context which includes the transcript
        of the video and the history of questions and answers. Based on this context
        you need to answer the given question.
        Context:{}
        Question:{}"""

    def answer(self, context, question):
        prompt = self.prompt.format(context, question)
        response = self.client.completions.create(model='gpt-3.5-turbo-instruct',
        prompt=prompt,
        max_tokens=50)
        return response.choices[0].text.strip()
