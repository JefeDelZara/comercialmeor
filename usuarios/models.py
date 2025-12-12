from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class UsuarioManager(BaseUserManager):
    def create_user(self, username, email, password=None, tipo_usuario='CLIENTE'):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        
        email = self.normalize_email(email)

        user = self.model(
            username=username,
            email=email,
            tipo_usuario=tipo_usuario
        )

        user.set_password(password)  # encripta contraseña
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password, tipo_usuario='ADMIN')
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    fecha_registro = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    TIPO_USUARIO_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('CLIENTE', 'Cliente'),
    ]

    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPO_USUARIO_CHOICES,
        default='CLIENTE',
        null=False,
        blank=False
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    EMAIL_FIELD = 'email'

    objects = UsuarioManager()

    def __str__(self):
        return self.username
