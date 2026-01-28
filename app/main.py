from fastapi import FastAPI
from contextlib import asynccontextmanager
from .endpoints import public, protected
from .database import Base, engine, SessionLocal
from .models import Product, User, CategoryEnum
from .auth import pwd_context
from sqlalchemy.exc import OperationalError
from fastapi import Request
from fastapi.responses import JSONResponse

productos_ejemplo = [
    {"name": "Paracetamol 500mg", "price": 5.50, "category": CategoryEnum.FARMACIA, "stock": 100},
    {"name": "Tomate Rojo", "price": 2.00, "category": CategoryEnum.FRUTAS, "stock": 50},
    {"name": "Leche Entera 1L", "price": 1.80, "category": CategoryEnum.LACTEOS, "stock": 75},
    {"name": "Pan Blanco 1kg", "price": 2.50, "category": CategoryEnum.PANADERIA, "stock": 60},
    {"name": "Pechuga de Pollo", "price": 7.90, "category": CategoryEnum.CARNES, "stock": 40},
    {"name": "Aceite de Oliva Virgen Extra 500ml", "price": 8.20, "category": CategoryEnum.LACTEOS, "stock": 30},
    {"name": "Ajo 1kg", "price": 3.00, "category": CategoryEnum.FRUTAS, "stock": 80},
    {"name": "Sal Común 1kg", "price": 1.50, "category": CategoryEnum.ABARROTES, "stock": 120},
    {"name": "Azúcar Refinada 1kg", "price": 2.20, "category": CategoryEnum.ABARROTES, "stock": 90},
    {"name": "Vino Tinto 750ml", "price": 6.80, "category": CategoryEnum.FARMACIA, "stock": 55},
    {"name": "Manzana Fuji", "price": 1.90, "category": CategoryEnum.FRUTAS, "stock": 110},
    {"name": "Queso Crema 200g", "price": 2.80, "category": CategoryEnum.LACTEOS, "stock": 65},
    {"name": "Cerdo Asado 1kg", "price": 9.50, "category": CategoryEnum.CARNES, "stock": 45},
    {"name": "Harina de Trigo 1kg", "price": 2.10, "category": CategoryEnum.PANADERIA, "stock": 70},
    {"name": "Bolsas de Verduras", "price": 1.30, "category": CategoryEnum.ABARROTES, "stock": 130},
    {"name": "Pastillas Fermentadas", "price": 4.00, "category": CategoryEnum.FARMACIA, "stock": 85},
    {"name": "Galletas de Chocolate", "price": 3.70, "category": CategoryEnum.PANADERIA, "stock": 50},
    {"name": "Pollo Entero", "price": 12.00, "category": CategoryEnum.CARNES, "stock": 35},
    {"name": "Plátanos", "price": 1.60, "category": CategoryEnum.FRUTAS, "stock": 105}
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Intentar conectar y crear tablas
    try:
        Base.metadata.create_all(bind=engine)
        
        db = SessionLocal()
        try:
            # Crear usuario admin
            admin_user = db.query(User).filter(User.alias == "admin").first()
            if not admin_user:
                hashed_pw = pwd_context.hash("admin")
                new_admin = User(
                    name="Admin",
                    lastname="System",
                    alias="admin",
                    hashed_password=hashed_pw,
                    tel="00000000"
                )
                db.add(new_admin)
                db.commit()
                print("Usuario admin creado.")
            else:
                print(f"El usuario admin ya existe con alias: {admin_user.alias}")
                # Asegurar que la contraseña sea 'admin' si por alguna razón falló antes
                if not pwd_context.verify("admin", admin_user.hashed_password):
                    print("Actualizando contraseña de admin a 'admin'...")
                    admin_user.hashed_password = pwd_context.hash("admin")
                    db.commit()

            # Sembrar productos si la tabla está vacía
            if db.query(Product).count() == 0:
                for p_data in productos_ejemplo:
                    product = Product(**p_data)
                    db.add(product)
                db.commit()
                print("Productos de ejemplo sembrados.")
            else:
                print(f"La tabla de productos ya contiene {db.query(Product).count()} elementos.")
                
        finally:
            db.close()
    except Exception as e:
        print(f"ERROR: No se pudo conectar a la base de datos. Verifique su configuración en el archivo .env")
        print(f"Detalle del error: {e}")
        # No detenemos la aplicación aquí para permitir que FastAPI inicie, 
        # pero los endpoints que requieran DB fallarán.
    
    yield

app = FastAPI(
    title="Lkmx Test API",
    description="API con FastAPI, SQLAlchemy y Auth0",
    version="1.0.0",
    lifespan=lifespan
)

@app.exception_handler(OperationalError)
async def db_operational_error_handler(request: Request, exc: OperationalError):
    return JSONResponse(
        status_code=503,
        content={"detail": "La base de datos no está disponible. Verifique la configuración en el archivo .env"},
    )

app.include_router(public.router, prefix="/api/v1/public", tags=["Public"])
app.include_router(protected.router, prefix="/api/v1/protected", tags=["Protected"])

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de prueba", "docs": "/docs"}
