from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from operateur.models import *
# Create your models here.


class MyAccountManager(BaseUserManager):
    """docstring for MyAccountManager"""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        '''Create and save a user with the given email, and
        password.
        '''
        if not email:
            raise ValueError('L\'adresse email est obligatoire')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must have is_staff=True.'
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must have is_superuser=True.'
            )

        return self._create_user(email, password, **extra_fields)


def get_profile_image_filepath(self, filename):
    # return f'image_de_profiles/{str(self.pk)}/{"image_de_profil.png"}'
    return f'image_de_profiles/user_{self.id}/{filename}'


def get_default_profile_image():
    return 'image_de_profiles/avatar-1.png'


def get_investisseur_carte(self, filename):
    return f'investisseur/carte{self.id}/{filename}'


def get_default_investisseur_carte():
    return 'investisseur/carte.png'


class CustomUser(AbstractBaseUser):
    email = models.EmailField(max_length=65, verbose_name="email", unique=True)
    date_inscription = models.DateTimeField(
        verbose_name='date de creation', auto_now_add=True)
    last_login = models.DateTimeField(
        verbose_name="dernier connexion", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath,
                                      null=True, blank=True)
    objects = MyAccountManager()
    USERNAME_FIELD = 'email'
    # USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "user"

    def __str__(self):
        return '{}'.format(self.email)

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{str(pk)}'):]

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Investisseur(models.Model):
    CIVILITE_TYPE_CHOICES = (
        ("Mr", "Monsieur"), ("Mme", "Madame"), ("Inconnue", "Inconnue"))

    user = models.OneToOneField("CustomUser", on_delete=models.CASCADE)
    prenom = models.CharField(max_length=50, null=True, blank=True)
    nom = models.CharField(max_length=50, null=True, blank=True)
    adresse = models.CharField(max_length=50, null=True, blank=True)
    telephone = models.CharField(max_length=50, null=True, blank=True)
    indicatif = models.CharField(max_length=4, null=True, blank=True)
    cni = models.CharField(max_length=60, null=True)
    carte = models.ImageField(max_length=255, upload_to=get_investisseur_carte,
                              null=True, blank=True)
    civilite = models.CharField(
        max_length=50, choices=CIVILITE_TYPE_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "Investisseur"
        verbose_name_plural = "Investisseurs"
        db_table = "investisseur"

    def __str__(self):
        brand = ""
        if self.prenom is not None:
            brand = self.prenom
        if self.nom is not None:
            brand += " "+self.nom
        if brand != "":
            return brand
        return self.user.email
