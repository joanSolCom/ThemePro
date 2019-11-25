# ThemePro

Code that was developed for the demo of ThemePro.
This assumes you have a MySQL database called Embeddings with the word embeddings you want to use.
Each table is a set of embeddings with the following fields
word (varchar 255 primary key) dim1 dim2 dim3 .... dimN (decimal (10,8))

backend and frontend are in their own folder.

The requirements for the backend:
python3
flask
spacy with model en_core_web_sm
neuralcoref
pymysql
sklearn
scipy

The requirements for the frontend
php

Upon acceptance, we will release a Docker container which the setup of the demo