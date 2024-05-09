from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from user.enums import SubscriptionChoices


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, password2=None):
        """Создание пользователя

        Создает и сохраняет пользователя с указанным
        адресом электронной почты, именем и паролем.
        """
        if not email:
            raise ValueError("User must have an email address")

        user = self.model(email=self.normalize_email(email), name=name)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """Создание суперпользователя

        Создает и сохраняет суперпользователя с указанным
        адресом электронной почты, датой рождения и паролем.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=255, verbose_name="name")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    is_admin = models.BooleanField(default=False, verbose_name="Is Admin")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created Date"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Updated Date"
    )
    subscription = models.CharField(
        max_length=20,
        choices=SubscriptionChoices.choices,
        default=SubscriptionChoices.FREE,
        verbose_name="Subscription choice",
    )
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin
