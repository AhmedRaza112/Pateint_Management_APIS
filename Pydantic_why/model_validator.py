from pydantic import BaseModel, EmailStr, AnyUrl, model_validator
from typing import List, Dict

class Patient(BaseModel):
    """
    A Pydantic model representing a patient's comprehensive profile.

    Attributes:
        name (str): The full name of the patient.
        email (EmailStr): A validated email address.
        linkedin (AnyUrl): A validated URL for the patient's LinkedIn profile.
        age (int): The age of the patient.
        married (bool): Marital status of the patient.
        gender (str): The gender of the patient.
        address (str): The residential address of the patient.
        phone (str): The primary contact phone number.
        city (str): The city where the patient resides.
        contact (Dict[str, str]): A dictionary containing contact information (e.g., secondary email, phone).
        allergies (List[str]): A list of known medical allergies.
        height (int): The height of the patient in centimeters.
        weight (float): The weight of the patient in kilograms.
        bmi (float): The Body Mass Index of the patient.
        verdict (str): A summary medical verdict or status.
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
    height: int
    weight: float
    bmi: float
    verdict: str

    @model_validator(mode="before")
    @classmethod
    def validate_emergency_contact(cls, model: Dict) -> Dict:
        """
        Validates the input data before model instantiation.
        
        Specifically checks if patients over the age of 60 have an 'emergency' 
        key present in their contact information dictionary.

        Args:
            model (Dict): The raw dictionary of data passed to the model constructor.

        Returns:
            Dict: The original model data if validation passes.

        Raises:
            ValueError: If the patient is older than 60 and lacks an emergency contact.
        """
        if model.get("age", 0) > 60 and 'emergency' not in model.get("contact", {}):
            raise ValueError("Emergency contact is required for patients above 60 years")
        return model
    
    def update_patient(self):
        """
        Logs the current state of the patient's attributes to the console.
        Useful for debugging or verifying the loaded data.
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
        print(f"Height: {self.height}")
        print(f"Weight: {self.weight}")
        print(f"BMI: {self.bmi}")
        print(f"Verdict: {self.verdict}")

# --- Execution Logic ---

# Define raw input data representing a patient
pateint_info = {
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
    "bmi": 23.15,
    "verdict": "Normal"
}

# Instantiate the Patient object. Pydantic will perform type checking and run validators.
pateint1 = Patient(**pateint_info)

# Call the instance method to display the patient's information
pateint1.update_patient()