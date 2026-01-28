from ..auth import pwd_context
from ..models import CategoryEnum



EXAMPLE_USER = {
    'name': "Admin",
    'lastname': "System",
    'alias': "admin",
    'hashed_password': pwd_context.hash("admin"),
    'tel': "00000000"
}


EXAMPLE_PRODUCTS = [
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


