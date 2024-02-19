from django.db import models

from django.conf import settings
from django.contrib.auth import user_logged_in
from django.contrib.auth.models import AbstractUser, UserManager as AuthUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.

class UserManager(AuthUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('지정된 사용자 이름을 설정해야 합니다')
        email = self.normalize_email(email)
        username = self.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        Profile.objects.create(user=user)
        return user


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=20,
        unique=True,
        help_text=_('*필수* 20자 이내의 문자, 숫자, 특수문자(@,.,+,-,_) 조합'),
        validators = [username_validator],
        error_messages={'unique':_("이미 가입된 username입니다"),},
    )
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={'unique':_("이미 가입된 email입니다"),},
    )
    object = UserManager()

    groups = models.ManyToManyField(Group, related_name='user_groups', through='UserGroup')
    user_permissions = models.ManyToManyField(Permission, related_name='user_permissions', through='UserPermission')

    class Meta:
        verbose_name = "사용자"
        verbose_name_plural = "사용자"

class UserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

class UserPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name="사용자", on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name="생성일", auto_now_add=True)
    update_at = models.DateTimeField(verbose_name="최근 업데이트", auto_now=True)

    def __str__(self):
        return self.user.username
    
    class Meta :
        verbose_name = "프로필"
        verbose_name_plural = "프로필"


class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)
    session_key = models.CharField(verbose_name="세션키", max_length=40, editable=False)
    created_at = models.DateTimeField(verbose_name="생성일", auto_now_add=True)

    class Meta:
        verbose_name = "유저 세션"
        verbose_name_plural = "유저 세션"


def kicked_my_other_sessions(sender, request, user, **kwargs):
    user.is_user_legged_in = True

user_logged_in.connect(kicked_my_other_sessions)