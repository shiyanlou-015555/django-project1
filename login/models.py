from django.db import models

# Create your models here.

class User(models.Model):
    # class Meta:
    #     model = models.User
    #     fields = ['name', 'password']
    #
    # def __init__(self, *args, **kwargs):
    #     super(UserForm, self).__init__(*args, *kwargs)
    #     self.fields['name'].label = '用户名'
    #     self.fields['password'].label = '密码'
    gender = (
        ('male',"男"),
        ('female',"女")
    )
    name = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32,choices=gender,default="男")
    c_time = models.DateTimeField(auto_now_add=True)
    has_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"


class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User',on_delete=models.DO_NOTHING)
#这里报错，因为你使用的是外检，所以你需要在应用后添加on_delete = models.CASCADE
    c_time = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.name + ":  "+self.code#设定哈希后的哈希值
    class Mata:
        #c_time是代表的是注册的提交时间
        ordering = ["-c_time"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"