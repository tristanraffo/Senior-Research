import transformers as transformers, scipy as sp, numpy as np, pandas as pd
import torch as torch, accelerate as accelerate, tqdm as tqdm, spacy as spacy
import sklearn as skl, en_core_web_trf as en_core_web_trf, nltk as nltk
from transformers import pipeline
from sklearn.feature_extraction.text import CountVectorizer
import circlify
import matplotlib.pyplot as plt


classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def classify_structural(text):
    the_text = text
    candidate_labels = ['the public labor market or employment',
                         'uncertainty in the future or uncertainty in general', 
                         'technological, automation, and/or economic restructuring']
    result = classifier(the_text, candidate_labels, multi_label = True,
                        hypothesis_template = "This text discusses {}.")
    return result

def make_bigram_display(relevant_list):
    top_n = 20
    vectorizer = CountVectorizer(ngram_range=(2, 2), stop_words="english")
    counts = vectorizer.fit_transform(relevant_list)
    totals = counts.sum(axis=0).A1
    results = pd.DataFrame({"bigram": vectorizer.get_feature_names_out(), "count": totals})
    results = results.sort_values("count", ascending=False).head(top_n)
    bubble_data = (results.rename(columns={"bigram": "id", "count": "datum"})
    [["id", "datum"]].to_dict(orient="records"))
    circles = circlify.circlify(bubble_data, show_enclosure = False)
    colors = plt.cm.tab20c.colors

    fig, ax = plt.subplots()
    ax.axis("off")
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect("equal")

    for circle, color in zip(circles, colors):
        x, y, r = circle
        ax.add_patch(plt.Circle((x, y), r, color = color))
        ax.annotate(circle.ex["id"].replace(" ", "\n"), (x, y), ha = "center", va = "center")
    plt.show()
    return bubble_data


def make_dictionary():
    df = pd.read_excel(input("Name of your input Excel file (with extension)? "))
    text_data = df['lead_text'].dropna().tolist()
    dictionary = {}
    for text in text_data:
        result = classify_structural(text)
        dictionary[text] = result
        dictionary[text]['relevant'] = all(prob > 0.5 for prob in dictionary[text]['scores'])
        print(dictionary[text]['scores'])
        dictionary[text]['relevant'] = all(prob > 0.5 for prob in dictionary[text]['scores'])
        print(dictionary[text]['relevant'])
    for text in dictionary:
        relevant_list = [text for text in dictionary if dictionary[text]['relevant']]
    make_bigram_display(relevant_list)

make_dictionary()

    