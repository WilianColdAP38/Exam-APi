from fastapi import FastAPI
from sqlmodel import SQLModel
from typing import Optional, List, Dict, Any

app = FastAPI(title="CRUD usuarios FastAPI (simple)")

# Modelos 
class User(SQLModel):
    id: int
    username: str
    password: str
    email: Optional[str] = None
    is_active: bool = True

class UserCreate(SQLModel):
    username: str
    password: str
    email: Optional[str] = None
    is_active: bool = True

class UserUpdate(SQLModel):
    username: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None

class Credentials(SQLModel):
    username: str
    password: str

#  "Base de datos" en memoria 
users_db: List[User] = []
next_id = 1  # autoincremental simple

# Helpers 
def find_user_by_id(user_id: int) -> Optional[User]:
    for user in users_db:
        if user.id == user_id:
            return user
    return None

def find_user_by_username(username: str) -> Optional[User]:
    for user in users_db:
        if user.username == username:
            return user
    return None

def safe_user(user: User) -> Dict[str, Any]:
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active,
    }

def add_seed_user() -> None:
    global next_id
    if not find_user_by_username("wilian"):
        users_db.append(User(
            id=next_id,
            username="wilian",
            password="pass123",  # para la prueba controlada
            email="wilian@mail.com",
            is_active=True,
        ))
        next_id += 1

add_seed_user()

#  Endpoints 
@app.get("/")
def root():
    return {"ok": True, "message": "API de Usuarios - CRUD simple OK"}

# Crear usuario
@app.post("/users")
def create_user(data: UserCreate):
    global next_id
    if find_user_by_username(data.username):
        return {"ok": False, "message": "username ya existe"}

    user = User(
        id=next_id,
        username=data.username,
        password=data.password,  # texto plano solo para el ejercicio
        email=data.email,
        is_active=data.is_active,
    )
    users_db.append(user)
    next_id += 1
    return {"ok": True, "message": "usuario creado", "user": safe_user(user)}

# Listar usuarios
@app.get("/users")
def list_users():
    return {"ok": True, "users": [safe_user(user) for user in users_db]}

# Obtener usuario por id
@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = find_user_by_id(user_id)
    if not user:
        return {"ok": False, "message": "no encontrado"}
    return {"ok": True, "user": safe_user(user)}

# Actualizar (excepto password)
@app.put("/users/{user_id}")
def update_user(user_id: int, data: UserUpdate):
    user = find_user_by_id(user_id)
    if not user:
        return {"ok": False, "message": "no encontrado"}

    if data.username and data.username != user.username:
        if find_user_by_username(data.username):
            return {"ok": False, "message": "username ya existe"}
        user.username = data.username

    if data.email is not None:
        user.email = data.email
    if data.is_active is not None:
        user.is_active = data.is_active

    return {"ok": True, "message": "usuario actualizado", "user": safe_user(user)}

# Eliminar usuario
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    user = find_user_by_id(user_id)
    if not user:
        return {"ok": False, "message": "no encontrado"}
    users_db.remove(user)
    return {"ok": True, "message": "usuario eliminado"}

# Login simple
@app.post("/login")
def login(creds: Credentials):
    user = find_user_by_username(creds.username)
    if user and user.password == creds.password and user.is_active:
        return {"ok": True, "message": "login successful"}
    return {"ok": False, "message": "Invalid credentials"}
