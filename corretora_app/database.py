import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv


load_dotenv() # carrega as variaveis do arquivo .env

def conectar_db():

    cnx = None
    try:
        db_host = os.getenv ("DB_HOST")
        db_user = os.getenv ("DB_USER")
        db_password = os.getenv ("DB_PASSWORD")
        db_name = os.getenv ("DB_NAME")

        if not all([db_host, db_user, db_password, db_name]):
            raise ValueError ("Todos os dados nao foram fornecidos")
        
        cnx = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
        )
        
        if cnx.is_connected():
            print ("Conectou-se ao banco de dados com sucesso")
            return cnx
        else:
            print ("Não conectou-se ao banco de dados")
            return None

    except mysql.connector.Error as erro:
        raise ValueError (f"Erro ao conectar-se ao banco de dados, erro: {erro}")

def desconectar_db(cnx):
    if cnx.is_connected():
        cnx.close()
        print ("Desconectou-se do banco de dados")
    else:
        print ("Não estava conectado ao banco de dados")
        return None

