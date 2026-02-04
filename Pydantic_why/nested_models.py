from pydantic import BaseModel

class Address(BaseModel):
    """
    Represents a physical mailing address.

    Attributes:
        address (str): The street address.
        city (str): The city name.
        state (str): The state or province.
        zip (str): The postal or zip code.
        country (str): The country name.
    """
    address: str
    city: str
    state: str
    zip: str
    country: str

class Patient(BaseModel):
    """
    Represents a patient's profile information.

    Attributes:
        name (str): The full name of the patient.
        email (str): The patient's email address.
        phone (str): The patient's contact phone number.
        address (Address): A nested Address model instance.
    """
    name: str
    email: str
    phone: str
    address: Address

# Define raw data for an address in a dictionary format
Address_dict = {
    "address": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip": "12345",
    "country": "USA"
}

# Create an Address instance by unpacking the dictionary.
# Pydantic validates that all required fields are present and are strings.
address1 = Address(**Address_dict)

# Define raw data for a patient, passing the previously created Address object
patient_dict = {
    "name": "John Doe",
    "email": "abc@gmail.com",
    "phone": "123-456-7890",
    "address": address1
}

# Create a Patient instance. 
# Pydantic ensures the 'address' field conforms to the Address model schema.
patient = Patient(**patient_dict)

# Output the validated Patient model instance as a readable string
print(patient)
