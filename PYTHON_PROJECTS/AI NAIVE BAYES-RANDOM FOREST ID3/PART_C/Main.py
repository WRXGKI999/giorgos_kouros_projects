import re
import numpy as np
from methods import load_imdb_data, calculate_metrics
import matplotlib.pyplot as plt
from tqdm import tqdm
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, SimpleRNN, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

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
    n = 50 # paraleipsh n syxnoterwn
    k = 100  # paraleipsh k spanioterwn
    data_dir = 'C:/Users/geoko/Desktop/AUEB/5TH SEMESTER/Τεχνητη Νοημοσυνη/aclImdb_v1/aclImdb/train'
    test_data_dir = 'C:/Users/geoko/Desktop/AUEB/5TH SEMESTER/Τεχνητη Νοημοσυνη/aclImdb_v1/aclImdb/test'
    # peiramatizomaste me ta training data sizes
    training_sizes = [100, 500, 1000, 5000]  # posa reviews tha einai ta dedomena ekpaideushs kathe fora ( 400 = 200 pos kai 200 neg)

# FORTONW ORISMENO ARITHMO TEST DEDOMENA
test_reviews, test_categories = load_imdb_data(test_data_dir,
                                      1000)  # fortono kapoia test, ( edo 1000 positive kai 1000 negative) me ta labels tous

# listes accuracy precision recall F1 training dedomena
accuracy_scores_train = []
precision_scores_train = []
recall_scores_train = []
f1_scores_train = []

# listes accuracy precision recall F1 test dedomena
accuracy_scores_test = []
precision_scores_test = []
recall_scores_test = []
f1_scores_test = []

# listes sfalmatwn sta dedomena ekpaideushs kai anaptyxis
train_loss = []
val_loss = []

for size in training_sizes:
    reviews, categories = load_imdb_data(data_dir, int(size/2))  # fortono ta reviews me limit = size/2 opou pos reviews + neg reviews = size
    train_doc_length = 0
    for doc in tqdm(reviews):
        tokens = str(doc).split()
        train_doc_length += len(tokens)
    maxlen = int(train_doc_length/len(reviews)) # number which will be used as the length of the sequence that will be passed into the network
    vocab_size = m # oso exoume orisei oti theloume na einai to m apo ta merh A kai B pou antriprosopeuei ton arithmo twn lexewn pou en telei tha xrisimopoihsoume

    #kataskeuazw training data se akolouthia akeraiwn anti gia text
    tokenizer = Tokenizer(num_words=vocab_size) # initialize to vocabulary me megisto arithmo lexewn = vocab_size
    tokenizer.fit_on_texts(reviews) # bres monadikes lexeis kai dose tous integer IDs
    sequences_train = tokenizer.texts_to_sequences(reviews) # convert ta text reviews se akolouthies apo akeraious
    x_train = pad_sequences(sequences_train, maxlen=maxlen) # iso megethos gia kathe akolouthia = maxlen
    y_train = np.array(categories)

    #kataskeuazw test data se akolouthia akeraiwn anti gia text
    sequences_test = tokenizer.texts_to_sequences(test_reviews)
    x_test = pad_sequences(sequences_test, maxlen=maxlen)
    y_test = np.array(test_categories)

    embedding_dim = 200  # allazoume xeirokinita, megethos word embedding
    rnn_units = 100  # allazoume xeirokinita

    model = Sequential()
    model.add(Embedding(vocab_size, embedding_dim, input_length=maxlen))
    model.add(SimpleRNN(rnn_units))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='adam', loss='binary_crossentropy')

    history = model.fit(x_train, y_train, epochs=10, validation_split=0.2)  # tis epoxes tis allazoume xeirokinita, 80% train 20% validate

    # sfalmata ekpaideusis-anaptyxis gia to trexon training data size
    train_loss.append(history.history['loss'])
    val_loss.append(history.history['val_loss'])

    train_results = (model.predict(x_train) > 0.5).astype("int32")
    test_results = (model.predict(x_test) > 0.5).astype("int32")
    # ypologizo tis times accuracy precision recall f1 gia training data
    metrics_train = calculate_metrics(y_train, train_results)

    # ypologizo tis times kai gia test data
    metrics_test = calculate_metrics(y_test, test_results)

    # ta bazo stis antistoixes listes
    accuracy_scores_train.append(metrics_train[0])
    precision_scores_train.append(metrics_train[1])
    recall_scores_train.append(metrics_train[2])
    f1_scores_train.append(metrics_train[3])

    accuracy_scores_test.append(metrics_test[0])
    precision_scores_test.append(metrics_test[1])
    recall_scores_test.append(metrics_test[2])
    f1_scores_test.append(metrics_test[3])


# edo ftiaxnoume tis kabyles mathisis accuracy precision recall f1 kai loss
plt.figure(figsize=(12, 6))

# accuracy
plt.subplot(2, 3, 1)
plt.plot(training_sizes, accuracy_scores_train, 'o-', label='RNN Training Accuracy')
plt.plot(training_sizes, accuracy_scores_test, 'o-', label='RNN Test Accuracy')
plt.xlabel('Training Size')
plt.ylabel('Accuracy')
plt.title('Learning Curve - RNN Accuracy')
plt.legend()

# precision
plt.subplot(2, 3, 2)
plt.plot(training_sizes, precision_scores_train, 'o-', label='RNN Training Precision')
plt.plot(training_sizes, precision_scores_test, 'o-', label='RNN Test Precision')
plt.xlabel('Training Size')
plt.ylabel('Precision for positive reviews')
plt.title('Learning Curve - RNN Precision positive')
plt.legend()

# recall
plt.subplot(2, 3, 3)
plt.plot(training_sizes, recall_scores_train, 'o-',  label='RNN Training Recall')
plt.plot(training_sizes, recall_scores_test, 'o-',  label='RNN Test Recall')
plt.xlabel('Training Size')
plt.ylabel('Recall for positive reviews')
plt.title('Learning Curve - RNN Recall positive')
plt.legend()

# F1
plt.subplot(2, 3, 4)
plt.plot(training_sizes, f1_scores_train, 'o-',  label='RNN Training F1 Score')
plt.plot(training_sizes, f1_scores_test, 'o-',  label='RNN Test F1 Score')
plt.xlabel('Training Size')
plt.ylabel('F1 Score for positive reviews')
plt.title('Learning Curve - RNN F1 Score positive')
plt.legend()

# Training Loss
plt.subplot(2, 3, 5)
for i, loss_values in enumerate(train_loss):
    plt.plot(range(1, len(loss_values) + 1), loss_values, label=f'Training Size: {training_sizes[i]}')
plt.xlabel('Epochs')
plt.ylabel('Training Loss')
plt.title('Learning Curve - RNN Training Loss')
plt.legend()

# Validation loss
plt.subplot(2, 3, 6)
for i, loss_values in enumerate(val_loss):
    plt.plot(range(1, len(loss_values) + 1), loss_values, label=f'Training Size: {training_sizes[i]}')
plt.xlabel('Epochs')
plt.ylabel('Validation Loss')
plt.title('Learning Curve - RNN Validation Loss')
plt.legend()

plt.tight_layout()
plt.show()



# ektypwnoume pinakes me pososta accuracy, precision, recall & F1 gia kathe timi training size ths listas

for i in range(len(training_sizes)):
    print(f"\nRESULTS FOR TRAINING DATA SIZE = {training_sizes[i]}")
    print("\nTraining Data:")
    print(f"Accuracy: {accuracy_scores_train[i] * 100:.2f}%")
    print(f"Precision for positive reviews: {precision_scores_train[i] * 100:.2f}%")
    print(f"Recall for positive reviews: {recall_scores_train[i] * 100:.2f}%")
    print(f"F1 Score for positive reviews: {f1_scores_train[i] * 100:.2f}%")

    print("\nTest Data:")
    print(f"Accuracy: {accuracy_scores_test[i] * 100:.2f}%")
    print(f"Precision for positive reviews: {precision_scores_test[i] * 100:.2f}%")
    print(f"Recall for positive reviews: {recall_scores_test[i] * 100:.2f}%")
    print(f"F1 Score for positive reviews: {f1_scores_test[i] * 100:.2f}%")

