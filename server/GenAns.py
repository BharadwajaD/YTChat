import os
from transformers import pipeline, AutoTokenizer, AutoModel
from openai import OpenAI
import torch

class QAModel:
    #TODO: Some better models instead of roberta to generate answer
    def __init__(self, top_k = 3, isOpenai = False, embedding_model="distilbert-base-cased-distilled-squad", answering_model="deepset/roberta-base-squad2"):

        self.top_k = top_k
        self.openai_key = os.environ.get('API_KEY')
        self.openai_client = OpenAI(api_key = self.openai_key)
        self.isOpenai = isOpenai

        self.embedder_tokenizer = AutoTokenizer.from_pretrained(embedding_model)
        self.embedder_model = AutoModel.from_pretrained(embedding_model)

        self.answering_pipeline = pipeline("question-answering", model=answering_model, tokenizer=answering_model)


    def add_context(self, context):
        self.context = context
        self.sentences = self.split_into_sentences(context)
        self.context_embeddings = self.compute_embeddings(self.sentences, True)


    def split_into_sentences(self, context):
        # Split the context into sentences
        sentences = context.split("::")  # You may need a more sophisticated sentence tokenizer
        return sentences

    # compute embeddings for the given sentences
    def compute_embeddings(self, sentences, isContext = False):

        # embeddings for context
        context_embeddings = []
        for sentence in sentences:
            inputs = self.embedder_tokenizer(sentence, return_tensors="pt", max_length=512, truncation=True)
            outputs = self.embedder_model(**inputs)
            embeddings = torch.mean(outputs.last_hidden_state, dim=1).squeeze().detach()
            context_embeddings.append(embeddings)

        if isContext:
            return context_embeddings
        else:
            return context_embeddings[0]


    def extract_top_k_similar_sentences(self, question_embedding):
        # Ensure that both tensors have the same dimension
        question_embedding = question_embedding.unsqueeze(0)

        # Calculate cosine similarity between question and context sentences
        similarities = [torch.nn.functional.cosine_similarity(question_embedding, context_embedding.unsqueeze(0)) for context_embedding in self.context_embeddings]

        # Convert the similarities to a NumPy array before sorting
        similarities_np = torch.tensor(similarities).numpy()

        # Extract top k similar sentences
        top_k_indices = sorted(range(len(similarities_np)), key=lambda i: similarities_np[i], reverse=True)[:self.top_k]
        top_k_sentences = [self.sentences[i] for i in top_k_indices]

        return top_k_sentences

    def answer(self, question):


        if self.isOpenai:

            response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo-16k",
                    messages=question,
                    )
            answer = response.choices[0].message.content
            return answer


        question_embedding = self.compute_embeddings([question])
        top_k_sentences = self.extract_top_k_similar_sentences(question_embedding)
        # Concatenate top k similar sentences with the question to form a new context
        new_context = ". ".join(top_k_sentences) + ". " + question

        answer = self.answering_pipeline({
            'question': question,
            'context': new_context
            })

        return answer['answer']


