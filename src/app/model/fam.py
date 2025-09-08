from typing import Optional, List, Any
from pydantic import BaseModel, field_validator
from datetime import date, datetime
from decimal import Decimal

from app.model.address import AddressModel

class FAMModel(BaseModel):
    # --- Required Fields ---
    health_insurance_company: str
    patient_nr: str
    pzn: str
    medicine_name: str
    medicine_price: Decimal
    prescription_date: date
    amount: int
    receipt_id: str
    vo_id: str
    
    # --- Optional Fields ---
    lanr: Optional[str] = None
    doctor_title: Optional[str] = None
    doctor_first_name: Optional[str] = None
    doctor_last_name: Optional[str] = None
    doctor_address: Optional[AddressModel] = None
    pharmacy_name: Optional[str] = None
    pharmacy_address: Optional[AddressModel] = None
    bs_nr: Optional[str] = None
    bs_name: Optional[str] = None
    doctor_phone: Optional[str] = None
    kv_district: Optional[str] = None
    doctor_specialization: Optional[str] = None
    role: Optional[str] = None
    billing_date: Optional[date] = None
    temp_lanr: Optional[str] = None
    doctor_id: Optional[str] = None
    pharmacy_owner: Optional[str] = None
    ihpe_units: Optional[int] = None


    @field_validator(
        'health_insurance_company', 'patient_nr', 'medicine_name', 'pharmacy_name',
        'pharmacy_owner', 'doctor_first_name', 'doctor_last_name', 
        'doctor_specialization', 'bs_name', 'role'
    )
    @classmethod
    def validate_required_text(cls, v: str):
        if not v.strip():
            raise ValueError("Field cannot be empty.")
        if v.isdigit():
            raise ValueError("Field cannot consist only of numbers.")
        return v

    @field_validator(
        'pzn', 'receipt_id', 'vo_id', 'lanr', 'bs_nr', 'doctor_id', 
        'temp_lanr', 'kv_district', 'doctor_phone'
    )
    @classmethod
    def validate_numeric_string(cls, v: Optional[str]):
        if v is None:
            return v  # Allow optional fields to be None
        if not v.strip():
            raise ValueError("Field cannot be empty.")
        if not v.isdigit():
            raise ValueError("Field must contain only digits.")
        return v

    @field_validator('amount', 'ihpe_units')
    @classmethod
    def validate_positive_integer(cls, v: Optional[int]):
        if v is not None and v < 0:
            raise ValueError("Value cannot be negative.")
        return v

    @field_validator('medicine_price')
    @classmethod
    def validate_positive_price(cls, v: Decimal):
        if v < 0:
            raise ValueError("Price cannot be negative.")
        return v
 
    @field_validator('prescription_date', 'billing_date', mode='before')
    @classmethod
    def validate_and_parse_date(cls, v: Any):
        if v is None:
            return v
        if isinstance(v, (date, datetime)):
             return v
        if not isinstance(v, str) or not v.strip():
            raise ValueError("Date must be a non-empty string.")
        try:
            return datetime.strptime(v, '%d.%m.%Y').date()
        except ValueError:
            raise ValueError("Date must be in dd.mm.yyyy format.")


    @field_validator('doctor_title')
    @classmethod
    def validate_doctor_title(cls, v: Optional[str]):
        if v is None:
            return v
        allowed = ["Dr.", "Dr. Dr.", "", "Prof. Dr.", "PD Dr.", "PD Dr. Dr.", "Prof. Dr. Dr."]
        if v not in allowed:
            raise ValueError(f"'{v}' is not a valid title.")
        return v
    