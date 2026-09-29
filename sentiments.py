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
    return dict(zip(result['labels'], result['scores']))

def classify_essential(text):
    the_text = text
    candidate_labels = ['the availability or the cost of any of: housing, transportation, groceries, or healthcare',
                         'uncertainty or uncertainty in general', 
                         'how households or ordinary consumers are affected']
    result = classifier(the_text, candidate_labels, multi_label = True,
                        hypothesis_template = "This text discusses {}.")
    return dict(zip(result['labels'], result['scores']))

def classify():
    text_data = df['lead_text'].dropna().tolist()
    text = input("Structural or essential? ")
    if text.lower().strip() == "structural":
        for text in text_data:
            result = classify_structural(text)
            print(result)
    elif text.lower().strip() == "essential":
        for text in text_data:
            result = classify_essential(text)
            print(result)
    else:
        print("Invalid input. Please enter 'structural' or 'essential'.")

classify()
    