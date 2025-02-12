import csv
import io
from flask import Response

def generate_csv(data, filename):
    """
    Gera uma resposta HTTP com um arquivo CSV a partir de uma lista de dicionários.

    Args:
        data (list): Lista de dicionários contendo os dados.
        filename (str): Nome do arquivo CSV (sem extensão).

    Returns:
        Response: Resposta HTTP com o arquivo CSV ou uma mensagem de erro.
    """
    # Validação dos dados
    if not data or not isinstance(data, list):
        return Response(
            "No data available or invalid data format",
            status=404,
            mimetype="text/plain"
        )

    if not all(isinstance(item, dict) for item in data):
        return Response(
            "Invalid data format: expected a list of dictionaries",
            status=400,
            mimetype="text/plain"
        )

    # Remove a extensão .csv do nome do arquivo, se presente
    if filename.endswith('.csv'):
        filename = filename[:-4]

    try:
        # Cria um buffer de string para armazenar o CSV
        output = io.StringIO()

        # Obtém os nomes das colunas a partir das chaves do primeiro dicionário
        fieldnames = data[0].keys()

        # Cria um escritor CSV usando DictWriter
        writer = csv.DictWriter(output, fieldnames=fieldnames)

        # Escreve o cabeçalho e os dados no buffer
        writer.writeheader()
        writer.writerows(data)

        # Cria a resposta HTTP com o conteúdo do CSV
        response = Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename={filename}.csv",
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )

        return response

    except Exception as e:
        # Log do erro (pode ser substituído por um logger real em produção)
        print(f"Error generating CSV: {str(e)}")

        return Response(
            f"Error generating CSV: {str(e)}",
            status=500,
            mimetype="text/plain"
        )