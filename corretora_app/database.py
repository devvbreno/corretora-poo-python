import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv


load_dotenv() 

def conectar_db():

    cnx = None
    try:
        db_host = os.getenv ("DB_HOST")
        db_user = os.getenv ("DB_USER")
        db_password = os.getenv ("DB_PASSWORD")
        db_name = os.getenv ("DB_NAME")

        if not all([db_host, db_user, db_password, db_name]):
            raise ValueError ("Os dados corretos não foram fornecidos")
        
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

def adicionar_cliente(nome, cpf):

    cursor = None
    cnx = None

    try:
        cnx = conectar_db()
        cursor = cnx.cursor()
        query = "INSERT INTO cliente (nome, cpf) VALUES (%s, %s);" # %s para evitar possiveis usuarios mal intencionados
        dados = (nome, cpf)
        cursor.execute(query, dados)
        cnx.commit()

    except mysql.connector.Error as erro:
        cnx.rollback()
        raise ValueError (f"Erro ao adicionar cliente, erro: {erro}")
    finally:
        if cursor:
            cursor.close()
        if cnx and cnx.is_connected():
            cnx.close()