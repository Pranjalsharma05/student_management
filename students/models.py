from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from django.core.exceptions import ValidationError
from django.utils import timezone

# Assignment Model
class Assignment(models.Model):
    title = models.CharField(max_length=255, help_text="Enter the title of the assignment.")
    description = models.TextField()
    due_date = models.DateField()
    class_group = models.ForeignKey('ClassGroup', on_delete=models.CASCADE, related_name='assignments')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Validate that due_date is in the future
        if self.due_date < timezone.now().date():
            raise ValidationError("Due date must be in the future.")

    def __str__(self):
        return self.title

# Submission Model
class Submission(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='submissions')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if Submission.objects.filter(student=self.student, assignment=self.assignment).exists():
            raise ValidationError("You have already submitted this assignment.")

    def save(self, *args, **kwargs):
        self.clean()  # Call clean to validate the submission
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.assignment.title}"



# Department Model
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
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
    name = models.CharField(max_length=100)
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE, related_name='class_groups')
    enrollment_year = models.IntegerField()  # Year when the group was enrolled (e.g., 2022)
    current_year = models.IntegerField(default=1)  # 1 for 1st year, 2 for 2nd year, etc.
    class_incharge = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True, related_name='incharge_classes')
    courses = models.ManyToManyField(Course, related_name='class_groups', blank=True)  # Relationship to courses

    def __str__(self):
        return f"{self.degree.name} - Batch {self.enrollment_year} (Year {self.current_year})"

    def get_class_details(self):
        """Returns details about the class including department, degree, in-charge, and courses."""
        return {
            'degree': self.degree.name,
            'department': self.degree.department.name,
            'class_incharge': str(self.class_incharge),
            'courses': [course.name for course in self.courses.all()],
            'enrollment_year': self.enrollment_year,
            'current_year': self.current_year,
        }

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
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

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
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)  # New gender field
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

class Teacher(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

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
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)  # New gender field

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
                # Find the next class group for the student
                next_class_group = ClassGroup.objects.filter(
                    degree=student.degree,
                    enrollment_year=student.enrollment_year,
                    current_year=class_group.current_year
                ).first()

                if next_class_group:
                    student.class_group = next_class_group
                    student.save()
                else:
                    print(f"No next class group found for {student}.")

        else:
            graduate_students(class_group)

def graduate_students(class_group):
    graduating_students = Student.objects.filter(class_group=class_group)

    for student in graduating_students:
        if not student.is_graduated:  # Check if the student is not already graduated
            student.is_graduated = True
            student.save()


class CarouselImage(models.Model):
    image = models.ImageField(upload_to='carousel_images/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.image.name
    
# Role Model
class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)  # e.g., Sports In-Charge, Club In-Charge, TPO
    description = models.TextField(null=True, blank=True)  # Optional description of the role

    class Meta:
        ordering = ['name']  # Order by name
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        
    def __str__(self):
        return self.name


class RoleAssignment(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='assignments')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='role_assignments')  # Allow one teacher to have multiple roles
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='role_assignments')  # Optional, depending on your use case

    class Meta:
        unique_together = ('role', 'teacher')  # Prevent assigning the same role to a teacher multiple times
        verbose_name = 'Role Assignment'
        verbose_name_plural = 'Role Assignments'

    def __str__(self):
        return f"{self.teacher} - {self.role}"