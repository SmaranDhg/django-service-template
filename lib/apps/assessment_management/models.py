from dataclasses import dataclass

from django.db import models

from lib.apps.patient_management.models import PatientFKMixin


@dataclass
class QandAModel:
    question: str
    answer: str


class Assessment(PatientFKMixin):
    
    ASSESSMENT_TYPE_CHOICES = [
        ("CS", "Cognitive Status"),
        ("PA", "Physical Assessment"),
    ]
    name = models.CharField(max_length=250, default="Assessments")
    assessment_type = models.CharField(max_length=2, choices=ASSESSMENT_TYPE_CHOICES)
    assessment_date = models.DateField()
    q_and_a = models.JSONField(default=list)
    final_score = models.IntegerField()
    class Meta:
        db_table = "assessment"
        unique_together = (("patient", "name"),)
        

    def __str__(self):
        return f"{self.get_assessment_type_display()} - {self.patient.full_name} on {self.assessment_date}"
