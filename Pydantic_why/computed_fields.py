from pydantic import BaseModel, EmailStr, AnyUrl, computed_field
from typing import List, Dict

class Patient(BaseModel):
    """
    A Pydantic model representing a patient's profile.
    
    This class handles data validation for patient attributes and automatically 
    calculates health metrics like BMI using computed fields.
    """
    name: str
    email: EmailStr
    linkedin: AnyUrl
    age: int
    married: bool
    gender: str
    address: str
    phone: str
    city: str
    contact: Dict[str, str]
    allergies: List[str]
    height: int  # measured in cm
    weight: float  # measured in kg

    @computed_field
    @property
    def bmi(self) -> float:
        """
        Calculates the Body Mass Index (BMI).
        
        Formula: weight (kg) / (height (m) ^ 2)
        Returns: float rounded to 2 decimal places.
        """
        return round(self.weight / (self.height / 100) ** 2, 2)

    @computed_field
    @property
    def bmi_verdict(self) -> str:
        """
        Determines the weight category based on the calculated BMI.
        
        Categories:
        - Underweight: BMI < 18.5
        - Normal: 18.5 <= BMI < 25
        - Overweight: 25 <= BMI < 30
        - Obesity: BMI >= 30
        """
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obesity"
    
    def update_patient(self):
        """
        Prints a formatted summary of the patient's record to the console.
        """
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"LinkedIn: {self.linkedin}")
        print(f"Age: {self.age}")
        print(f"Married: {self.married}")
        print(f"Gender: {self.gender}")
        print(f"Address: {self.address}")
        print(f"Phone: {self.phone}")
        print(f"City: {self.city}")
        print(f"Contact: {self.contact}")
        print(f"Allergies: {self.allergies}")
        print(f"Height: {self.height} cm")
        print(f"Weight: {self.weight} kg")
        print(f"BMI (Computed): {self.bmi}")
        print(f"Verdict (Computed): {self.bmi_verdict}")

# --- Execution Logic ---

# Define raw input data for a patient
patient_info = {
    "name": "John Doe",
    "email": "abc@gmail.com",
    "linkedin": "https://www.linkedin.com/in/john-doe/",
    "age": 30,
    "married": True,
    "gender": "Male",
    "address": "123 Main St",
    "phone": "123-456-7890",
    "city": "New York",
    "contact": {
        "email": "abc@gmail.com",
        "phone": "123-456-7890"
    },
    "allergies": ['Penicillin', 'Peanuts'],
    "height": 180,
    "weight": 75,
}

# Instantiate the Patient object. 
# Pydantic validates types and constraints during initialization.
patient1 = Patient(**patient_info)

# Display the processed patient information
patient1.update_patient()