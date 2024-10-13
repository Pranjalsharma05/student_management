from rest_framework import serializers
from .models import Department, Degree, Course, ClassGroup, DepartmentCourse, Student, Teacher, HOD, CarouselImage

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


class CarouselImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarouselImage
        fields = ['id', 'image', 'is_active']