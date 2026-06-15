# Valores em Divida

Aplicação para visualizar e gerenciar documentos em aberto de fornecedores.

## Estrutura do Projeto

```
zapp_valores_em_divida/
├── backend/
│   ├── db.py          # Funções de acesso à base de dados
│   ├── main.py        # Aplicação FastAPI
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── App.css
│   │   ├── main.tsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── tsconfig.node.json
└── requirements.txt
```

## Setup

### Backend

1. Instalar dependências:
```bash
cd backend
pip install -r ../requirements.txt
```

2. Executar aplicação:
```bash
python main.py
```

A API estará disponível em `http://localhost:8004`

### Frontend

1. Instalar dependências:
```bash
cd frontend
npm install
```

2. Modo desenvolvimento:
```bash
npm run dev
```

3. Build para produção:
```bash
npm run build
```

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/valores-em-divida` - Lista de valores em divida por fornecedor
- `GET /api/resumo` - Resumo dos totais agregados

## Integração com Quadro de Bordo

A aplicação está integrada no `quadro-de-bordo` através do arquivo:
- `quadro-de-bordo/backend/apps/valores_em_divida.py`

Endpoints no quadro-de-bordo:
- `GET /api/valores/lista` - Lista de valores em divida
- `GET /api/valores/resumo` - Resumo dos totais
