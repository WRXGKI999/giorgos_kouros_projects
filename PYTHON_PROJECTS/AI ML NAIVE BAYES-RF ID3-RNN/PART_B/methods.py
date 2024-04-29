import re
import numpy as np
import os
from sklearn.metrics import accuracy_score, precision_recall_fscore_support


def normalize(text): # methodos oste na dioxoume eidikous xaraktires kai na exoume lexeis mono, arithmous kai kena
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    return text.lower() # metatrepoyme oles tis lexeis wste na min uparxoun kefalaia grammata, mono peza


def load_imdb_data(data_dir, limit):
    reviews = []
    labels = []
    flag = 0  # px limit = 100 simainei pernei san training data 100 positive kai 100 negative

    for category in ['pos', 'neg']:
        category_dir = os.path.join(data_dir, category)
        for filename in os.listdir(category_dir):
            if flag < limit:
                if filename.endswith(".txt"):
                    filepath = os.path.join(category_dir, filename)
                    with open(filepath, 'r', encoding='utf-8') as file:
                        review = file.read()
                    reviews.append(normalize(review).lower())
                    labels.append(1 if category == 'pos' else 0)
                    flag += 1
            else:
                flag = 0  # kanto 0 gia ta #limit iterates twn neg
                break

    return reviews, labels


def vectorizer(reviews, features):  # metatrepo ton pinaka x me ta reviews se dianysmatiki morfi
    X_train = []

    for review in reviews:
        words = re.findall(r'\b\w+\b', review)
        vector = [1 if word in words else 0 for word in features]
        X_train.append(vector)

    return np.array(X_train)


def extract_features(reviews, m, n, k):  # orismos lexilogiou apo apo n syxnoterh mexri
    word_counts = {}

    # metra gia kathe lexh poses fores uparxei se ola ta reviews
    for review in reviews:
        words = re.findall(r'\b\w+\b', review)
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1

    # taxinomisi bash syxnotitas
    sorted_words = sorted(word_counts.items(), key=lambda sorted_by: sorted_by[1], reverse=True)
    sorted_words = sorted_words[n:-k]  # exclude ta n syxnotera kai ta k spaniotera
    features = [word for word, count in sorted_words[:m]]  # sth synexeia pare ta m syxnotera apo auta

    return features


def calculate_metrics(y_true, y_pred):  # synarthsh ypologismou accurancy, precision, recall, F1
    accuracy = accuracy_score(y_true, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='binary', pos_label=1,
                                                               zero_division=1)  # precision recall f1 mono gia positive
    return accuracy, precision, recall, f1
