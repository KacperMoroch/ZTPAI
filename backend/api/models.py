from django.db import models


# tabela ról użytkowników
class Role(models.Model):
    rola = models.CharField(max_length=50)

    def __str__(self):
        return self.rola

# tabela kont użytkowników
class UserAccount(models.Model):
    id_role = models.ForeignKey(Role, null=True, on_delete=models.SET_NULL)
    email = models.EmailField(unique=True)
    login = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)
    salt = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.login

# tabela krajów
class Country(models.Model):
    name = models.CharField(max_length=100)
    flag_image_path = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

# tabela lig
class League(models.Model):
    name = models.CharField(max_length=100)
    logo_image_path = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

# tabela klubów
class Club(models.Model):
    name = models.CharField(max_length=100)
    logo_image_path = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

# tabela pozycji
class Position(models.Model):
    name = models.CharField(max_length=50)
    position_image_path = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

# tabela wieku
class Age(models.Model):
    value = models.IntegerField()
    age_image_path = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.value)

# tabela numerów koszulek
class ShirtNumber(models.Model):
    number = models.IntegerField()
    number_image_path = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.number)

# tabela pikarzy
class Player(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    age = models.ForeignKey(Age, on_delete=models.CASCADE)
    shirt_number = models.ForeignKey(ShirtNumber, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
