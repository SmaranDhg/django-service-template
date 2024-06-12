import logging
from datetime import date
from typing import Type, TypeVar, Union

from django.db import models
from django.db.models import Manager, QuerySet

from ...shared.authentication.models import UserFKMixin
from ...shared.utils.mixins import ModelMixin

_T = TypeVar("_T", bound="PatientMixin")


class Patient(UserFKMixin):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]

    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    address = models.TextField()

    class Meta:
        db_table = "patient"
        unique_together = (("user", "full_name", "gender"),)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "patient"


"""---------------------------User related Mixins---------------------------"""


class PatientMixin(ModelMixin):
    """
    Contains `patient:Patient` attribute related query operations.

    Assertions: `hasattr(cls,'patient')`
    """

    @classmethod
    def new(cls: Type[_T], patient: Patient, /) -> _T:
        """
        Create new instance with the `patient`

        :param patient: instance of `Patient` of which we need related class.
        """
        return cls.objects.create(patient=patient)

    @classmethod
    def of_patient(
        cls: Type[_T] | Type[models.Model],
        patient: Patient,
        /,
        *,
        new_on_absent=False,
        return_all=False,
        warning_if_multiple=False,
        warning_if_absent=True,
    ) -> Union[_T, QuerySet[_T, Manager], None]:
        """
        Give patient {T}
        Also if patient is other patient type the return it so!

        :param new_on_absent: Returns new on if its absent
        :param patient: instance of `Patient` of which we need related class.
        :param other_user: If 'yes' query the company of patient.other_user
        :return: An instance of the class or its subclass.
        """

        qset = cls.objects.filter(patient=patient)
        if return_all:
            return qset
        elif qset.exists():
            if warning_if_multiple and qset.count() > 0:
                logging.warning(f"Multiple {cls.__name__} for Patient {patient}")
            return qset.first()
        elif new_on_absent:
            return cls.new(patient)

        if warning_if_absent:
            logging.warning(f"`{cls.__name__}` doesn't exists for Patient `{patient}`.")

    class Meta:
        abstract = True


class Patient121Mixin(PatientMixin):
    """
    Subclasses `PatientMixin`
    with a attribute `patient` of type `OneToOneField` with `Patient`
    """

    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class PatientFKMixin(PatientMixin):
    """
    Subclasses `PatientMixin`
    with a attribute `patient` of type `OneToOneField` with `Patient`
    """

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    class Meta:
        abstract = True
