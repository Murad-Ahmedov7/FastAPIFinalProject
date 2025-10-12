
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from database import Base, engine
from routers import users_router, products_router_user, products_router_admin, basket_router, order_router
from models import *
Base.metadata.create_all(bind=engine)
app = FastAPI(title="FinalProj")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users_router)
app.include_router(products_router_user)
app.include_router(products_router_admin)

app.include_router(basket_router)

app.include_router(order_router)



# _init__.py:
#
# Olmasa → heç nə import edə bilməzsən.
#
# Boş olsa → import işləyir, amma tam yol yazmalısan.
#
# Dolu olsa → import-u qısaltmaq və paket səviyyəsində setup etmək olur.

# paket səviyyəsində???/