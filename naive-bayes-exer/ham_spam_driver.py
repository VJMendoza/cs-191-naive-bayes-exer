import pandas as pd
import numpy as np
import os
import sys
from sklearn.model_selection import train_test_split

from naive_bayes import NaiveBayes
from driver_helper import main

# datafile = 'vocab.csv'
datafile = 'ham_spam_dataset.csv'

if __name__ == '__main__':
    alpha, reduce, vocab_count_class = main(sys.argv[1:])
    dataset = pd.read_csv(os.path.join(
        sys.path[0], datafile), sep=',', index_col=0, header=0)
    dataset.dropna(how='any', subset=['text'], inplace=True)
    print('----- Data Loaded -----')

    x_train, x_test, y_train, y_test = train_test_split(
        dataset['text'], dataset['ham_or_spam'],
        test_size=0.2, random_state=191, stratify=dataset['ham_or_spam'])

    classes = np.unique(y_train)

    nb = NaiveBayes(classes, float(alpha), reduce, int(vocab_count_class))
    print('----- Training In Progress with alpha = {} -----'.format(nb.alpha))
    nb.train(x_train, y_train)
    print('----- Training Completed with {} words -----'.format(
        nb.vocab_length))

    prob_classes = nb.test(x_test)
    test_acc = np.sum(prob_classes == y_test)/float(y_test.shape[0])

    print('Test Set Accuracy: {:.05%}'.format(test_acc))
