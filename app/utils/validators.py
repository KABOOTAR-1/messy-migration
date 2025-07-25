import re

EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

def validate_user_data(data, require_password=False):
    errors = {}

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not isinstance(name, str) or len(name) < 2:
        errors["name"] = "Name must be at least 2 characters"

    if not email or not EMAIL_REGEX.match(email):
        errors["email"] = "Invalid email format"

    if require_password:
        if not password or not isinstance(password, str) or len(password) < 6:
            errors["password"] = "Password must be at least 6 characters"

    return errors
