from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    """
    A Pydantic model representing a patient's medical and personal information.
    
    This class handles data validation, transformation (e.g., name casing), 
    and provides methods for simulated CRUD operations.
    """
    name: Annotated[str, Field(..., min_length=2, max_length=50, title="Name of the patient", description="Name of the patient less than 50 characters", examples=["John Doe"])]
    email: EmailStr
    linkedin: AnyUrl
    age: Annotated[int, Field(..., gt=0, lt=100, title="Age of the patient", description="Age of the patient between 0 and 100", examples=[30])]
    married: Optional[bool] = None
    gender: Annotated[str, Field(..., pattern="^(Male|Female|Other)$", title="Gender of the patient", description="Gender of the patient", examples=["Male"])]
    address: str
    phone: str
    city: str
    contact: Dict[str, str]
    allergies: Annotated[Optional[List[str]], Field(default=None, min_items=0, max_items=10)]
    height: int
    weight: Annotated[float, Field(..., gt=0, strict=True, lt=1000, title="Weight of the patient", description="Weight of the patient between 0 and 1000", examples=[75])]
    bmi: float
    verdict: str

    @field_validator("name")
    @classmethod
    def transform_name(cls, value: str) -> str:
        """
        Validator that transforms the patient's name to uppercase.
        """
        return value.upper()

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        """
        Validator that ensures the email domain is restricted to common providers.
        
        Raises:
            ValueError: If the email domain is not in the allowed list.
        """
        valid_domains = ["gmail.com", "yahoo.com", "hotmail.com"]
        domain_name = value.split("@")[1]
        if domain_name not in valid_domains:
            raise ValueError("Invalid email address: domain not supported")
        return value
    
    def insert_patient(self):
        """
        Simulates the logic for inserting a new patient record into a database.
        """
        print(f"--- Inserting Patient: {self.name} ---")
        self._display_info()
         
    def update_patient(self):
        """
        Simulates the logic for updating an existing patient record.
        """
        print(f"--- Updating Patient: {self.name} ---")
        self._display_info()

    def delete_patient(self):
        """
        Simulates the logic for deleting a patient record.
        """
        print(f"--- Deleting Patient: {self.name} ---")
        self._display_info()

    def _display_info(self):
        """
        Helper method to print all patient attributes to the console.
        """
        for field, value in self.model_dump().items():
            print(f"{field}: {value}")

# Test code
if __name__ == "__main__":
    patient_info = {
        "name": "John Doe",
        "email": "abc@gmail.com",
        "linkedin": "https://www.linkedin.com/in/john-doe/",
        "age": 30,
        "married": None,
        "gender": "Male",
        "address": "123 Main St",
        "phone": "123-456-7890",
        "city": "New York",
        "contact": {
            "email": "abc@gmail.com",
            "phone": "123-456-7890"
        },
        "allergies": None,
        "height": 180,
        "weight": 75.0,
        "bmi": 23.15,
        "verdict": "Normal"
    }

    patient1 = Patient(**patient_info)
    patient1.update_patient()