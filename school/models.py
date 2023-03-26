from django.db import models
from django.db.models import Q
from django.db.models import Avg
from rest_framework import serializers


class Teacher(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-id',)
        verbose_name = "Teacher"
        verbose_name_plural = "Teacher"


class SchoolClass(models.Model):
    name = models.CharField(max_length=255)
    teacher = models.ManyToManyField(Teacher, related_name='school_classes')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-id',)
        verbose_name = "School Class"
        verbose_name_plural = "School Classes"


class Subject(models.Model):
    name = models.CharField(max_length=255)
    class_name = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-id',)
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"


class Student(models.Model):
    name = models.CharField(max_length=255)
    class_name = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-id',)
        verbose_name = "Student"
        verbose_name_plural = "Students"


class Mark(models.Model):
    GRADE_CHOICES = (
        ('5.00', 'A+'),
        ('4.00', 'A'),
        ('3.50', 'A-'),
        ('3.25', 'B'),
        ('2.00', 'C'),
        ('1.00', 'D'),
        ('0.00', 'F'),
        )
    class_name = models.ForeignKey('school.SchoolClass', on_delete=models.CASCADE, related_name='marks')
    subject = models.ForeignKey('school.Subject', on_delete=models.CASCADE, related_name='marks')
    student = models.ForeignKey('school.Student', on_delete=models.CASCADE, related_name='marks')
    teacher = models.ForeignKey('school.Teacher', on_delete=models.CASCADE, related_name='marks')
    mark = models.IntegerField()
    grade = models.CharField(max_length=5, null=True, blank=True)
    grade_point = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # self.validate_grade(self.grade)
        print(self.mark)
        if self.mark >= 80:
            self.grade = 'A+'
            self.grade_point = 5.0
        elif self.mark >= 70:
            self.grade = 'A'
            self.grade_point = 4.0
        elif self.mark >= 60:
            self.grade = 'A-'
            self.grade_point = 3.5
        elif self.mark >= 50:
            self.grade = 'B'
            self.grade_point = 3.25
        elif self.mark >= 40:
            self.grade = 'C'
            self.grade_point = 2.0
        elif self.mark >= 33:
            self.grade = 'D'
            self.grade_point = 1.0
        else:
            self.grade = 'F'
            self.grade_point = 0.0
        super().save(*args, **kwargs)

    @property
    def gpa(self):
        return self.student.marks.aggregate(avg_grade_point=Avg('grade_point'))['avg_grade_point']

    # def validate_grade(self, value):
    #     valid_choices = [choice[0] for choice in Mark.GRADE_CHOICES]
    #     value = value.strip()  # Strip any whitespace from the value
    #     if value not in valid_choices:
    #         raise serializers.ValidationError(f'{value} is not a valid grade. Valid grades are {valid_choices}.')
    #     return value

    class Meta:
        ordering = ('-id',)
        verbose_name = "Mark"
        verbose_name_plural = "Mark"



# mark_list = Mark.objects.filter(class_name_id=3, mark__gt=33).select_related().prefetch_related()
# subject_list = Subject.objects.filter(class_name_id=3, marks__mark__gt=33).annotate()
