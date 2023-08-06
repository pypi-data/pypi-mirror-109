from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import pickle
import re
from sklearn.metrics.pairwise import cosine_similarity
class TfIdf:
    def load_dataset(self,path_dataset_texts,path_dataset_topics):
        df_dataset_texts=pd.read_csv(path_dataset_texts)
        df_dataset_topics=pd.read_csv(path_dataset_topics)
        df_dataset_topics=df_dataset_topics[['name','topic.id']]
        df_dataset_texts=df_dataset_texts.merge(df_dataset_topics,on='topic.id')
        df_dataset_texts=df_dataset_texts.sort_values('topic.id')
        return df_dataset_texts

    def preprocess_dataset(self,df_dataset_texts):
        def preprocess_text(text):
            text = text.lower()
            text = text.replace("\n", " ").replace("\r", " ")
            text = re.sub(r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+", " ", text)
            return re.sub("[^A-Za-z]+", " ", text).replace("  ", " ")

        df_dataset_texts['text']=df_dataset_texts['text'].apply(preprocess_text)
        return df_dataset_texts

    def __init__(self,path_dataset_texts=None,path_dataset_topics=None,path_model=None,stop_words=None,tokenizer=None):

        if path_dataset_texts!=None and path_dataset_topics!=None:
            self.dataset= self.load_dataset(path_dataset_texts,path_dataset_topics)
            self.dataset=self.preprocess_dataset(self.dataset)
            self.topics= self.dataset['name']

        if path_model != None:
            self.load_model(path_model)
        else:
            self.tf_idf_model = TfidfVectorizer(stop_words='english')
            self.matrix= self.tf_idf_model.fit_transform(self.dataset['text'])
    def create_model_paths(self,path_model):
        path_matrix=path_model+"matrix.pkl"
        path_tfidf_model=path_model+"tfidf-model.pkl"
        path_topics=path_model+"topics.pkl"
        return path_matrix, path_tfidf_model, path_topics

    def load_model(self,path_model):
        path_matrix, path_tfidf_model, path_topics = self.create_model_paths(path_model)
        self.tf_idf_model = pickle.load(open(path_tfidf_model,'rb'))
        self.matrix = pickle.load(open(path_matrix,'rb'))
        self.topics= pickle.load(open(path_topics, 'rb'))

    def dump_model(self,path_model):
        path_matrix, path_tfidf_model, path_topics = self.create_model_paths(path_model)
        pickle.dump(self.tf_idf_model,open(path_tfidf_model,'wb'))
        pickle.dump(self.matrix,open(path_matrix,'wb'))
        pickle.dump(self.topics, open(path_topics,'wb'))
    def model_topic(self,text):
        vector = self.tf_idf_model.transform([text])
        similarity= cosine_similarity(vector,self.matrix)
        similarity_dict= {}
        for i,concept in enumerate(self.topics):
            similarity_dict[concept]=similarity[0,i]
        return similarity_dict




