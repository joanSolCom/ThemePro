FROM php:7.0-apache
COPY web /var/www/html
EXPOSE 80

RUN apt-get update
RUN apt-get install python3 python3-dev python3-pip git gensim
RUN pip3 install spacy numpy scipy flask flask-jsonpify

#NEURALCOREF
RUN git clone https://github.com/huggingface/neuralcoref.git
RUN cd neuralcoref
RUN pip3 install -r requirements.txt
RUN pip3 install -e 

RUN git clone https://github.com/joanSolCom/ThemePro.git 
RUN cd themePro
RUN cd embeddings
RUN wget http://nlp.stanford.edu/data/glove.42B.300d.zip
RUN unzip glove.42B.300d.zip
RUN rm glove.42B.300d.zip
RUN cd ..
RUN python3 glove2word2vec.py

RUN cd ../frontend/
RUN mkdir /var/www/html/themePro/
RUN cp * /var/www/html/themePro/

RUN cd ../backend/
CMD [python3 themazo.py]