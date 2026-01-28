from fastapi import FastAPI
from contextlib import asynccontextmanager
from .endpoints import public, protected
from .database import Base, engine, SessionLocal
from .models import Product, User
from .auth import pwd_context
from sqlalchemy.exc import OperationalError
from fastapi import Request
from fastapi.responses import JSONResponse
from .startup_items.example_data import EXAMPLE_USER, EXAMPLE_PRODUCTS


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
                new_admin = User(**EXAMPLE_USER)
                db.add(new_admin)
                db.commit()
                print("Usuario admin creado.")
            else:
                print(f"El usuario admin ya existe con alias: {admin_user.alias}")
                # Ensure password is 'admin' only if it's not already valid
                try:
                    # Check if the stored string is a valid hash before verifying
                    if admin_user.hashed_password and not admin_user.hashed_password.startswith("$2b$"):
                        is_valid = False
                    else:
                        is_valid = pwd_context.verify("admin", admin_user.hashed_password)
                except Exception as e:
                    print(f"Error verifying password: {e}")
                    is_valid = False
                
                if not is_valid:
                    print("Actualizando contraseña de admin a 'admin'...")
                    admin_user.hashed_password = pwd_context.hash("admin")
                    db.commit()

            # Sembrar productos si la tabla está vacía
            if db.query(Product).count() == 0:
                for p_data in EXAMPLE_PRODUCTS:
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
