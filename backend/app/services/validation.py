def validate_primary_language(primary, available):
    if primary not in available:
        raise ValueError("Primary language must be in available languages")
