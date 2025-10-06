
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from database import Base, engine
from routers import users_router, products_router

Base.metadata.create_all(bind=engine)
app = FastAPI(title="FinalProj")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users_router)
app.include_router(products_router)



# _init__.py:
#
# Olmasa → heç nə import edə bilməzsən.
#
# Boş olsa → import işləyir, amma tam yol yazmalısan.
#
# Dolu olsa → import-u qısaltmaq və paket səviyyəsində setup etmək olur.

# paket səviyyəsində???/