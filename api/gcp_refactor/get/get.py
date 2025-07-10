import json
import os

import functions_framework
import psycopg


def conectar_banco():
    """
    Função responsável por criar uma conexão com o banco de dados postgres.
    Caso a conexão com o banco falhe, retorna a exceção formatada como string.
    """
    try:
        conexao = psycopg.connect(
            dbname=os.environ["DB_POSTGRES"],
            user=os.environ["USUARIO_POSTGRES"],
            password=os.environ["SENHA_POSTGRES"],
            host=os.environ["URL_POSTGRES"],
        )
        return conexao
    except Exception as e:
        return str(e)


@functions_framework.http
def get(request):
    """
    Retorna todos os dados de nota fiscal do banco de dados postgres
    """
    # Tenta se conectar com o banco
    conexao = conectar_banco()
    # Caso a conexão não tenha retornado uma string, quer dizer que a conexão foi bem sucedida e assim o código corre normalmente
    if not isinstance(conexao, str):
        with conexao:
            with conexao.cursor() as cursor:
                # Cria a tabela caso ela não exista (precaução)
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS notas (id serial PRIMARY KEY, valor real, cnpj varchar, data date)"
                )

                # Retorna todos os dados da tabela "notas"
                cursor.execute("SELECT * FROM notas")
                resultado = cursor.fetchall()

                conexao.commit()

                json_retorno = {"payload": []}

                for dados in resultado:
                    json_retorno["payload"].append(
                        {
                            "Index": dados[0],
                            "Valor": dados[1],
                            "CNPJ": dados[2],
                            "Data": dados[3].isoformat(),
                        }
                    )

                return (
                    json.dumps(json_retorno),
                    200,
                    {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "GET, OPTIONS",
                        "Access-Control-Allow-Headers": "*",
                    },
                )
    else:
        # Caso a conexão retorne uma string, quer dizer que houve um erro. Exibe o erro para o usuário
        return (
            json.dumps({"erro": conexao}),
            500,
            {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "*",
            },
        )
