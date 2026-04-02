import uuid


def generate_token() -> uuid.UUID:
    """Genera un token UUID4 único y seguro."""
    return uuid.uuid4()