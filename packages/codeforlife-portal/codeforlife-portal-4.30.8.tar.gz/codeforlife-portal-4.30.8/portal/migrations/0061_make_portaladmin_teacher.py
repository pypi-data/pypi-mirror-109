# Generated by Django 2.0 on 2020-10-28 17:36

import os

from django.contrib.auth.hashers import make_password
from django.db import migrations


def give_portaladmin_teacher_profile(apps, schema_editor):
    """
    This migration is so that we can still log in using the portaladmin User, but from
    the teacher login form, which requires school data to be linked to the User.
    """
    User = apps.get_model("auth", "User")
    UserProfile = apps.get_model("common", "UserProfile")
    School = apps.get_model("common", "School")
    Teacher = apps.get_model("common", "Teacher")
    Class = apps.get_model("common", "Class")
    Student = apps.get_model("common", "Student")

    # Amend portaladmin details
    portaladmin = User.objects.get(username="portaladmin")
    portaladmin.first_name = "Portal"
    portaladmin.last_name = "Admin"
    portaladmin.email = "codeforlife-portal@ocado.com"
    portaladmin.save()

    # Create portaladmin UserProfile
    portaladmin_userprofile = UserProfile.objects.create(user=portaladmin)

    # Find test school
    portaladmin_school, _ = School.objects.get_or_create(
        name="Swiss Federal Polytechnic"
    )

    # Create Teacher object and link it to School
    portaladmin_teacher = Teacher.objects.create(
        title="Mr",
        user=portaladmin_userprofile,
        new_user=portaladmin,
        school=portaladmin_school,
        is_admin=True,
        pending_join_request=None,
    )

    # Create a Class
    portaladmin_class = Class.objects.create(
        name="Portaladmin's class",
        teacher=portaladmin_teacher,
        access_code="PO123",
        classmates_data_viewable=True,
        always_accept_requests=True,
    )

    # Create the student User
    portaladmin_student_user = User.objects.create(
        username="portaladmin student",
        first_name="Portaladmin",
        last_name="Student",
        email="adminstudent@codeforlife.com",
        password=make_password(os.getenv("ADMIN_PASSWORD", "Password1")),
    )

    # Create the student UserProfile
    portaladmin_student_userprofile = UserProfile.objects.create(
        user=portaladmin_student_user
    )

    # Create the Student
    portaladmin_student = Student.objects.create(
        class_field=portaladmin_class,
        user=portaladmin_student_userprofile,
        new_user=portaladmin_student_user,
        pending_class_request=None,
    )


def revert_portaladmin_data(apps, schema_editor):
    User = apps.get_model("auth", "User")
    UserProfile = apps.get_model("common", "UserProfile")
    Teacher = apps.get_model("common", "Teacher")
    Class = apps.get_model("common", "Class")
    Student = apps.get_model("common", "Student")

    portaladmin, created = User.objects.get_or_create(username="portaladmin")

    if not created:
        portaladmin_userprofile = UserProfile.objects.get(user=portaladmin)
        portaladmin_teacher = Teacher.objects.get(new_user=portaladmin)
        portaladmin_class = Class.objects.get(teacher=portaladmin_teacher)
        portaladmin_student_user = User.objects.get(username="portaladmin student")
        portaladmin_student_userprofile = UserProfile.objects.get(
            user=portaladmin_student_user
        )
        portaladmin_student = Student.objects.get(user=portaladmin_student_userprofile)

        portaladmin_student.delete()
        portaladmin_student_userprofile.delete()
        portaladmin_student_user.delete()
        portaladmin_class.delete()
        portaladmin_teacher.delete()
        portaladmin_userprofile.delete()

    portaladmin.first_name = ""
    portaladmin.last_name = ""
    portaladmin.email = "('codeforlife-portal@ocado.com',)"
    portaladmin.save()


class Migration(migrations.Migration):

    dependencies = [("portal", "0060_delete_guardian")]

    operations = [
        migrations.RunPython(give_portaladmin_teacher_profile, revert_portaladmin_data)
    ]
