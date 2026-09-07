from rest_framework.exceptions import ValidationError

class InvalidStateTransitionError(ValidationError):
    def __init__(self, old_status, new_status):
        detail = f"Invalid status transition from '{old_status}' to '{new_status}'."
        super().__init__(detail={'status': detail})
