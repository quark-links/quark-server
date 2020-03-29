"""Custom WTForm validators."""
from wtforms.validators import ValidationError


class Unique(object):
    """WTForm validator for ensuring a value doesn't exist in the database."""
    def __init__(self, model, field,
                 message="This value has already been used by someone else."):
        """Create a new unique validator."""
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        """Validate the field."""
        check = self.model.query.filter(self.field == field.data).first()

        if check is not None:
            raise ValidationError(self.message)
