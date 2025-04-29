from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin  
from django.db import models  
from django.core.exceptions import ValidationError  
from django.conf import settings  
from django.contrib.admin.models import LogEntry

# Token._meta.get_field('user').remote_field.model = settings.AUTH_USER_MODEL
LogEntry._meta.get_field("user").remote_field.model = settings.AUTH_USER_MODEL

# Manager użytkowników
class UserAccountManager(BaseUserManager):
    def create_user(self, email, login, password=None, **extra_fields):
        if not email:
            raise ValueError("Użytkownik musi mieć adres e-mail")
        if not login:
            raise ValueError("Użytkownik musi mieć login")

        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        user = self.model(email=email, login=login, **extra_fields)

        if password:
            user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, login, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser musi mieć is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser musi mieć is_superuser=True.")

        return self.create_user(email, login, password, **extra_fields)


class UserAccount(AbstractBaseUser, PermissionsMixin):
    id_role = models.ForeignKey("Role", null=True, blank=True, on_delete=models.SET_NULL)
    email = models.EmailField(unique=True)
    login = models.CharField(max_length=50, unique=True)
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # atrybuty wymagane do panelu admina
    is_staff = models.BooleanField(default=False) 
    is_superuser = models.BooleanField(default=False)  

    objects = UserAccountManager()

    USERNAME_FIELD = "email" 
    REQUIRED_FIELDS = ["login"]

    groups = models.ManyToManyField(
        "auth.Group",
        blank=True
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        blank=True
    )

    def clean(self):
        if len(self.login) < 4:
            raise ValidationError("Login musi mieć co najmniej 4 znaki.")

    def __str__(self):
        return self.login


# tabela ról użytkowników
class Role(models.Model):
    rola = models.CharField(max_length=50)

    def __str__(self):
        return self.rola


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
