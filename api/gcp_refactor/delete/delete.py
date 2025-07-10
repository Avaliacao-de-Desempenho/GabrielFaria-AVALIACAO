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
def delete(request):
    """
    Função que tem o objetivo de deletar uma linha da tabela "notas"

    Parâmetros:
        id (int): id da linha a ser deletada
    """

    # Trata requisição do método OPTIONS, comum acontecer antes de rodar o DELETE
    if request.method == "OPTIONS":
        return (
            "",
            204,
            {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "*",
                "Content-Type": "application/json",
            },
        )

    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and "id" in request_json:
        id = request_json["id"]
    elif request_args and "id" in request_args:
        id = request_args["id"]
    else:
        id = 1

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

                # Deleta a linha da tabela onde o id bate com o parâmetro passado
                cursor.execute("DELETE FROM notas WHERE id = (%s)", (id,))

                conexao.commit()

                # Verifica se alguma linha foi alterada. Caso não, o id passado não existe na tabela
                if cursor.rowcount:
                    return (
                        json.dumps(
                            {"Sucesso": f"Linha com id: {id} deletada com sucesso!"}
                        ),
                        200,
                        {
                            "Content-Type": "application/json",
                            "Access-Control-Allow-Origin": "*",
                            "Access-Control-Allow-Methods": "DELETE, OPTIONS",
                            "Access-Control-Allow-Headers": "*",
                        },
                    )
                else:
                    return (
                        json.dumps({"Erro": f"Linha com id: {id} não existe."}),
                        404,
                        {
                            "Content-Type": "application/json",
                            "Access-Control-Allow-Origin": "*",
                            "Access-Control-Allow-Methods": "DELETE, OPTIONS",
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
                "Access-Control-Allow-Methods": "DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "*",
            },
        )
