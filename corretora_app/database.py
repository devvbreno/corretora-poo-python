import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv
from .models.cliente import Cliente
from .models.conta import Conta
from .models.ativo import Ativo

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

def adicionar_cliente(nome, cpf):

    cursor = None
    cnx = None

    try:
        cnx = conectar_db()
        if cnx and cnx.is_connected():
            cursor = cnx.cursor()
            query = "INSERT INTO cliente (nome, cpf) VALUES (%s, %s);" # %s para evitar possiveis usuarios mal intencionados
            dados = (nome, cpf)
            cursor.execute(query, dados)
            cnx.commit()
        else:
            raise ConnectionError('Falha ao tentar conectar-se ao banco de dados.')

    except mysql.connector.Error as erro:
        cnx.rollback()
        raise ValueError (f"Erro ao adicionar cliente, erro: {erro}")
    finally:
        if cursor:
            cursor.close()
        if cnx and cnx.is_connected():
            cnx.close()

def buscar_cliente_por_cpf(cpf: str):

    cnx = None
    cursor = None

    try:
        cnx = conectar_db()
        if cnx and cnx.is_connected():
            cursor = cnx.cursor()
            query = "SELECT id, nome, cpf FROM cliente WHERE cpf = %s"
            dados = (cpf,)
            cursor.execute(query, dados)
            resultado = cursor.fetchone()
            
            if resultado:
                id_cliente, nome_cliente, cpf_cliente = resultado
                try:
                    cliente_obj = Cliente(nome_cliente=nome_cliente, cpf_cliente= cpf_cliente, id_cliente=id_cliente)
                    return cliente_obj
                except (ValueError, TypeError) as conv_err:
                    print("Erro de resultado dos dados de busca de cliente por cpf.")
        else:
            print("Falha ao tentar conectar-se ao banco de dados.")
    except mysql.connector.Error as error:
        raise ValueError (f'Erro nos dados de busca:  {error}')
    finally:
        if cursor:
            cursor.close()
        if cnx and cnx.is_connected():
            cnx.close()

def buscar_ativo_por_ticker(ticker: str):

    cnx = None
    cursor = None

    try:
        cnx = conectar_db()
        if cnx and cnx.is_connected():
            
            cursor = cnx.cursor()
            
            query = "SELECT id, ticker, nome_empresa, preco_atual FROM ativo WHERE ticker = %s"
            dados = (ticker,)
            
            cursor.execute(query, dados)
            resultado = cursor.fetchone()
            
            if resultado:
                id_ativo, ticker_bd, nome_empresa_bd, preco_atual_bd = resultado
                try:
                    preco_atual = float(preco_atual_bd)
                    ativo_obj = Ativo(ticker=ticker_bd, nome_empresa=nome_empresa_bd, preco_atual=preco_atual)
                    return ativo_obj
                except (ValueError, TypeError) as conv_err:
                    print(f"Erro ao converter o ativo do banco de dados: {conv_err}")
            else:
                print(f"Ativo com ticker '{ticker} não encontrado.")
                return None
        else:
            print("Falha ao tentar conectar-se ao banco de dados.")

    except mysql.connector.Error as error:
        print (f'Erro nos dados de busca:  {error}')

    finally:
        if cursor:
            cursor.close()
        if cnx and cnx.is_connected():
            cnx.close()
    return None

def atualizar_preco_ativo(ticker: str, novo_preco: float):
    cnx = None
    cursor = None
    try:
        if not isinstance(novo_preco, (int, float)) or novo_preco < 0:
            raise ValueError ("O novo preço deve ser um numero e não pode ser menor que zero.")
        
        cnx = conectar_db()
        if cnx and cnx.is_connected():
            cursor = cnx.cursor()

            query = "UPDATE ativo SET preco_atual = %s WHERE ticker = %s"
            dados = (novo_preco, ticker)

            cursor.execute(query, dados)
            cnx.commit()
            if cursor.rowcount > 0:
                print(f"Preço do ativo '{ticker}' atualizado para R$ {novo_preco:.2f} com sucesso.")
            else:
                print(f"Aviso: Ativo com ticker '{ticker}' não encontrado para atualização.")
    except (TypeError, ValueError) as val_error:
        print(f"Erro de validação ao atualizar preço: {val_error}")
        raise

    except mysql.connector.Error  as bd_error:
        if cnx:
            cnx.rollback()
            print("Erro ao tentar atualizar o novo preço do ativo no banco de dados. ")
            raise ValueError(f"Erro no banco de dados ao atualizar preço.") from bd_error

    except Exception as e:
        print(f"EErro inesperado: {e}")
        raise

    finally:
        if cursor:
            cursor.close()
        if cnx and cnx.is_connected():
            cnx.close()

def salvar_conta(conta : Conta):
    cursor = None
    cnx = None

    try:
        cnx = conectar_db()
        if cnx and cnx.is_connected():
            cursor = cnx.cursor()
            
            numero = conta.numero_conta
            saldo = conta.saldo_da_conta
            cliente_associado = conta.cliente
            if not cliente_associado or not cliente_associado.id:
                raise ValueError("O cliente associado a esta conta não possui u ID do banco")
            id_do_cliente = cliente_associado.id
            
            query = "INSERT INTO conta (numero_conta, saldo, cliente_id) VALUES (%s, %s, %s)" 
            dados = (numero, saldo, id_do_cliente)
            cursor.execute(query, dados)
            cnx.commit()
            
            print(f"Conta número: '{numero}' salva com sucesso!")
            return cursor.lastrowid
        else:
            raise ConnectionError('Falha ao tentar conectar-se ao banco de dados.')
    
    except mysql.connector.Error as erro:
        if cnx:
            cnx.rollback()
        raise ValueError (f"Erro ao salvar a conta, erro: {erro}")
    except Exception as e:
        print(f"Um erro inesperado: {e}")
    finally:
        if cursor:
            cursor.close()
        if cnx and cnx.is_connected():
            cnx.close()