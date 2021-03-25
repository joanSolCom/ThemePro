FROM php:apache-buster

EXPOSE 80

RUN apt-get update
RUN apt-get install build-essential python3 python3-dev python3-pip git -y
RUN apt-get upgrade -y
RUN pip3 install -U pip setuptools wheel
RUN pip3 install -U spacy==2.3.1
RUN pip3 install numpy scipy flask flask-jsonpify gensim
RUN python3 -m spacy download en_core_web_lg-2.3.1 --direct

RUN git clone https://github.com/huggingface/neuralcoref.git
RUN cd neuralcoref && pip3 install -r requirements.txt && pip3 install -e .

RUN git clone https://github.com/joanSolCom/ThemePro.git 
RUN apt-get install wget unzip -y
RUN cd ThemePro/backend/embeddings && wget http://nlp.stanford.edu/data/glove.42B.300d.zip && unzip glove.42B.300d.zip && rm glove.42B.300d.zip
RUN cd ThemePro/backend/embeddings && python3 glove2word2vec.py
RUN cd ThemePro/frontend/ && mkdir /var/www/html/themePro/ && cp -R * /var/www/html/themePro/
RUN pip3 install sklearn
RUN pip3 install flask_cors
RUN pip3 install python-Levenshtein
ADD launch.sh launch.sh
RUN chmod 0755 launch.sh
CMD ./launch.sh