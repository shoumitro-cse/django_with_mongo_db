from rest_framework import serializers
from .models import Subject, SchoolClass, Student, Teacher, Mark
from django.utils.translation import gettext_lazy as _


class SubjectSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(SubjectSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and (request.method == 'POST' or request.method == 'PUT'):
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1

    class Meta:
        model = Subject
        fields = '__all__'
        depth = 0

class SchoolClassSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True)

    class Meta:
        model = SchoolClass
        fields = ['id', 'name', 'subjects']

    def create(self, validated_data):
        subjects_data = validated_data.pop('subjects', [])
        school_class = SchoolClass.objects.create(**validated_data)
        for subject_data in subjects_data:
            subject, created = Subject.objects.get_or_create(**subject_data)
            school_class.subjects.add(subject)
        return school_class    
    
    def update(self, instance, validated_data):
        subjects_data = validated_data.pop('subjects', [])
        instance = super().update(instance, validated_data)
        for subject_data in subjects_data:
            subject, created = Subject.objects.get_or_create(**subject_data)
            instance.subjects.add(subject)
        return instance

class StudentSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(StudentSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and (request.method == 'POST' or request.method == 'PUT'):
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1

    class Meta:
        model = Student
        fields = '__all__'
        depth = 0

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class MarkSerializer(serializers.ModelSerializer):
    
    # GRADE_CHOICES = (
    #     ('5.00', 'A+'),
    #     ('4.00', 'A'),
    #     ('3.50', 'A-'),
    #     ('3.25', 'B'),
    #     ('2.00', 'C'),
    #     ('1.00', 'D'),
    #     ('0.00', 'F'),
    # )

    # grade = serializers.ChoiceField(choices=GRADE_CHOICES, error_messages={
    #     'invalid_choice': _("Invalid grade. Choose a valid grade from A+ to F."),
    # })

    grade = serializers.ChoiceField(choices=Mark.GRADE_CHOICES)
    def __init__(self, *args, **kwargs):
        super(MarkSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and (request.method == 'POST' or request.method == 'PUT'):
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1

    class Meta:
        model = Mark
        fields = '__all__'
        depth = 0