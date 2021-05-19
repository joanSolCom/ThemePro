# import required methods from gensim package
from gensim.test.utils import get_tmpfile
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
 
# create temp file and save converted embedding into it
target_file = get_tmpfile('glove_word2vec.txt')
glove2word2vec('glove.42B.300d.txt', target_file)

# load the converted embedding into memory
model = KeyedVectors.load_word2vec_format(target_file)

# save as binary data
model.save_word2vec_format('glove_word2vec.bin.gz', binary=True)