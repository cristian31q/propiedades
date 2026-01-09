from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text  # Importa text para consultas SQL en bruto
from models import Base
from database import engine, sessionlocal
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from routers import (
    PropiedadRouter, UserRouter, TransactionRouter, SalespersonRouter, 
    TaxRouter, TenantRouter, ContractRouter, OwnershipRouter, 
    InmobiliariaRouter, RegistroRouter, OwnerpropertyRouter, EntityFileRouter,
    PropertyStoryRouter
)
import sqlalchemy.exc as exc
import uvicorn

def getDB():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(PropiedadRouter.router)
app.include_router(UserRouter.router)
app.include_router(TransactionRouter.router)
app.include_router(SalespersonRouter.router)
app.include_router(TaxRouter.router)
app.include_router(TenantRouter.router)
app.include_router(ContractRouter.router)
app.include_router(OwnershipRouter.router)
app.include_router(InmobiliariaRouter.router)
app.include_router(RegistroRouter.router)
app.include_router(OwnerpropertyRouter.router)
app.include_router(EntityFileRouter.router)
app.include_router(PropertyStoryRouter.router)
db_dependencies = Annotated[Session, Depends(getDB)]

@app.get("/")
def HelloWorld(db: db_dependencies):
    try:
        # Usar text() para la consulta en bruto
        result = db.execute(text("SELECT 1")).fetchone()
        if result is not None:
            return {"message": "Conexión a la base de datos exitosa!"}
        else:
            raise HTTPException(status_code=500, detail="Error al acceder a la base de datos")
    except exc.SQLAlchemyError as e:
        # Captura cualquier error relacionado con la base de datos
        raise HTTPException(status_code=500, detail=f"Error de conexión: {str(e)}")
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
