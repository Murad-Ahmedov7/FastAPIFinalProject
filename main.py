
from fastapi import FastAPI
from database import Base, engine
from routers import users_router


Base.metadata.create_all(bind=engine)
app = FastAPI(title="FinalProj")


app.include_router(users_router)



# _init__.py:
#
# Olmasa → heç nə import edə bilməzsən.
#
# Boş olsa → import işləyir, amma tam yol yazmalısan.
#
# Dolu olsa → import-u qısaltmaq və paket səviyyəsində setup etmək olur.

# paket səviyyəsində???/