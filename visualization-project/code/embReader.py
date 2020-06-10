import logging
import numpy as np
import gensim
import os
from sklearn.cluster import KMeans

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)


class EmbReader:

    def __init__(self, emb_path, emb_dim=None, wv_type=None):

        glove_emb_path = os.path.join('./pretrained_embeddings/glove.6B/glove.6B.300d.txt')
        word2vec_emb_path = os.path.join('./pretrained_embeddings/GoogleNews-vectors-negative300.txt')

        ##########Glove
        self.embeddings_index = {}
        if wv_type == "glove" or wv_type == "both":
            f = open(glove_emb_path)
            for line in f:
                values = line.split()
                word = values[0]
                coefs = np.asarray(values[1:], dtype='float32')
                self.embeddings_index[word] = coefs
            f.close()
        elif wv_type == "word2vec_finetune":
            f = open(word2vec_emb_path)
            for line in f:
                values = line.split()
                word = values[0]
                coefs = np.asarray(values[1:], dtype='float32')
                self.embeddings_index[word] = coefs
            f.close()

            logger.info('Found %s word vectors.' % len(self.embeddings_index))

        ############
        self.embeddings = {}
        emb_matrix = []

        logger.info('Loading embeddings from: %s', emb_path)

        if wv_type in ["both", "glove", "w2v", "word2vec_finetune"]:  # Check this again
            model = gensim.models.Word2Vec.load(emb_path)
        else:  # glove_finetuned
            model = gensim.models.KeyedVectors.load_word2vec_format(emb_path, binary=False)

        self.emb_dim = emb_dim

        for word in model.wv.vocab:
            if wv_type == "both":
                self.embeddings[word] = list(np.concatenate((model[word], self.get_glove_or_none(word))))
                emb_matrix.append(list(np.concatenate((model[word], self.get_glove_or_none(word)))))
            elif wv_type == "glove":
                self.embeddings[word] = list((self.get_glove_or_none(word)))
                emb_matrix.append(list(self.get_glove_or_none(word)))
            elif wv_type == "w2v" or wv_type == "glove_finetuned":
                self.embeddings[word] = list(model[word])
                emb_matrix.append(list(model[word]))
            elif wv_type == "word2vec_finetune":
                self.embeddings[word] = list(self.get_word2vec_or_none(word))
                emb_matrix.append(list(self.get_word2vec_or_none(word)))

        self.vector_size = len(self.embeddings)
        self.emb_matrix = np.asarray(emb_matrix)

        logger.info('  #vectors: %i, #dimensions: %i' % (self.vector_size, self.emb_dim))

    def get_glove_or_none(self, word):
        embedding_vector = self.embeddings_index.get(word)
        if embedding_vector is None:
            return [0] * 300
        return embedding_vector

    def get_word2vec_or_none(self, word):
        embedding_vector = self.embeddings_index.get(word)
        if embedding_vector is None:
            return [0] * 300
        return embedding_vector

    def get_emb_given_word(self, word):
        try:
            return self.embeddings[word]
        except KeyError:
            return None

    def get_emb_matrix_given_vocab(self, vocab, emb_matrix):
        counter = 0.
        for word, index in vocab.iteritems():
            try:
                emb_matrix[index] = self.embeddings[word]
                counter += 1
            except KeyError:
                pass

        logger.info(
            '%i/%i word vectors initialized (hit rate: %.2f%%)' % (counter, len(vocab), 100 * counter / len(vocab)))
        # L2 normalization
        norm_emb_matrix = emb_matrix / np.linalg.norm(emb_matrix, axis=-1, keepdims=True)
        return norm_emb_matrix

    def get_topic_matrix(self, n_clusters, fix_clusters="no"):
        km = KMeans(n_clusters=n_clusters)
        km.fit(self.emb_matrix)
        clusters = km.cluster_centers_

        if fix_clusters == "yes":
            clusters[0] = self.embeddings["environment"]
            clusters[1] = self.embeddings["quality"]
            clusters[2] = self.embeddings["health"]
            clusters[3] = self.embeddings["price"]

        # L2 normalization
        norm_topic_matrix = clusters / np.linalg.norm(clusters, axis=-1, keepdims=True)
        return norm_topic_matrix.astype(np.float32)

    def get_emb_dim(self):
        return self.emb_dim
