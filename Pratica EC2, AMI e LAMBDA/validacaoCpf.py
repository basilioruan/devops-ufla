import boto3
import json
import csv

LAMBDA = 'validacaoCpf'
REGIAO = 'sa-east-1'
CSV_ENTRADA = 'cpfValidacao.csv'
CSV_SAIDA = 'cpfValidado.csv'

def lambda_validacao_cpf(cpf, cliente_lambda):
    try:
        payload = {
            'cpf': cpf
        }

        response = cliente_lambda.invoke(
            FunctionName=LAMBDA,
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )

        resultado_payload = response['Payload'].read().decode('utf-8')
        
        resultado_json = json.loads(resultado_payload)

        return resultado_json

    except Exception as e:
        print(f"Erro ao invocar a Lambda para o CPF {cpf}: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'mensagem': f'Erro de comunicação com a AWS: {str(e)}'})
        }

def main():
    print("Iniciando o processo de validação de CPFs...")

    try:
        cliente_lambda = boto3.client('lambda', region_name=REGIAO)
    except Exception as e:
        print(f"Erro ao inicializar o cliente Boto3. Verifique suas credenciais e região. Erro: {e}")
        return

    resultados_finais = []

    try:
        with open(CSV_ENTRADA, mode='r', encoding='utf-8') as infile:
            leitor_csv = csv.reader(infile)
            next(leitor_csv) 

            for linha in leitor_csv:
                cpf_original = linha[0].strip()
                print(f"Validando CPF: {cpf_original}...")

                resultado_lambda = lambda_validacao_cpf(cpf_original, cliente_lambda)

                status_code = resultado_lambda.get('statusCode')
                mensagem = "Erro ao processar resposta da Lambda."
                if 'body' in resultado_lambda:
                    try:
                        body_dict = json.loads(resultado_lambda['body'])
                        mensagem = body_dict.get('mensagem', 'Mensagem não encontrada.')
                    except json.JSONDecodeError:
                        mensagem = "Resposta do body não era um JSON válido."

                status_validacao = 'Válido' if status_code == 200 else 'Inválido'

                resultados_finais.append([cpf_original, status_validacao, mensagem])

    except FileNotFoundError:
        print(f"ERRO: Arquivo de entrada '{CSV_ENTRADA}' não encontrado.")
        return

    with open(CSV_SAIDA, mode='w', newline='', encoding='utf-8') as outfile:
        escritor_csv = csv.writer(outfile)

        escritor_csv.writerow(['cpf_enviado', 'status_validacao', 'mensagem_retorno'])

        escritor_csv.writerows(resultados_finais)

    print("\n--- Relatório Final ---")
    print(f"{'CPF Enviado':<20} | {'Status':<10} | {'Mensagem'}")
    print("-" * 50)
    for res in resultados_finais:
        print(f"{res[0]:<20} | {res[1]:<10} | {res[2]}")
        
    print(f"\nProcesso finalizado! Relatório salvo em '{CSV_SAIDA}'.")

if __name__ == "__main__":
    main()