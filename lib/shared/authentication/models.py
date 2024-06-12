import logging
import re
from typing import Type, TypeVar, Union

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models import Manager, Q, QuerySet
from django_tenants.models import DomainMixin, TenantMixin
from rest_framework_simplejwt.tokens import AccessToken


from ..utils.mixins import ModelMixin

_T = TypeVar("_T", bound="ModelMixin")


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    objects = UserManager()
    username = None
    email = models.EmailField(("email address"), unique=True)
    full_name = models.CharField(max_length=200, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "user"


class Tenant(TenantMixin):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_tenant"
    )

    auto_create_schema = True

    @classmethod
    def of_user(cls, user: User, new_on_absent: bool = False) -> "Tenant":
        """
        Retrieve or create a Tenant instance based on the provided user.

        Parameters:
        - user (User): The user for which to retrieve or create a Tenant instance.
        - new_on_absent (bool): If True, create a new Tenant instance if none is found for the user.

        Returns:
        - Tenant: The Tenant instance associated with the provided user.

        """
        qset = cls.objects.filter(user=user)

        if qset:
            return qset.first()
        elif new_on_absent:
            base_schema_name = user.email
            schema_name = re.sub(r"\W|^(?=\d)", "_", base_schema_name.lower())
            schema_name = schema_name[:63]
            Tenant.objects.create(
                user=user,
                schema_name=schema_name,
                name=base_schema_name,
            )

    @classmethod
    def from_auth_token(cls, token: str) -> "Tenant":
        """
        Retrieve a Tenant instance based on the provided authentication token.

        Parameters:
        - token (str): The authentication token used to retrieve the user information.

        Returns:
        - Tenant: The Tenant instance associated with the user from the authentication token.
        """
        decoded_token = AccessToken(token)
        user_id = decoded_token["user_id"]
        user = User.objects.get(pk=user_id)
        return cls.of_user(user, new_on_absent=True)

    class Meta:
        db_table = "user_tenant"


"""---------------------------User related Mixins---------------------------"""


class UserMixin(ModelMixin):
    """
    Contains `user:User` attribute related query operations.

    Assertions: `hasattr(cls,'user')`
    """

    @classmethod
    def new(cls: Type[_T], user: User, /) -> _T:
        """
        Create new instance with the `user`

        :param user: instance of `User` of which we need related class.
        """
        return cls.objects.create(user=user)

    @classmethod
    def of_user(
        cls: Type[_T] | Type[models.Model],
        user: User,
        /,
        *,
        new_on_absent=False,
        return_all=False,
        warning_if_multiple=False,
        warning_if_absent=True,
        other_user_check=False,
    ) -> Union[_T, QuerySet[_T, Manager], None]:
        """
        Give user {T}
        Also if user is other user type the return it so!

        :param new_on_absent: Returns new on if its absent
        :param user: instance of `User` of which we need related class.
        :param other_user: If 'yes' query the company of user.other_user
        :return: An instance of the class or its subclass.
        """
        if other_user_check:
            if other_user := getattr(user, "other_user", None):
                user = other_user
            else:
                print(
                    f"WARNING: given user type: '{type(user)}' is not other-user or `user.other_user` is `none`"
                )

        qset = cls.objects.filter(user=user)
        if return_all:
            return qset
        elif qset.exists():
            if warning_if_multiple and qset.count() > 0:
                logging.warning(f"Multiple {cls.__name__} for User {user}")
            return qset.first()
        elif new_on_absent:
            return cls.new(user)

        if warning_if_absent:
            logging.warning(f"`{cls.__name__}` doesn't exists for User `{user}`.")

    class Meta:
        abstract = True


class User121Mixin(UserMixin):
    """
    Subclasses `UserMixin`
    with a attribute `user` of type `OneToOneField` with `User`
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class UserFKMixin(UserMixin):
    """
    Subclasses `UserMixin`
    with a attribute `user` of type `OneToOneField` with `User`
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True
