import jwt
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from gameplay.dices import roll_ability_dice
from robots.utils import craete_new_name


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def with_perm(
        self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), blank=True, unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    experience = models.IntegerField(_("experience"), default=0)
    level = models.IntegerField(_("level"), default=1)
    robot_options = models.JSONField(_("robot options"), default=dict)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    objects = UserManager()

    def add_experience(self, value: int):
        self.experience += value
        self.save()

    def generate_new_robot_options(self):
        key = settings.SECRET_KEY
        options = [
            {
                "name": craete_new_name(),
                "data": {
                    "strength": roll_ability_dice(),
                    "dexterity": roll_ability_dice(),
                    "intelligence": roll_ability_dice(),
                    "constitution": roll_ability_dice(),
                    "wisdom": roll_ability_dice(),
                    "charisma": roll_ability_dice(),
                }
            },
            {
                "name": craete_new_name(),
                "data": {
                    "strength": roll_ability_dice(),
                    "dexterity": roll_ability_dice(),
                    "intelligence": roll_ability_dice(),
                    "constitution": roll_ability_dice(),
                    "wisdom": roll_ability_dice(),
                    "charisma": roll_ability_dice(),
                }
            },
            {
                "name": craete_new_name(),
                "data": {
                    "strength": roll_ability_dice(),
                    "dexterity": roll_ability_dice(),
                    "intelligence": roll_ability_dice(),
                    "constitution": roll_ability_dice(),
                    "wisdom": roll_ability_dice(),
                    "charisma": roll_ability_dice(),
                }
            },
        ]
        for option in options:
            option["key"] = jwt.encode(option["data"], key, algorithm="HS256")
        self.robot_options = options
        self.save()

    def get_max_robots(self):
        return 1
