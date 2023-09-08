from django.core.exceptions import ValidationError


def validate_not_null(value):
    """Валидатор для положительного числа."""
    if value == 0:
        raise ValidationError(('Значение должно быть больше 0.'))
