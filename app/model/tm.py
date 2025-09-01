from typing import Optional, List, Any
from pydantic import BaseModel, field_validator
from decimal import Decimal

class TMModel(BaseModel):
    # --- Required Fields (Pflichtangaben) ---
    vo_id: str
    charge_nr: str
    position: int
    pzn: str
    bezeichnung: str
    faktorenkennzeichen: str
    mengenfaktor: float
    teilmengen_preis: Decimal
    
    # --- Optional Fields ---
    preiskennzeichen: Optional[str] = None
    packungsgroesse: Optional[str] = None
    mengeneinheit: Optional[str] = None
    darreichungsform: Optional[str] = None
    atc_code: Optional[str] = None
    atc_bezeichnung: Optional[str] = None

    # --- Reusable Validators ---

    @field_validator('charge_nr', 'bezeichnung', 'faktorenkennzeichen')
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
        'preiskennzeichen', 'packungsgroesse', 'mengeneinheit', 
        'darreichungsform', 'atc_code', 'atc_bezeichnung'
    )
    @classmethod
    def validate_optional_text(cls, v: Optional[str]):
        if v is not None and not v.strip():
            raise ValueError("Field cannot be empty if provided.")
        return v

    @field_validator('position', 'mengenfaktor', 'teilmengen_preis')
    @classmethod
    def validate_positive_number(cls, v):
        if v is None:
            # This check is for safety, but these fields are required
            raise ValueError("Required numeric field cannot be None.")
        if v <= 0:
            raise ValueError("Value must be positive and greater than zero.")
        return v
    
    @field_validator('mengenfaktor')
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
    