Librerias necesarias:

- pip install sklear
- pip install nltk
- pip install tweepy
- pip install django

Correr:
- python3.6 manage.py runserver

- La api de twitter para conseguir los tweets por locacion y filtrado por candidato
- filtrar que sean solo en español
- modificar vectorizer para que ignore ciertos caracteres especiales en el español y para que realice el proceso de stemming que sirve para volver las palabras a su raiz. i.e. Transformar -> transform
- convertir el data set en csv y montarlo en memoria para ser procesado como arreglo
- separar en 2 arreglos los datos y la categoria
- entrenar el modelo analitico supervisado