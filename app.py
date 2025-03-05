from joblib import load
from typing import Optional
from fastapi import FastAPI 
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

# Chargement du model
loaded_model = load("./model/model.joblib")

#Création du nouvelle instance FastAPI
app = FastAPI()

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials= True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

# Définir un objet pour réaliser des requête
class request_body(BaseModel):
    classe_passager: float
    sexe: str
    age: float

@app.get('/api/')
def get_request():
    return {"message": "hello, world"}

@app.post("/predict")
def predict(data: request_body):
    if data.sexe == 'homme':
        sexe_passager = 1
    else:
        sexe_passager = 0
        
    new_data = new_data = pd.DataFrame(
    [[
        data.classe_passager,
        sexe_passager,
        data.age
    ]])
    
        # Prédiction
    class_predict = round(loaded_model.predict(new_data)[0])
    if class_predict == 1:
        prediction = "Pas mort"
    else:
        prediction  = "Mort"

    # Return la valeur du prédiction
    return {'prediction': prediction }
