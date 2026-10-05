import transformers as transformers, scipy as sp, numpy as np, pandas as pd
import torch as torch, accelerate as accelerate, tqdm as tqdm, spacy as spacy
import sklearn as skl, en_core_web_trf as en_core_web_trf, nltk as nltk
from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
df = pd.read_excel(input("What is the name of your Excel file (with extension)? "))

def classify_structural(text):
    the_text = text
    candidate_labels = ['the public labor market or employment',
                         'uncertainty in the future or uncertainty in general', 
                         'technological, automation, and/or economic restructuring']
    result = classifier(the_text, candidate_labels, multi_label = True,
                        hypothesis_template = "This text discusses {}.")
    return result

def classify():
    text_data = df['lead_text'].dropna().tolist()
    type = input("Paste or read from Excel? ")
    if(not (type.lower().strip() == 'paste' or type.lower().strip() == 'excel' or type.lower().strip() == 'read')):
         print("Invalid method. Please enter 'paste' or 'Excel'.")
         classify()
         return
    dictionary = {}
    if(type.lower().strip() == 'paste'):
        mytext =input("text: ")
        result = classify_structural(mytext)
        dictionary[mytext] = result
        dictionary[mytext]['relevant'] = all(prob > 0.5 for prob in dictionary[mytext]['scores'])
        print(dictionary[mytext]['relevant'])
    else:
        for text in text_data:
            result = classify_structural(text)
            dictionary[text] = result
            dictionary[text]['relevant'] = all(prob > 0.5 for prob in dictionary[text]['scores'])
            print(dictionary[text]['relevant'])

classify()
    