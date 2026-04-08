from fastapi import FastAPI
from app.api.routes.file_routes import router

app = FastAPI(
    title="WeTransfer Clon",
    description="Servicio de transferencia de archivos con enlaces únicos y expiración automática.",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def root():
    return {"message": "WeTransfer Clon API corriendo"}