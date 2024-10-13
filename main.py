from fastapi import FastAPI, HTTPException
import db_alumnat
import alumnes
from typing import List
from pydantic import BaseModel

app = FastAPI()

class Alumne(BaseModel):
    nomalumne: str
    cicle: str
    curs: int
    grup: str
    idaula: int 

@app.get("/")
def read_root():
    # Retorna un missatge bàsic per indicar que l'API està activa.
    return {"API"}

@app.get("/alumne/list", response_model=List[dict])  
def read_alumnes():
    # Retorna la llista de tots els alumnes.
    alumne_db = db_alumnat.read_all()
    if not alumne_db:
        raise HTTPException(status_code=404, detail="No hi ha alumnes")
    
    alumnes_serialized = alumnes.alumnes_schema(alumne_db)
    return alumnes_serialized

@app.get("/alumne/show/{id}", response_model=dict)
def read_alumne(id: int):
    # Retorna un alumne per la seva ID.
    alumne_db = db_alumnat.read_id(id)  
    if not alumne_db:
        raise HTTPException(status_code=404, detail="Alumne no trobat")  
    
    alumne_serialized = alumnes.alumne_schema(alumne_db)
    return alumne_serialized

@app.post("/alumne/add", response_model=dict)
def add_alumne(alumne: Alumne):
    # Afegeix un nou alumne a la base de dades.
    aula_exists = db_alumnat.check_aula_exists(alumne.idaula) 
    if not aula_exists:
        raise HTTPException(status_code=400, detail="La ID de Aula no existeix")

    db_alumnat.add_alumne(alumne.nomalumne, alumne.cicle, alumne.curs, alumne.grup, alumne.idaula) 

    return {"message": "S'ha afegit correctament"}

@app.delete("/alumne/delete/{id}", response_model=dict)
def delete_alumne(id: int):
    # Elimina un alumne per la seva ID.
    deleted_rows = db_alumnat.delete_alumne(id)
    if deleted_rows == 0:
        raise HTTPException(status_code=404, detail="Alumne no trobat")  
    
    return {"message": "S'ha esborrat correctament"}

@app.put("/alumne/update/{id}", response_model=dict)
def update_alumne(id: int, alumne: Alumne):
    # Actualitza les dades d'un alumne per la seva ID.
    if alumne.idaula is not None:
        aula_exists = db_alumnat.check_aula_exists(alumne.idaula)
        if not aula_exists:
            raise HTTPException(status_code=400, detail="La IdAula no existe")

    updated_rows = db_alumnat.update_alumne(id, alumne.nomalumne, alumne.cicle, alumne.curs, alumne.grup, alumne.idaula)
    
    if updated_rows == 0:
        raise HTTPException(status_code=404, detail="Alumne no trobat") 
    
    return {"message": "S’ha modificat correctament"}
