from optparse import _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=MyUserManager.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('first_name'), max_length=30)
    last_name = models.CharField(_('last_name'), max_length=30)
    email = models.EmailField(_('email_address'), max_length=75, unique=True)
    gender = models.CharField(max_length=10, choices=(('Male', 'Male'), ('Female', 'Female')), default='Male')
    updated_at = models.DateTimeField(_('last_updated'), auto_now_add=True)
    # User Authentication Fields
    # traffic, crime, weather
    moderator = models.CharField(default='public', max_length=20)
    bearer_token = models.CharField(default='', max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    city = models.CharField(default='', max_length=60)
    phone_number = models.CharField(default='', max_length=60)
    profile_img_path = models.CharField(max_length=512, default='/static/img/default_profile_image.jpg', blank=True)
    objects = MyUserManager()
    USERNAME_FIELD = 'email'

    def get_token(self):
        return self.bearer_token

    def set_password(self, raw_password):
        self.password = raw_password

    def check_password(self, raw_password):

        if self.password == raw_password:
            return True
        else:
            return False

    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def get_name(self):
        # The user is identified by their email address
        return self.first_name + ' ' + self.last_name

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        db_table = 'users'
        ordering = ['-id']
        verbose_name = 'user'
        verbose_name_plural = 'users'
