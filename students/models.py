from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

# Department Model
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)  # Example: 'CSE', 'ECE'

    def __str__(self):
        return self.name

# Degree Model
class Degree(models.Model):
    name = models.CharField(max_length=100, unique=True)  # e.g., B.Tech, M.Tech, M.Sc, MBA
    duration = models.IntegerField()  # Duration in years (e.g., 4 for B.Tech)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='degrees')
    abbreviation = models.CharField(max_length=5)  # e.g., B.Tech, M.Sc, etc.

    def __str__(self):
        return self.name

# Course Model
class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    credits = models.IntegerField()
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE, related_name='courses')
    year = models.IntegerField()  # Year for which the course is assigned (1 for 1st year, etc.)

    class Meta:
        unique_together = ('name', 'degree', 'year')

    def __str__(self):
        return f"{self.name} ({self.degree.name} - Year {self.year})"

# ClassGroup Model
class ClassGroup(models.Model):
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE, related_name='class_groups')
    enrollment_year = models.IntegerField()  # Year when the group was enrolled (e.g., 2022)
    current_year = models.IntegerField(default=1)  # 1 for 1st year, 2 for 2nd year, etc.
    class_incharge = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True, related_name='incharge_classes')

    def __str__(self):
        return f"{self.degree.name} - Batch {self.enrollment_year} (Year {self.current_year})"

# DepartmentCourse Model
class DepartmentCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='department_courses')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    course_code = models.CharField(max_length=10, unique=True, editable=False)  # auto-generated

    def save(self, *args, **kwargs):
        if not self.course_code:
            department_code = self.department.code.upper()
            self.course_code = f"{department_code}{self.course.id:03d}"  # 'CSE101' if id is 1
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('course', 'department')

    def __str__(self):
        return f"{self.course_code} - {self.course.name} ({self.department.name})"

# Student Model
class Student(models.Model):
    student_id = models.CharField(max_length=15, unique=True, editable=False)  # e.g., BT202201
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    father_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    village = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    dob = models.DateField()
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE, related_name='students', default=1)
    class_group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE)
    enrollment_year = models.IntegerField()
    is_graduated = models.BooleanField(default=False)  # Graduation status

    def clean(self):
        # Custom validation to ensure dob is in the past
        if self.dob >= date.today():
            raise ValidationError("Date of birth must be in the past.")

    def save(self, *args, **kwargs):
        if not self.student_id:
            degree_code = self.degree.abbreviation.upper()
            enrollment_year = str(self.enrollment_year)

            last_student = Student.objects.filter(
                degree=self.degree,
                enrollment_year=self.enrollment_year
            ).order_by('student_id').last()

            if last_student:
                last_number = int(last_student.student_id[-3:])
                new_number = last_number + 1
            else:
                new_number = 1

            self.student_id = f"{degree_code}{enrollment_year}{new_number:03d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Teacher Model
class Teacher(models.Model):
    teacher_id = models.CharField(max_length=10, unique=True, editable=False)  # auto-generated ID
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='teachers')
    dob = models.DateField()
    joining_date = models.DateField()
    designation = models.CharField(max_length=50)
    qualification = models.CharField(max_length=50)
    village = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)

    def clean(self):
        # Custom validation to ensure dob is in the past
        if self.dob >= date.today():
            raise ValidationError("Date of birth must be in the past.")

    def save(self, *args, **kwargs):
        if not self.teacher_id:
            department_code = self.department.code.upper()
            last_teacher = Teacher.objects.filter(department=self.department).order_by('teacher_id').last()

            if last_teacher:
                last_number = int(last_teacher.teacher_id[-3:])
                new_number = last_number + 1
            else:
                new_number = 1

            self.teacher_id = f"{department_code}{new_number:03d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# HOD Model
class HOD(models.Model):
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE)  # HOD is a teacher
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='hods')

    def __str__(self):
        return f"{self.teacher.first_name} {self.teacher.last_name} ({self.department.name})"

# Function for Promotion Logic
def promote_students():
    current_year = date.today().year

    # Loop through all class groups
    for class_group in ClassGroup.objects.all():
        # Get the current year of study for the class group
        if class_group.current_year < class_group.degree.duration:
            # Promote class group to the next year
            class_group.current_year += 1
            class_group.save()

            # Promote all students in this class group
            students_in_class = Student.objects.filter(class_group=class_group)
            for student in students_in_class:
                student.class_group = ClassGroup.objects.filter(
                    degree=student.degree,
                    enrollment_year=student.enrollment_year,
                    current_year=class_group.current_year
                ).first()
                student.save()
        else:
            graduate_students(class_group)

# Function to handle graduating students (final year)
def graduate_students(class_group):
    graduating_students = Student.objects.filter(class_group=class_group)

    for student in graduating_students:
        student.is_graduated = True
        student.save()

class CarouselImage(models.Model):
    image = models.ImageField(upload_to='carousel_images/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.image.name