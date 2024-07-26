from django.core.exceptions import ValidationError


class CustomPasswordValidator():

    def __init__(self, min_length=1):
        self.min_length = min_length

    def validate(self, password, user=None):
        self.special_characters = set(" !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                ("Le mot de passe doit contenir au moins %(min_length)d nombre.") % {'min_length': self.min_length}
            )
        if not any(char.isalpha() for char in password):
            raise ValidationError(
                ("Le mot de passe doit contenir au moins %(min_length)d lettre.") % {'min_length': self.min_length}
            )
        if not any(char in self.special_characters for char in password):
            raise ValidationError(
                ("Le mot de passe doit contenir au moins %(min_length)d caractère spécial.") % {
                    'min_length': self.min_length}
            )

    def get_help_text(self):
        return ("Votre mot de passe doit contenir au moins 1 lettre, 1 chiffre et 1 caractère spécial")
