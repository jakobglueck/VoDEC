from typing import Optional, List, Any
from pydantic import BaseModel, field_validator
from decimal import Decimal

class TMModel(BaseModel):
    # --- Required Fields (Pflichtangaben) ---
    vo_id: str
    charge_nr: str
    position: int
    pzn: str
    am_name: str
    factor_indicator: str
    quantity_factor: float
    partial_quantity_price: Decimal
    
    # --- Optional Fields ---
    price_indicator: Optional[str] = None
    package_size: Optional[str] = None
    unit_of_measurement: Optional[str] = None
    presentation_form: Optional[str] = None
    atc_code: Optional[str] = None
    atc_name: Optional[str] = None


    @field_validator('charge_nr', 'am_name', 'factor_indicator')
    @classmethod
    def validate_required_text(cls, v: str):
        if not v or not v.strip():
            raise ValueError("Field cannot be empty.")
        return v

    @field_validator('vo_id', 'pzn')
    @classmethod
    def validate_required_numeric_string(cls, v: str):
        if not v or not v.strip():
            raise ValueError("Field cannot be empty.")
        if not v.isdigit():
            raise ValueError("Field must contain only digits.")
        return v

    @field_validator(
        'price_indicator', 'package_size', 'unit_of_measurement', 
        'presentation_form', 'atc_code', 'atc_name'
    )
    @classmethod
    def validate_optional_text(cls, v: Optional[str]):
        if v is not None and not v.strip():
            raise ValueError("Field cannot be empty if provided.")
        return v

    @field_validator('position', 'factor_indicator', 'partial_quantity_price')
    @classmethod
    def validate_positive_number(cls, v):
        if v is None:
            # This check is for safety, but these fields are required
            raise ValueError("Required numeric field cannot be None.")
        if v <= 0:
            raise ValueError("Value must be positive and greater than zero.")
        return v
    
    @field_validator('factor_indicator')
    @classmethod
    def validate_four_decimal_places(cls, v: Decimal) -> Decimal:

        value_str = str(v)

        if '.' in value_str:

            decimal_part = value_str.split('.')[1]
 
            if len(decimal_part) != 4:
                raise ValueError("The value must have exactly four decimal places.")
        else:
            raise ValueError("The value must have exactly four decimal places.")
        return v
    