from rest_framework import serializers
from django.utils import timezone
from .models import (
    Department, Degree, Course, ClassGroup, DepartmentCourse,
    Student, Teacher, HOD, CarouselImage, Assignment, Submission
,Role,RoleAssignment)

# Department Serializer
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

# Degree Serializer
class DegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Degree
        fields = '__all__'

# Course Serializer
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

# ClassGroup Serializer
class ClassGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassGroup
        fields = '__all__'

# DepartmentCourse Serializer
class DepartmentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentCourse
        fields = '__all__'

# Student Serializer
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    def validate(self, attrs):
        # Example: Add validation for the enrollment year
        if attrs['enrollment_year'] < 2000:
            raise serializers.ValidationError("Enrollment year must be after 2000.")
        return attrs

# Teacher Serializer
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

# HOD Serializer
class HODSerializer(serializers.ModelSerializer):
    class Meta:
        model = HOD
        fields = '__all__'

# CarouselImage Serializer
class CarouselImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarouselImage
        fields = ['id', 'image', 'is_active']

# Assignment Serializer
class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'

    def validate(self, attrs):
        # Example: Ensure due_date is in the future
        if attrs['due_date'] < timezone.now().date():
            raise serializers.ValidationError("Due date must be in the future.")
        return attrs

# Submission Serializer
class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'

    def validate(self, attrs):
        # Example: Ensure a student can only submit once per assignment
        if Submission.objects.filter(student=attrs['student'], assignment=attrs['assignment']).exists():
            raise serializers.ValidationError("You have already submitted this assignment.")
        return attrs


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['role_id', 'name', 'description']

class RoleAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleAssignment
        fields = '__all__'