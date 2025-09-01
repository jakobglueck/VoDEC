from typing import Optional
from pydantic import BaseModel, field_validator

class AddressModel(BaseModel):
    street: Optional[str] = None
    postcode: Optional[str] = None
    city: Optional[str] = None

    @field_validator('street')
    @classmethod
    def validate_street(cls, v: str) -> Optional[str]:
        if v is None:
            return v

        if not v.strip():
            raise ValueError("Street cannot be empty or just spaces.")
            
        if v.isdigit():
            raise ValueError("Street cannot consist of numbers alone.")
            
        return v
    
    @field_validator('postcode')
    @classmethod
    def validate_postcode(cls, v: str) -> Optional[str]:
        if v is None:
            return v
        
        if not v.isdigit():
            raise ValueError("Postcode must only contain numbers.")
            
        if len(v) != 5:
            raise ValueError("Postcode must have exactly five digits.")
            
        return v
    
    @field_validator('city')
    @classmethod
    def validate_city(cls, v: str) -> Optional[str]:
        if v is None:
            return v

        if not v.strip():
            raise ValueError("City cannot be empty or just spaces.")
            
        if v.isdigit():
            raise ValueError("A city name cannot consist only of numbers.")
            
        return v
    