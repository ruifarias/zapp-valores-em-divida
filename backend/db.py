import pyodbc
from datetime import datetime, date
from typing import List, Dict, Any

CONN_STR = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=TSERVER\\SQLSERVER;"
    "DATABASE=DBClassico;"
    "UID=GIWINDOWS;"
    "PWD=GIWINDOWS;"
    "TrustServerCertificate=yes;"
)

def get_connection():
    return pyodbc.connect(CONN_STR)

def get_valores_em_divida() -> List[Dict[str, Any]]:
    """Obter totais de documentos em aberto por fornecedor (vencidos e não vencidos)"""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        ano_atual = datetime.now().year

        query = f"""
        SELECT
            doc.Codigo_Conta,
            doc.Tipo_Movimento,
            doc.Numero_Documento,
            doc.Data_Vencimento,
            CASE doc.Tipo_Movimento
                WHEN 'C' THEN doc.Valor_por_Regularizar
                WHEN 'D' THEN -doc.Valor_Por_Regularizar
            END as Valor_Por_Regularizar,
            COALESCE(poc.Descricao_Conta, CONCAT('Conta ', doc.Codigo_Conta)) as Nome_Fornecedor
        FROM TB0001CntDocReg doc
        LEFT JOIN TB0001CntPOC poc ON doc.Codigo_Conta = poc.Codigo_Conta AND poc.Ano = {ano_atual}
        WHERE (doc.codigo_conta LIKE '22%'
            OR doc.codigo_conta LIKE '271%')
        """

        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()

        # Agrupar por Codigo_Conta e calcular totais
        dados_por_conta = {}
        hoje = datetime.now().date()

        for row in rows:
            codigo_conta = row[0]
            data_vencimento = row[3]
            valor = float(row[4]) if row[4] else 0.0
            nome_fornecedor = row[5] if row[5] else f"Conta {row[0]}"

            if codigo_conta not in dados_por_conta:
                dados_por_conta[codigo_conta] = {
                    "nome": nome_fornecedor,
                    "total_vencido": 0.0,
                    "total_nao_vencido": 0.0
                }

            # Converter data_vencimento para date se for datetime
            if data_vencimento:
                if isinstance(data_vencimento, datetime):
                    data_vencimento = data_vencimento.date()

                # Verificar se está vencido
                if data_vencimento < hoje:
                    dados_por_conta[codigo_conta]["total_vencido"] += valor
                else:
                    dados_por_conta[codigo_conta]["total_nao_vencido"] += valor
            else:
                dados_por_conta[codigo_conta]["total_nao_vencido"] += valor

        valores = []
        for codigo_conta, dados in dados_por_conta.items():
            valores.append({
                "codigo_conta": codigo_conta,
                "fornecedor": dados["nome"],
                "total_vencido": dados["total_vencido"],
                "total_nao_vencido": dados["total_nao_vencido"],
                "total_divida": dados["total_vencido"] + dados["total_nao_vencido"]
            })

        # Ordenar por fornecedor
        valores.sort(key=lambda x: x["fornecedor"])
        return valores
    except Exception as e:
        print(f"Erro ao obter valores em divida: {e}")
        return []

def get_resumo_totais() -> Dict[str, float]:
    """Obter totais agregados de todos os fornecedores"""
    try:
        valores = get_valores_em_divida()

        total_vencido = sum(v["total_vencido"] for v in valores)
        total_nao_vencido = sum(v["total_nao_vencido"] for v in valores)
        total_divida = sum(v["total_divida"] for v in valores)

        return {
            "total_vencido": total_vencido,
            "total_nao_vencido": total_nao_vencido,
            "total_divida": total_divida,
            "quantidade_fornecedores": len(valores)
        }
    except Exception as e:
        print(f"Erro ao obter resumo de totais: {e}")
        return {
            "total_vencido": 0.0,
            "total_nao_vencido": 0.0,
            "total_divida": 0.0,
            "quantidade_fornecedores": 0
        }
