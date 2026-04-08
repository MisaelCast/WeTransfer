from fastapi import FastAPI
from app.api.routes.file_routes import router
from app.services.expiration_service import start_scheduler

app = FastAPI(
    title="WeTransfer Clon",
    description="Servicio de transferencia de archivos con enlaces únicos y expiración automática.",
    version="1.0.0"
)

app.include_router(router)


@app.on_event("startup")
def startup_event():
    start_scheduler()


@app.get("/")
def root():
    return {"message": "WeTransfer API corriendo"}