from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
UserModel = get_user_model()

def custom_validation(data):
    email = data['email'].strip()
    name = data['name'].strip()  # Updated from username to name
    password = data['password'].strip()

    # Validate email
    if not email or UserModel.objects.filter(email=email).exists():
        raise ValidationError('Choose another email')

    # Validate password
    if not password or len(password) < 8:
        raise ValidationError('Choose another password, min 8 characters')

    # Validate name
    if not name:
        raise ValidationError('Name is required')
    
    return data


def validate_email(data):
    email = data['email'].strip()
    if not email:
        raise ValidationError('An email is needed')
    return True

def validate_password(data):
    password = data['password'].strip()
    if not password:
        raise ValidationError('A password is needed')
    return True