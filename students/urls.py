from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    DepartmentViewSet, DegreeViewSet, CourseViewSet, DepartmentCourseViewSet,
    ClassGroupViewSet, StudentViewSet, TeacherViewSet, HODViewSet,
    CarouselImageViewSet,
    
)

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'degrees', DegreeViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'department-courses', DepartmentCourseViewSet)
router.register(r'class-groups', ClassGroupViewSet)
router.register(r'students', StudentViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'hods', HODViewSet)
router.register(r'carousel',CarouselImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)