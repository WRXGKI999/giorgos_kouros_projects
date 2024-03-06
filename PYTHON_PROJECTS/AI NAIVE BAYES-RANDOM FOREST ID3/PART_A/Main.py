import re
import numpy as np
from Algorithms import ID3RandomForest, load_imdb_data, extract_features, vectorizer, Naive_Bayes, calculate_metrics
import matplotlib.pyplot as plt

parameter = int(input("Enter 0 (zero) for default example or 1 for your example : "))
while parameter != 1 and parameter != 0:
    parameter = int(input("Enter 0 (zero) for default example or 1 for your example : "))
if parameter == 1:
    m = int(input("Enter the value of m (number of most frequent words to consider): "))  # m syxnoteres
    n = int(
        input("Enter the value of n (number of words to exclude from the most frequent): "))  # paraleipsh n syxnoterwn
    k = int(input(
        "Enter the value of k (number of words to exclude from the least frequent): "))  # paraleipsh k spanioterwn
    data_dir = input("Enter the path to the training data directory: ")
    test_data_dir = input("Enter the path to the test data directory: ")
    training_sizes_str = input("Enter the training sizes as a list (e.g., [20, 40, 60, 80, 100]): ")
    training_sizes = [int(size) for size in re.findall(r'\b\d+\b', training_sizes_str)]

elif parameter == 0:
    # peiramatizomaste me ta m n k
    m = 10000  # m syxnoteres
    n = 50  # paraleipsh n syxnoterwn
    k = 100  # paraleipsh k spanioterwn
    data_dir = 'C:/Users/geoko/Desktop/AUEB/5TH SEMESTER/Τεχνητη Νοημοσυνη/aclImdb_v1/aclImdb/train'
    test_data_dir = 'C:/Users/geoko/Desktop/AUEB/5TH SEMESTER/Τεχνητη Νοημοσυνη/aclImdb_v1/aclImdb/test'
    # peiramatizomaste me ta training data sizes
    training_sizes = [100, 500, 1000, 5000]  # posa reviews tha einai ta dedomena ekpaideushs kathe fora ( 400 = 200 pos kai 200 neg)

# FORTONW ORISMENO ARITHMO TEST DEDOMENA
test_reviews, labels = load_imdb_data(test_data_dir,
                                      1000)  # fortono kapoia test, ( edo 1000 positive kai 1000 negative) me ta labels tous

# listes accuracy precision recall F1 training dedomena RF ID3
accuracy_scores_train_rf = []
precision_scores_train_rf = []
recall_scores_train_rf = []
f1_scores_train_rf = []

# listes accuracy precision recall F1 test dedomena RF ID3
accuracy_scores_test_rf = []
precision_scores_test_rf = []
recall_scores_test_rf = []
f1_scores_test_rf = []

# listes accuracy precision recall F1 training dedomena NAIVE BAYES
accuracy_scores_train_nb = []
precision_scores_train_nb = []
recall_scores_train_nb = []
f1_scores_train_nb = []

# listes accuracy precision recall F1 test dedomena NAIVE BAYES
accuracy_scores_test_nb = []
precision_scores_test_nb = []
recall_scores_test_nb = []
f1_scores_test_nb = []

for size in training_sizes:
    reviews, categories = load_imdb_data(data_dir,
                                         int(size/2))  # fortono ta reviews me limit = size/2 opou pos reviews + neg reviews = size
    features = extract_features(reviews, m, n, k)  # ftiaxno lexilogio
    X = vectorizer(reviews,
                   features)  # ftiaxno ton pinaka x me ta reviews se dianismatiki morfi bash tou lexilogiou mou
    Y = categories  # labels 1 h 0, positive or negative gia kathe review ston X
    X_test = vectorizer(test_reviews, features)  # kano ton pinaka X me ta test reviews dianysatiko bash lexilogiou

    # EKPAIDEYSH RANDOM FOREST ID3
    trainRFID3 = ID3RandomForest(features, num_of_trees=400, # peiramatizomaste me arithmo dentrwn kai max depth
                                 max_depth=15)  # initialize, orizo kathe fora posa dentra thelo na ftiaxtoun sto dasos kai megisto bathos
    # default times einai 10 dentra me megisto bathos 6
    trainRFID3.fit(np.array(X), np.array(Y))  # algorithmos id3 random forest

    train_resultsRFID3 = trainRFID3.predict(
        X)  # apotelesmata bash tou random forest id3 pou exoume ftiaxei me ta idia ta train data
    test_resultsRFID3 = trainRFID3.predict(
        X_test)  # apotelesmata bash tou random forest id3 pou exoume ftiaxei me kapoia test data

    # Random Forest ypologizo tis times gia training data
    metrics_train_rf = calculate_metrics(Y, train_resultsRFID3)

    # Random Forest ypologizo tis times gia test data
    metrics_test_rf = calculate_metrics(labels, test_resultsRFID3)

    # ta bazo stis antistoixes listes Random Forest
    accuracy_scores_train_rf.append(metrics_train_rf[0])
    precision_scores_train_rf.append(metrics_train_rf[1])
    recall_scores_train_rf.append(metrics_train_rf[2])
    f1_scores_train_rf.append(metrics_train_rf[3])

    accuracy_scores_test_rf.append(metrics_test_rf[0])
    precision_scores_test_rf.append(metrics_test_rf[1])
    recall_scores_test_rf.append(metrics_test_rf[2])
    f1_scores_test_rf.append(metrics_test_rf[3])

    # EKPAIDEYSH NAIVE BAYES
    trainNB = Naive_Bayes()
    trainNB.train_naive_bayes(np.array(X), np.array(Y))

    train_resultsNB = trainNB.predict(X)  # apotelesmata bash tou naive bayes pou exoume ftiaxei
    test_resultsNB = trainNB.predict(X_test)  # apotelesmata bash tou naive bayes pou exoume ftiaxei

    # Naive Bayes ypologizo tis times gia training data
    metrics_train_nb = calculate_metrics(Y, train_resultsNB)

    # Naive Bayes ypologizo tis times gia test data
    metrics_test_nb = calculate_metrics(labels, test_resultsNB)

    # ta bazo stis antistoixes listes Naive Bayes
    accuracy_scores_train_nb.append(metrics_train_nb[0])
    precision_scores_train_nb.append(metrics_train_nb[1])
    recall_scores_train_nb.append(metrics_train_nb[2])
    f1_scores_train_nb.append(metrics_train_nb[3])

    accuracy_scores_test_nb.append(metrics_test_nb[0])
    precision_scores_test_nb.append(metrics_test_nb[1])
    recall_scores_test_nb.append(metrics_test_nb[2])
    f1_scores_test_nb.append(metrics_test_nb[3])

# edo ftiaxnoume tis kabyles mathisis gia Random Forest
plt.figure(figsize=(12, 6))

# accuracy Random forest
plt.subplot(2, 2, 1)
plt.plot(training_sizes, accuracy_scores_train_rf, 'o-', label='RF Training Accuracy')
plt.plot(training_sizes, accuracy_scores_test_rf, 'o-', label='RF Test Accuracy')
plt.xlabel('Training Size')
plt.ylabel('Accuracy')
plt.title('Learning Curve - RF Accuracy')
plt.legend()

# precision Random Forest
plt.subplot(2, 2, 2)
plt.plot(training_sizes, precision_scores_train_rf, 'o-', label='RF Training Precision')
plt.plot(training_sizes, precision_scores_test_rf, 'o-', label='RF Test Precision')
plt.xlabel('Training Size')
plt.ylabel('Precision for positive reviews')
plt.title('Learning Curve - RF Precision positive')
plt.legend()

# recall Random Forest
plt.subplot(2, 2, 3)
plt.plot(training_sizes, recall_scores_train_rf, 'o-',  label='RF Training Recall')
plt.plot(training_sizes, recall_scores_test_rf, 'o-',  label='RF Test Recall')
plt.xlabel('Training Size')
plt.ylabel('Recall for positive reviews')
plt.title('Learning Curve - RF Recall positive')
plt.legend()

# F1 Random Forest
plt.subplot(2, 2, 4)
plt.plot(training_sizes, f1_scores_train_rf, 'o-',  label='RF Training F1 Score')
plt.plot(training_sizes, f1_scores_test_rf, 'o-',  label='RF Test F1 Score')
plt.xlabel('Training Size')
plt.ylabel('F1 Score for positive reviews')
plt.title('Learning Curve - RF F1 Score positive')
plt.legend()

plt.tight_layout()
plt.show()

# edo ftiaxnoume tis kabiles mathisis gia Naive Bayes
plt.figure(figsize=(12, 6))

# accuracy Naive Bayes
plt.subplot(2, 2, 1)
plt.plot(training_sizes, accuracy_scores_train_nb, 'o-',  label='NB Training Accuracy')
plt.plot(training_sizes, accuracy_scores_test_nb, 'o-',  label='NB Test Accuracy')
plt.xlabel('Training Size')
plt.ylabel('Accuracy')
plt.title('Learning Curve - NB Accuracy')
plt.legend()

# precision Naive Bayes
plt.subplot(2, 2, 2)
plt.plot(training_sizes, precision_scores_train_nb, 'o-',  label='NB Training Precision')
plt.plot(training_sizes, precision_scores_test_nb, 'o-',  label='NB Test Precision')
plt.xlabel('Training Size')
plt.ylabel('Precision for positive reviews')
plt.title('Learning Curve - NB Precision positive')
plt.legend()

# recall Naive Bayes
plt.subplot(2, 2, 3)
plt.plot(training_sizes, recall_scores_train_nb, 'o-',  label='NB Training Recall')
plt.plot(training_sizes, recall_scores_test_nb, 'o-',  label='NB Test Recall')
plt.xlabel('Training Size')
plt.ylabel('Recall for positive reviews')
plt.title('Learning Curve - NB Recall positive')
plt.legend()

# F1 Naive Bayes
plt.subplot(2, 2, 4)
plt.plot(training_sizes, f1_scores_train_nb, 'o-',  label='NB Training F1 Score')
plt.plot(training_sizes, f1_scores_test_nb, 'o-',  label='NB Test F1 Score')
plt.xlabel('Training Size')
plt.ylabel('F1 Score for positive reviews')
plt.title('Learning Curve - NB F1 Score positive')
plt.legend()

plt.tight_layout()
plt.show()


# ektypwnoume pinakes Random Forest & Naive Bayes me pososta accuracy, precision, recall & F1 gia thn teleutaia timh training size ths listas

for i in range(len(training_sizes)):
    print(f"\nRESULTS FOR TRAINING DATA SIZE = {training_sizes[i]}")
    print("\nRandom Forest Values:")
    print("\nTraining Data:")
    print(f"Accuracy: {accuracy_scores_train_rf[i] * 100:.2f}%")
    print(f"Precision for positive reviews: {precision_scores_train_rf[i] * 100:.2f}%")
    print(f"Recall for positive reviews: {recall_scores_train_rf[i] * 100:.2f}%")
    print(f"F1 Score for positive reviews: {f1_scores_train_rf[i] * 100:.2f}%")

    print("\nTest Data:")
    print(f"Accuracy: {accuracy_scores_test_rf[i] * 100:.2f}%")
    print(f"Precision for positive reviews: {precision_scores_test_rf[i] * 100:.2f}%")
    print(f"Recall for positive reviews: {recall_scores_test_rf[i] * 100:.2f}%")
    print(f"F1 Score for positive reviews: {f1_scores_test_rf[i] * 100:.2f}%")

    # Print metrics for Naive Bayes
    print("\nNaive Bayes Values:")
    print("\nTraining Data:")
    print(f"Accuracy: {accuracy_scores_train_nb[i] * 100:.2f}%")
    print(f"Precision for positive reviews: {precision_scores_train_nb[i] * 100:.2f}%")
    print(f"Recall for positive reviews: {recall_scores_train_nb[i] * 100:.2f}%")
    print(f"F1 Score for positive reviews: {f1_scores_train_nb[i] * 100:.2f}%")

    print("\nTest Data:")
    print(f"Accuracy: {accuracy_scores_test_nb[i] * 100:.2f}%")
    print(f"Precision for positive reviews: {precision_scores_test_nb[i] * 100:.2f}%")
    print(f"Recall for positive reviews: {recall_scores_test_nb[i] * 100:.2f}%")
    print(f"F1 Score for positive reviews: {f1_scores_test_nb[i] * 100:.2f}%")

