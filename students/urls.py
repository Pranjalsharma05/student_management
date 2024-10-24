from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    DepartmentViewSet,
    DegreeViewSet,
    CourseViewSet,
    DepartmentCourseViewSet,
    ClassGroupViewSet,
    StudentViewSet,
    TeacherViewSet,
    HODViewSet,
    CarouselImageViewSet,
    AssignmentViewSet,
    SubmissionViewSet,
    RoleListCreateView,
    RoleAssignmentViewSet
)

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'degrees', DegreeViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'department-courses', DepartmentCourseViewSet)
router.register(r'roles', RoleListCreateView, basename='role')
router.register(r'teachers', TeacherViewSet)
router.register(r'hods', HODViewSet)
router.register(r'class-groups', ClassGroupViewSet)
router.register(r'students', StudentViewSet)
router.register(r'assignments', AssignmentViewSet)
router.register(r'submissions', SubmissionViewSet)
router.register(r'carousel', CarouselImageViewSet)
router.register(r'role-assignments', RoleAssignmentViewSet)


urlpatterns = [
    path('', include(router.urls)),  # Added API versioning
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
