from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserManager(BaseUserManager):
    def create_user(self, email, phone, level, password=None):
        if not email:
            raise ValueError('User must have email address')
        
        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
            level=level,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    LEVEL_CHOICES = [
        ('Manager', 'Manager'),
        ('Project-leader', 'Project-leader'),
        ('Software-developer', 'Software-developer'),
    ]
    email = models.EmailField(verbose_name='email', max_length=50, unique=True)
    phone = models.CharField(max_length=15)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'level']

    objects = UserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    phoneno = models.CharField(max_length=15, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='profiles/', blank=True, null=True)

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

