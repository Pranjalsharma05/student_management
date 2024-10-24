from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework import status
from rest_framework import generics
from .models import (
    Department,
    Degree,
    Course,
    ClassGroup,
    DepartmentCourse,
    Student,
    Teacher,
    HOD,
    CarouselImage,
    Assignment,
    Submission
,
Role,RoleAssignment)
from .serializers import (
    DepartmentSerializer,
    DegreeSerializer,
    CourseSerializer,
    ClassGroupSerializer,
    DepartmentCourseSerializer,
    StudentSerializer,
    TeacherSerializer,
    HODSerializer,
    CarouselImageSerializer,
    AssignmentSerializer,
    SubmissionSerializer,
    RoleSerializer,RoleAssignmentSerializer
)

# Department ViewSet
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

# Degree ViewSet
class DegreeViewSet(viewsets.ModelViewSet):
    queryset = Degree.objects.all()
    serializer_class = DegreeSerializer

# Course ViewSet
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

# DepartmentCourse ViewSet
class DepartmentCourseViewSet(viewsets.ModelViewSet):
    queryset = DepartmentCourse.objects.all()
    serializer_class = DepartmentCourseSerializer

# Teacher ViewSet
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

# HOD ViewSet
class HODViewSet(viewsets.ModelViewSet):
    queryset = HOD.objects.all()
    serializer_class = HODSerializer

# ClassGroup ViewSet
class ClassGroupViewSet(viewsets.ModelViewSet):
    queryset = ClassGroup.objects.all()
    serializer_class = ClassGroupSerializer

    @action(detail=True, methods=['post'])
    def promote_students(self, request, pk=None):
        class_group = self.get_object()
        # Ensure promote_students function is defined and imported
        promote_students(class_group)  
        return Response({'status': 'students promoted'}, status=200)

# Student ViewSet
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @action(detail=False, methods=['get'], url_path='by-class/(?P<degree_id>[^/.]+)/(?P<enrollment_year>[^/.]+)', url_name='by_class')
    def by_class(self, request, degree_id, enrollment_year):
        students = self.queryset.filter(degree=degree_id, enrollment_year=enrollment_year)
        serializer = self.get_serializer(students, many=True)
        
        if students:
            return Response(serializer.data, status=200)
        else:
            return Response({'message': 'No students found.'}, status=404)

# CarouselImage ViewSet
class CarouselImageViewSet(viewsets.ModelViewSet):
    queryset = CarouselImage.objects.all()
    serializer_class = CarouselImageSerializer

# Assignment ViewSet
class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

# Submission ViewSet
class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    @action(detail=False, methods=['get'], url_path='by-assignment/(?P<assignment_id>[^/.]+)', url_name='by_assignment')
    def by_assignment(self, request, assignment_id):
        submissions = self.queryset.filter(assignment_id=assignment_id)
        serializer = self.get_serializer(submissions, many=True)

        if submissions:
            return Response(serializer.data, status=200)
        else:
            return Response({'message': 'No submissions found for this assignment.'}, status=404)


class RoleListCreateView(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class RoleAssignmentViewSet(viewsets.ModelViewSet):
    queryset = RoleAssignment.objects.all()
    serializer_class = RoleAssignmentSerializer
    