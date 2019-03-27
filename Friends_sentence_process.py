import os
import re
import string
import numpy as np
import collections
import tensorflow as tf
from tensorflow.python.ops import nn_ops
class sentenceProcess():
    def __init__(self, file_path=None, fileformat='txt', stops=[]):
        self.file_path = file_path
        self.fileformat = fileformat
        self.stops = stops
    def index_build(self, file_path):
        # file_path = self.file_path
        file_format = self.fileformat
        index= []
        index_dict_id2sen = {}
        index_dict_sen2id = {}
        if file_format == 'txt':
            sub_file_list = os.listdir(file_path)
            for line in sub_file_list:
                sub_file_path = file_path+'/'+line
                if line == '.DS_Store':
                    os.remove(sub_file_path)
                else:
                    txt_list = os.listdir(sub_file_path)
                    for txtline in txt_list:
                        txt_path = sub_file_path+'/'+txtline
                        if txtline == '.DS_Store':
                            os.remove(txt_path)
                        else:
                            [txt_index] = re.findall(r'(.*).txt',txtline)
                            with open(txt_path,'r') as f:
                                for i, sentence in enumerate(f):
                                    sub_index = [txt_index, i, sentence.strip('\n').lower()]
                                    index.append(sub_index)
                                    index_dict_sen2id.setdefault(sub_index[2],[]).append(txt_index+'-'+str(i))
                                    index_dict_id2sen.setdefault(txt_index+'-'+str(i), sub_index[2])
        else:
            print('Can\'t process it! TXT only!')
        return index, index_dict_id2sen, index_dict_sen2id
        ## index=[['1-1',1,sentence1]['1-1',2,sentence2]...]
        ## index_dict_id2sen={'1-1-1':sentence, ...}
        ## index_dict_sen2id={sentence:['1-1-1',...], ...}

    def save_index_file(self, parent_path, index, id2sen, sen2id):
        index_path = parent_path+'index_list.txt'
        id2sen_path = parent_path+'id2sen.txt'
        sen2id_path = parent_path+'sen2id.txt'
        # self.text_save(index, index_path)
        self.save_dict_to_file(id2sen, id2sen_path)
        self.save_dict_to_file(sen2id, sen2id_path)

    def normalize_text(self, index):
        index_normal = []
        stops = self.stops
        for i in range(len(index)):
            texts = index[i][2]
            # Lower case
            texts = texts.lower()
            # Remove punctuation]
            texts = ''.join(c for c in texts if c not in string.punctuation)
            # # Remove numbers
            # texts = ''.join(c for c in texts if c not in '12345667890')
            # Remove stopwords and trim extra whitespace
            texts = ' '.join(word for word in texts.split() if word not in stops)
            index_normal.append(texts)
        return index_normal

    def get_index(self,file_path):
        index, index_dict_id2sen, index_dict_sen2id = self.index_build(file_path)
        index_normal = self.normalize_text(index)
        return index, index_normal, index_dict_id2sen, index_dict_sen2id

    def text_save(self, content, filename, mode='w'):
        # Try to save a list variable in txt file.
        file = open(filename, mode)
        for i in range(len(content)):
            file.write(str(content[i]) + '\n')
        file.close()

    def load_dict_from_file(self, filepath):
        _dict = {}
        try:
            with open(filepath, 'r') as dict_file:
                for line in dict_file:
                    (key, value) = line.strip().split(':::')
                    _dict[key] = value
        except IOError as ioerr:
            print("文件 %s 不存在" % (filepath))
        return _dict

    def save_dict_to_file(self, _dict, filepath):
        try:
            with open(filepath, 'w') as dict_file:
                for (key, value) in _dict.items():
                    dict_file.write('%s:::%s\n' % (key, value))
        except IOError as ioerr:
            print("文件 %s 无法创建" % (filepath))


    def triple_process(self, index, save_path):
        source_data = []
        target_data = []
        for i in range(len(index)-1):
            episode_num = index[i][0]
            if episode_num == index[i+1][0]:
                source_data.append(index[i][2])
                target_data.append(index[i+1][2])
        source_filename = save_path + 'source_data.txt'
        target_filename = save_path + 'target_data.txt'
        self.text_save(source_data, source_filename)
        self.text_save(target_data, target_filename)

class vocabProcess():
    def __init__(self, vec_path=None, fileformat=None):
        self.vec_path = vec_path
        self.fileformat = fileformat
        self.word2id = {}
        self.id2word = {}
        if fileformat == 'txt':
            self.fromText(vec_path)
    def fromText(self, vec_path, voc):
        vec_file = open(vec_path,'r',encoding='utf-8')
        word_vecs = {}
        self.voc = voc
        for line in vec_file:
            line = line.strip()
            parts = line.split(' ')
            word = parts[0]
            if (voc is not None) and (word not in voc): continue
            vector = np.array(parts[1:], dtype='float32')
            self.word_dim = len(parts[1:])
            cur_index = len(self.word2id)
            self.word2id[word] = cur_index
            self.id2word[cur_index] = word
            word_vecs[cur_index] = vector
        vec_file.close()
        # print(self.word2id[i] for i in range(3))
        self.vocab_size = len(self.word2id)
        self.word_vecs = np.zeros((self.vocab_size + 1, self.word_dim),
                                  dtype=np.float32)  # the last dimension is all zero
        for cur_index in range(self.vocab_size):
            self.word_vecs[cur_index] = word_vecs[cur_index]
        return word_vecs

    def build_dictionary(self, sentences):
        # Turn sentences which are list of strings into list of words
        split_sentence = [t.split() for t in sentences]
        split_word = [w.split() for s in split_sentence for w in s]
        # split_word = [t for t in sentences]
        split_words = []
        for w in split_word:
            [word] = w
            split_words.append(word)
        # Initial list of [word, word_count] for each word, starting with unknown
        # count = [('RARE', -1)]
        count = []
        # Now add most frequent words, limited to the N-most frequent (N=vocabulary size)
        count.extend(collections.Counter(split_words).most_common())
        # Now create the dictionary
        word_dict = {}
        # For each word that we want in the dictionary, add it, then make it the value of the prior dictionary length
        for word, word_count in count:
            word_dict[word] = len(word_dict)
        return word_dict

if __name__ == '__main__':
    sp = sentenceProcess()
    file_path = 'Friends/txtfile'
    # index, index_normal, a, b = sp.get_index(file_path)
    # sp.triple_process(index, 'Friends/data/')
    index, id2sen, sen2id = sp.index_build(file_path)
    sp.save_index_file('Friends/data/', index, id2sen, sen2id)
    # vp = vocabProcess()
    # word_dict = vp.build_dictionary(index_normal)
    # vec_path = '/Users/artemis/Downloads/glove/glove.840B.300d.txt'
    # voc = word_dict.keys()
    # word_vecs = vp.fromText(vec_path=vec_path, voc=voc)
    # print(len(word_vecs))
    # print(word_dict, len(word_dict))
    # print(len(index_normal), len(a), len(b))
    # print(a['3-18-112'], b['Oh.'])