from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
from fastapi.responses import JSONResponse
import json
app=FastAPI()

class Pateint(BaseModel):
    id:Annotated[str,Field(...,description="Enter the patient ID",title="Patient ID",examples=["P001"])]
    name:Annotated[str,Field(...,description="Enter the patient name",title="Patient Name",examples=["John Doe"])]
    city:Annotated[str,Field(...,description="Enter the patient city",title="Patient City",examples=["New York"])]
    age:Annotated[int,Field(...,gt=0,lt=120, description="Enter the patient age",title="Patient Age",examples=[30])]
    gender:Annotated[Literal["Male","Female","Other"],Field(...,description="Enter the patient gender",title="Patient Gender",examples=["Male"])]
    height:Annotated[float,Field(...,gt=0,lt=300,description="Enter the patient height",title="Patient Height",examples=[180])]
    weight:Annotated[float,Field(...,gt=0,lt=1000,description="Enter the patient weight",title="Patient Weight",examples=[75])]
    
    @computed_field
    def bmi(self)->float:
        bmi = round(self.weight / (self.height / 100) ** 2,2)
        return bmi
    @computed_field
    def verdict(self)->str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obesity"


class PateintUpdate(BaseModel):
    name:Annotated[Optional[str],Field(None,description="Enter the patient name",title="Patient Name",examples=["John Doe"])]
    city:Annotated[Optional[str],Field(None,description="Enter the patient city",title="Patient City",examples=["New York"])]
    age:Annotated[Optional[int],Field(None,gt=0,lt=120, description="Enter the patient age",title="Patient Age",examples=[30])]
    gender:Annotated[Optional[Literal["Male","Female","Other"]],Field(None,description="Enter the patient gender",title="Patient Gender",examples=["Male"])]
    height:Annotated[Optional[float],Field(None,gt=0,lt=300,description="Enter the patient height",title="Patient Height",examples=[180])]
    weight:Annotated[Optional[float],Field(None,gt=0,lt=1000,description="Enter the patient weight",title="Patient Weight",examples=[75])]

def load_data():
    with open("pateints.json", "r") as f:
        data = json.load(f)
        return data

def save_data(data):
    with open("pateints.json", "w") as f:
        json.dump(data, f, indent=4)

@app.get("/")
def Hello():
    return {"Message":"Pateint Management system api"}

@app.get("/about")
def About():
    return{"Message":"A fully functional API to maange Your pateint records"}

@app.get("/view")
def get_patients():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def get_patient(patient_id:str = Path(..., description="Enter the patient ID", title="Patient ID", examples=["P001"])):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/sort")
def sort_patients(sort_by:str = Query("name", description="sort in the basis of name, age, gender, address, phone, city, height, weight, bmi, verdict"), order:str = Query("asc", description="sort order: asc or desc")):
    valid_fields = ["name", "age", "gender", "address", "phone", "city", "height", "weight", "bmi", "verdict"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"invalid filed select from {valid_fields}")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="invalid order select from asc or desc")
    data = load_data()

    sort_order = True if order == "desc" else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)
    return sorted_data

@app.post("/create")
def create_patient(patient:Pateint):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")
    data[patient.id] = patient.model_dump(exclude=["id"])
    save_data(data)
    return JSONResponse(status_code=201, content={"message": "Patient created successfully"})


@app.put("/edit/{patient_id}")
def update_patient(patient_id:str, patient_update:PateintUpdate):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
        
    existing_patient_info = data[patient_id]
    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value
    
    existing_patient_info['id'] = patient_id
    patient_pydantic_object = Pateint(**existing_patient_info)
    
    existing_patient_info = patient_pydantic_object.model_dump(exclude=["id"])
    data[patient_id] = existing_patient_info
    save_data(data)
    return JSONResponse(status_code=200, content={"message": "Patient updated successfully"})
   

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id:str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200, content={"message": "Patient deleted successfully"})
