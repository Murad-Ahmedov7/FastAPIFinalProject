from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from auth import decode_token
from database import SessionLocal
from models.user import Role,User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
def get_db():
    db:Session=SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db))->User:
    cred_exc=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials",headers={"WWW-Authenticate":"Bearer"})
    try:
        payload=decode_token(token)
        email:str=payload.get("sub")
        if not email:
            raise cred_exc
    except JWTError:
        raise cred_exc
    user=db.query(User).filter(User.email==email).first()
    if not user or not user.is_active:
        raise cred_exc
    return user

def require_roles(*roles:Role):
    def _dep(current:User = Depends(get_current_user)) ->User:
        if current.role not in roles:
            raise HTTPException(status_code=403,detail="Forbidden")
        return current
    return _dep
#
#
# Sənin require_roles nümunəndə closure belə işləyir:
#
# def require_roles(*roles: Role):
#     # Bu xarici funksiya closure yaradır
#     def _dep(current: User = Depends(get_current_user)) -> User:
#         # _dep daxili funksiya, xaricdən gələn 'roles' dəyişənini yadda saxlayır
#         if current.role not in roles:
#             raise HTTPException(status_code=403, detail="Forbidden")
#         return current
#     return _dep  # _dep funksiyasını qaytarır, amma hələ icra olunmayıb
#
# Sətr-sətr necə işləyir:
#
# require_roles(Role.admin) çağırılır
#
# _dep funksiyası yaradılır
#
# Xarici funksiyadan gələn roles (Role.admin) _dep-də yadda saxlanılır
#
# _dep funksiyası geri qaytarılır, amma hələ icra olunmayıb
#
# FastAPI endpoint çağırılır:
#
# @router.post(
#     '/',
#     response_model=AuthorOut,
#     dependencies=[Depends(require_roles(Role.admin))],
#     status_code=201
# )
# def create_author(payload: AuthorCreate, db: Session = Depends(get_db)):
#     ...
#
#
# Burada Depends(require_roles(Role.admin)) → _dep funksiyası icra olunur
#
# _dep current: User = Depends(get_current_user) vasitəsilə user məlumatını alır
#
# _dep yoxlayır: current.role in roles
#
# Əgər yoxsa → 403 Forbidden
#
# Əgər varsa → current qaytarılır
#
# _dep qaytardığı dəyər (current) artıq endpoint içində istifadə oluna bilər (məsələn, lazım olsa create_author daxilində istifadə etmək üçün)
#
# 💡 Qısaca:
#
# return _dep → closure obyekti yaradır, hələ icra olunmayıb
#
# _dep → sorğu gələndə icra olunur, rol yoxlaması edir
#
# current → sorğu üçün aktiv user obyektidir
#
# İstəsən mən bunu şəkil və axın diagramı ilə göstərim ki, “xarici funksiya, daxili funksiya, sorğu və return-lər” tam aydın olsun.

#closure deiler buna