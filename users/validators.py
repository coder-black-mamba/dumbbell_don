from django.core.validators import RegexValidator
bd_phone_number_validator = RegexValidator(
    regex=r'^\+8801\d{9}$',
    message="Phone number must be entered in the format: +8801234567890. Up to 15 digits allowed.",
)   
