import random
import re
from statistics import mode
import numpy as np
import math
import os
from sklearn.metrics import accuracy_score, precision_recall_fscore_support


class Node:
    def __init__(self, checking_feature_idx=None, is_leaf=False, category=None, idx_features=None):
        self.checking_feature_idx = checking_feature_idx  # to index sto opoio brisketai to index ths idiothtas me to max IG
        self.left_child = None
        self.right_child = None
        self.is_leaf = is_leaf  # an eimaste se fylo opote einai positive h negative to review
        self.category = category  # positive or negative (1 or 0)


class ID3RandomForest:
    def __init__(self, features, num_of_trees=10, max_depth=6):
        self.forest = []  # lista me ta dentra tou random forest
        self.features = features  # lexilogio
        self.num_of_trees = num_of_trees
        self.max_depth = max_depth

    def fit(self, x, y):
        for i in range(self.num_of_trees):  # gia kathe dentro
            # ftiaxno ena bootstrapped deigma apo ta dedomena
            indices = [random.randint(0, len(x) - 1) for i in range(len(x))]
            x_sample = x[indices]
            y_sample = y[indices]

            # dialexe tyxaia ena yposynolo apo tis lexeis
            total_features = len(self.features)
            subset_size = int(math.sqrt(total_features)) # prossegisi rizas gia tin posotita twn features pou tha laboume ypopsi
            # subset_size = int(0.5 * total_features) posa features tha paroume kathe fora (50% toy synolou) diaforetiki prosegisi
            # subset_size = int(math.log2(total_features)) + 1 diaforetiki proseggisi log2
            all_features_indices = range(
                total_features)  # akolouthia apo to 0 mexri to total features - 1 (ta indices ths kathe lexhs)

            selected_features = random.sample(all_features_indices,
                                              k=subset_size)  # apo ta indices twn lexewn pare tyxaia tosa oso to k
            most_common = mode(y.flatten())
            tree = self.create_tree(x_sample, y_sample, features=np.array(selected_features), category=most_common)
            self.forest.append(tree)
        return self.forest

    def create_tree(self, x_train, y_train, features, category, current_depth=0):
        # check empty data

        if self.max_depth is not None and current_depth >= self.max_depth: # elegxoume an exoume yperbei to megisto bathos wste na stamatisei h kataskeui tou dentrou
            return Node(checking_feature_idx=None, is_leaf=True, category=category)
        if len(x_train) == 0:
            return Node(checking_feature_idx=None, is_leaf=True, category=category)  # decision node

        # check all examples belonging in one category
        if np.all(y_train.flatten() == 0):
            return Node(checking_feature_idx=None, is_leaf=True, category=0)
        elif np.all(y_train.flatten() == 1):
            return Node(checking_feature_idx=None, is_leaf=True, category=1)

        if len(features) == 0:
            return Node(checking_feature_idx=None, is_leaf=True, category=mode(y_train.flatten()))

        igs = list()
        for feat_index in features.flatten():
            igs.append(self.calculate_ig(y_train.flatten(), [example[feat_index] for example in x_train]))

        max_ig_idx = np.argmax(np.array(igs).flatten())
        m = mode(y_train.flatten())  # most common category

        root = Node(checking_feature_idx=max_ig_idx, idx_features=features)

        # data subset with X = 0
        x_train_0 = x_train[x_train[:, max_ig_idx] == 0, :]
        y_train_0 = y_train[x_train[:, max_ig_idx] == 0].flatten()

        # data subset with X = 1
        x_train_1 = x_train[x_train[:, max_ig_idx] == 1, :]
        y_train_1 = y_train[x_train[:, max_ig_idx] == 1].flatten()

        new_features_indices = np.delete(features.flatten(), max_ig_idx)  # remove current feature (auto eixa apo ergastirio kai den leitourgouse)

        root.left_child = self.create_tree(x_train=x_train_1, y_train=y_train_1, features=new_features_indices,
                                           category=m, current_depth=current_depth + 1)  # go left for X = 1 positive
        if x_train[0, max_ig_idx] == 0 and x_train[1, max_ig_idx] == 0:  # Check if the feature value is 0 for both examples
            root.right_child = Node(checking_feature_idx=None, is_leaf=True, category=m)
        else:
            root.right_child = self.create_tree(x_train=x_train_0, y_train=y_train_0, features=new_features_indices,
                                                category=m, current_depth=current_depth + 1)  # go right for X = 0 negative
        return root

    @staticmethod
    def calculate_ig(classes_vector,
                     feature):  # einai h euretiki ypologizei to IG information gain apo ton typo HC - HC_IDIOTHTAS_TREXOUSAS
        classes = set(classes_vector)

        HC = 0
        for c in classes:
            PC = list(classes_vector).count(c) / len(classes_vector)  # P(C=c)
            HC += - PC * math.log(PC, 2)  # H(C)
            # print('Overall Entropy:', HC)  # entropy for C variable

        feature_values = set(feature)  # 0 or 1 in this example
        HC_feature = 0
        for value in feature_values:
            # pf --> P(X=x)
            pf = list(feature).count(value) / len(feature)  # count occurences of value
            indices = [i for i in range(len(feature)) if feature[i] == value]  # rows (examples) that have X=x

            classes_of_feat = [classes_vector[i] for i in indices]  # category of examples listed in indices above
            for c in classes:
                # pcf --> P(C=c|X=x)
                pcf = classes_of_feat.count(c) / len(classes_of_feat)  # given X=x, count C
                if pcf != 0:
                    # - P(X=x) * P(C=c|X=x) * log2(P(C=c|X=x))
                    temp_H = - pf * pcf * math.log(pcf, 2)
                    # sum for all values of C (class) and X (values of specific feature)
                    HC_feature += temp_H

        ig = HC - HC_feature
        return ig

    def predict(self, x):
        predicted_classes = list()  # lista me ta predictions kathe example

        for unlabeled in x:  # for every example
            tree_predictions = list()  # initialize gia kathe paradeigma lista me prediction kathe dentrou
            for tree in self.forest:  # tsekare kathe dentro
                tmp = tree  # begin at root
                while not tmp.is_leaf:
                    if unlabeled[tmp.checking_feature_idx] == 1:
                        tmp = tmp.left_child
                    else:
                        tmp = tmp.right_child
                tree_predictions.append(tmp.category)  # ti prediction dinei kai balto sti lista

            predicted_classes.append(mode(
                tree_predictions))  # telika pare to syxnotero (0 h 1) kai balto sti lista me ta predictions tou ekastote paradeigmatos

        return np.array(
            predicted_classes)  # kanei return ena pinaka opou gia kathe review tou x exei mesa 0 h 1 (negative h positive)\


class Naive_Bayes:
    def __init__(self):
        self.class_priors = None
        self.word_probs = None

    def train_naive_bayes(self, train_reviews, train_labels):
        # Ypologismos arithmou eggrafwn kai arithmwn leksewn
        n_docs = len(train_reviews)
        n_words = len(train_reviews[0])
        # Apothikeush twn labels gia
        classes = set(train_labels)

        # init class priors kai word probs
        self.class_priors = {cls: 0 for cls in classes}
        self.word_probs = {cls: [1] * n_words for cls in classes}

        # Ypologismos class_priors kai word_probs
        for doc, label in zip(train_reviews, train_labels):
            self.class_priors[label] += 1
            for i, word in enumerate(doc):
                self.word_probs[label][i] += word

        # Kanonikopoihsh class_priors kai word_probs
        for cls in classes:
            self.class_priors[cls] /= n_docs
            total_words = sum(self.word_probs[cls])
            self.word_probs[cls] = [word / total_words for word in self.word_probs[cls]]

        return self.class_priors, self.word_probs

    # predict vash tou Naive Bayes Classifier
    def predict(self, x):
        # Adeia lista gia apothikeush predictions
        predicted_classes = list()

        # lipsi klasewn apo ta class priors
        classes = self.class_priors.keys()
        for unlabeled in x:
            # arxikopoihsei flags gia max class (= None) kai gia max prob = - apeiro
            max_class, max_prob = None, float('-inf')

            # Euresh highest probability
            for cls in classes:
                log_prob = np.log(self.class_priors[cls])
                for i, word in enumerate(unlabeled):
                    # Aukshsh probability bash lekseis
                    if word:
                        log_prob += np.log(self.word_probs[cls][i])
                    else:
                        log_prob += np.log(1 - self.word_probs[cls][i])

                # An > max tote neo max
                if log_prob > max_prob:
                    max_class, max_prob = cls, log_prob
            predicted_classes.append(max_class)

        return np.array(predicted_classes)


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
