
from django.db import models
# OBS   preciso verificar se consigo trazer informacao do user para essa model com import
from account import User

class Environment(models.Model):
    properties_choices = (
        ("Apartment", "apartment"),
        ("House", "house"),
        ("Others", "others")
    )

    property_type = models.CharField(
        max_length=30,
        choices=properties_choices,
        null=False,
        blank=False
    )
    name = models.CharField()


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="User responsable by this budget")
    name = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(
        null=False,
        blank=False,
        help_text="Text descripting the request client in the current quote"
    )
    created_at = models.DateField(auto_now=True)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class BudgetItems(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name="items")
    measures = models.CharField(max_length=150, null=True, blank=False,
                                help_text='Insira aqui as medidas apartamento/casa')



class Image(models.Model):
    thumbnail = models.FileField(null=True, blank=True, help_text='Envie fotos do seu apartamento/casa')
    describe = models.TextField(null=False, blank=False, help_text='Conte pra gente tudo sobre seu espaço')
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name="images")
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images_user")

    def __str__(self):
        return self.thumbnail