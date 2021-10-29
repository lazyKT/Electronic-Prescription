"""
# Utitlies functions such as data validation, regex etc
"""

def validate_prescription (data):
    """
    # Validate the prescription create request
    """
    if 'patient' not in data or 'identifier' not in data or 'pharmacist' not in data or 'medication' not in data or 'from_date' not in data or 'to_date' not in data:
        return False
    return True
