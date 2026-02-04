from pydantic import BaseModel

class Address(BaseModel):
    """
    Data model representing a physical mailing address.
    """
    address: str
    city: str
    state: str
    zip: str
    country: str

class Patient(BaseModel):
    """
    Data model representing a patient's personal and contact information.
    Includes a nested Address model.
    """
    name: str
    email: str
    phone: str
    address: Address

# Dictionary containing raw address data
Address_dict = {
    "address": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip": "12345",
    "country": "USA"
}

# Instantiate the Address model by unpacking the dictionary
address1 = Address(**Address_dict)

# Dictionary containing raw patient data, incorporating the Address instance
patient_dict = {
    "name": "John Doe",
    "email": "abc@gmail.com",
    "phone": "123-456-7890",
    "address": address1
}

# Instantiate the Patient model
patient = Patient(**patient_dict)

# .model_dump() serializes the model instance into a Python dictionary.
# The 'include' parameter filters the output to only contain the specified fields.
temp = patient.model_dump(include=["name"])

# .model_dump_json() serializes the model instance into a JSON string.
# The 'exclude' parameter removes the specified fields from the resulting JSON.
temp_json = patient.model_dump_json(exclude=["address"])

# Output the results of serialization to demonstrate types and contents
print(f"Dictionary Serialization Type: {type(temp)}")
print(f"Dictionary Serialization Output: {temp}")
print(f"JSON Serialization Type: {type(temp_json)}")
print(f"JSON Serialization Output: {temp_json}")
