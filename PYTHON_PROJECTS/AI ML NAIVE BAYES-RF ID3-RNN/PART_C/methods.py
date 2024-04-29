import re
import os
from sklearn.metrics import accuracy_score, precision_recall_fscore_support


def normalize(text): # methodos oste na dioxoume eidikous xaraktires kai na exoume lexeis mono, arithmous kai kena
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    return text.lower() # metatrepoyme oles tis lexeis wste na min uparxoun kefalaia grammata, mono peza


def load_imdb_data(data_dir, limit):
    reviews = []
    labels = []
    #flag = 0  # px limit = 100 simainei pernei san training data 100 positive kai 100 negative AXREIASTO TO KANO MESA STI FOR GIA KATHE KATIGORIA

    for category in ['pos', 'neg']:
        flag = 0
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
                #flag = 0  # kanto 0 gia ta #limit iterates twn neg AXREIASTO TO KANO PIO PANO 0 GIA KATHE KATIGORIA (OTAN EBAZA LIMIT>=12.500 DEN EBAINE POTE EDO
                # ME APOTELESMA TO FLAG NA MIN MIDENIZOTAN KAI NA MIN FORTONE POTE TA NEG REVIEWS EPEIDH EXO SYNOLIKA 12500 POS KAI 12500 NEG
                break

    return reviews, labels


def calculate_metrics(y_true, y_pred):  # synarthsh ypologismou accurancy, precision, recall, F1
    accuracy = accuracy_score(y_true, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='binary', pos_label=1,
                                                               zero_division=1)  # precision recall f1 mono gia positive
    return accuracy, precision, recall, f1
