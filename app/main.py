from fastapi import FastAPI
from .endpoints import public, protected
from .database import Base, engine

# Crear tablas si no se usa Alembic para desarrollo rápido (aunque Alembic es requerido)
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Lkmx Test API",
    description="API con FastAPI, SQLAlchemy y Auth0",
    version="1.0.0"
)

app.include_router(public.router, prefix="/api/v1/public", tags=["Public"])
app.include_router(protected.router, prefix="/api/v1/protected", tags=["Protected"])

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de prueba", "docs": "/docs"}
