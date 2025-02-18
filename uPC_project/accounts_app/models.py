from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from products_app.models import Product

# Create your models here

class UserManager(BaseUserManager):
    def create_user(self, username, password, name, email, auth, **extra_fields):
        if not username:
            raise ValueError('username Required!')
        user = self.model(
            username = username,
            name = name,
            email = email,
            auth = auth,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        
        user.email_confirmed = True
        user.save(using=self._db)

        return user
    
    def create_superuser(self, username, password, name=None, email=None, auth=None):
        user = self.create_user(username, password, name, email, auth)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin): 
    username = models.CharField(max_length=20, verbose_name="아이디", unique=True)
    password = models.CharField(max_length=128, verbose_name="비밀번호")
    name = models.CharField(max_length=8, verbose_name="이름", null=True)
    email = models.EmailField(max_length=254, verbose_name="이메일", null=True, unique=True)

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="가입일", blank=True)

    auth = models.CharField(max_length=10, verbose_name="인증번호", null=True)
    email_confirmed = models.BooleanField(default=False, verbose_name="이메일 확인 여부")

    groups = models.ManyToManyField('auth.Group', related_name='user_accounts', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='user_accounts', blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username
    
    class Meta:
        db_table = "회원목록"
        verbose_name = "사용자"
        verbose_name_plural = "사용자"



class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True, related_name='wishlist')

    def add_to_wishlist(self, product):
        self.products.add(product)
        product.increase_popularity_count()
        

    def remove_from_wishlist(self, product):
        self.products.remove(product)
        product.decrease_popularity_count()


    class Meta:
        db_table = "wishlist"
        verbose_name = "wishlist"
        verbose_name_plural = "wishlist"



class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255)
    search_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "search_history"
        verbose_name = "search_history"
        verbose_name_plural = "search_history"
    
    def __str__(self):
        return self.keyword
