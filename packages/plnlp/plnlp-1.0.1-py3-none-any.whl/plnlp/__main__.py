import logging
from plnlp.utils import read_conll, ModelHelper, write_conll
import sys
import os
import csv

def main(data_train, data_dev):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    logger.info("Loading training data...")
    train = read_conll(data_train)
    logger.info("Done. Read %d sentences", len(train))
    logger.info("Loading dev data...")
    dev = read_conll(data_dev)
    logger.info("Done. Read %d sentences", len(dev))

    helper = ModelHelper.build(train)

    # now process all the input data.
    train_data = helper.vectorize(train)
    dev_data = helper.vectorize(dev)

    cwd = os.getcwd()
    with open(cwd+'/train.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(train_data)

    with open(cwd+'/dev.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(dev_data)

    return train_data, dev_data, helper.tok2id

# class ARGS:
#     data_train = open("/Users/pengluyao/Documents/pypkg/tiny.conll", 'r')
#     data_dev = open("/Users/pengluyao/Documents/pypkg/tiny.conll", 'r')
#     #vocab = open("data/vocab.txt", 'r')
#     #vectors = open("data/wordVectors.txt", 'r')
#
# args = ARGS()
#
# train, dev, train_raw, dev_raw = load_and_preprocess_data(args)

if __name__ == "__main__":
    data_train = open(sys.argv[1], 'r')
    data_dev = open(sys.argv[2], 'r')

    main(data_train, data_dev)