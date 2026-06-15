# Zapp Valores em Divida

## Descrição

Aplicação para visualizar e gerenciar documentos em aberto de fornecedores.

Mostra:
- Totais vencidos
- Totais não vencidos  
- Total de divida por fornecedor
- Resumo agregado de todos os fornecedores

## Arquitetura

### Backend (Python + FastAPI)
- **main.py** - Aplicação FastAPI com rotas de API
- **db.py** - Funções de acesso à base de dados SQL Server
  - `get_valores_em_divida()` - Retorna lista de valores em divida por fornecedor
  - `get_resumo_totais()` - Retorna totais agregados

### Frontend (React + TypeScript + Vite)
- **App.tsx** - Componente principal
- **App.css** - Estilos da aplicação
- Tabela responsiva com dados de fornecedores
- Cards de resumo com totais

## Base de Dados

Usa as tabelas:
- `TB0001CntDocReg` - Documentos por regularizar (vencimento)
- `TB0001CntPlano` - Plano de contas (nomes de fornecedores)

Filtra contas que começam com `22%` ou `271%` (fornecedores).

## Integração com Quadro de Bordo

Integrada através de:
- `quadro-de-bordo/backend/apps/valores_em_divida.py`
- Endpoints em `/api/valores/*`

O quadro de bordo importa dinamicamente o módulo `db.py` da zapp_valores_em_divida.

## Deploy

Ambas as aplicações podem rodar independentemente ou integradas:

1. **Standalone**: Iniciar `backend/main.py` (porta 8004)
2. **Integrada**: Acessar via quadro-de-bordo na porta 8003

## Dependências

Python:
- fastapi==0.111.0
- uvicorn[standard]==0.29.0
- pyodbc==5.1.0
- pydantic==2.7.1

Node:
- react@18.2.0
- react-dom@18.2.0
- axios@1.6.0
- typescript@5.2.2
- vite@5.0.0
