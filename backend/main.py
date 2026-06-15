from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List, Dict, Any
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db

app = FastAPI(title="Valores em Divida API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/valores-em-divida")
def get_valores_em_divida():
    """Obter totais de documentos em aberto por fornecedor"""
    try:
        valores = db.get_valores_em_divida()
        return {"valores": valores}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/resumo")
def get_resumo():
    """Obter totais agregados de todos os fornecedores"""
    try:
        resumo = db.get_resumo_totais()
        return resumo
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Serve static files from frontend build
frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dist')
if os.path.exists(frontend_dir):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dir, 'assets')), name="assets")

@app.get("/")
async def serve_root():
    """Serve index.html for SPA"""
    index_file = os.path.join(frontend_dir, 'index.html')
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"error": "Frontend not built"}

@app.get("/{path_name:path}")
async def serve_spa(path_name: str):
    """Serve index.html for all non-API routes (SPA routing)"""
    if path_name.startswith('api/'):
        return {"error": "Not found"}

    index_file = os.path.join(frontend_dir, 'index.html')
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"error": "Frontend not built"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
