import transformers as transformers, scipy as sp, numpy as np, pandas as pd
import torch as torch, accelerate as accelerate, tqdm as tqdm, spacy as spacy
import sklearn as skl, en_core_web_trf as en_core_web_trf, nltk as nltk
from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def classify_structural(text):
    the_text = text
    candidate_labels = ['the public labor market or employment',
                         'uncertainty in the future or uncertainty in general', 
                         'technological, automation, and/or economic restructuring']
    result = classifier(the_text, candidate_labels, multi_label = True,
                        hypothesis_template = "This text discusses {}.")
    return result

def test():
    dictionary = {}
    df = pd.read_excel(input("Name of your input Excel file (with extension)? ")).dropna()
    shuffled = df.sample(frac=1, random_state=12).reset_index(drop=True)
    n_train = round(len(shuffled) * 0.8)
    articles_80 = shuffled.iloc[:n_train].copy()
    articles_20 = shuffled.iloc[n_train:].copy()
    text_data = articles_80['lead_text'].dropna().tolist()
    relevance = articles_80['relevance'].dropna().tolist()
    run = input("Train or test? ")
    if(run.lower().strip() == 'train'):
        i = 0
        a = 0
        for text in text_data:
            result = classify_structural(text)
            dictionary[text] = result
            dictionary[text]['relevant'] = all(prob > 0.5 for prob in dictionary[text]['scores'])
            dictionary[text]['relevance'] = relevance[i]
            if(dictionary[text]['relevance'].lower().strip() == 'relevant'):
                dictionary[text]['accurate'] = (dictionary[text]['relevant'] == True)
            else:
                dictionary[text]['accurate'] = (dictionary[text]['relevant'] == False)
            dictionary[text]['relevant'] = all(prob > 0.5 for prob in dictionary[text]['scores'])
            if(dictionary[text]['accurate'] == True):
                a += 1
            i += 1
        print("Accuracy: " + str((a/i)*100) + "% on " + str(i) + " articles")
    elif(run.lower().strip() == 'test'):
        i = 0
        a = 0
        for text in articles_20['lead_text'].dropna().tolist():
            result = classify_structural(text)
            dictionary[text] = result
            dictionary[text]['relevant'] = all(prob > 0.5 for prob in dictionary[text]['scores'])
            dictionary[text]['relevance'] = articles_20['relevance'].dropna().tolist()[i]
            if(dictionary[text]['relevance'].lower().strip() == 'relevant'):
                dictionary[text]['accurate'] = (dictionary[text]['relevant'] == True)
            else:
                dictionary[text]['accurate'] = (dictionary[text]['relevant'] == False)
            if(dictionary[text]['accurate'] == True):
                a += 1
            i += 1
        print("Accuracy: " + str((a/i)*100) + "% on " + str(i) + " articles")

test()