from django.shortcuts import render
from django.shortcuts import redirect
from . import models
#导入本地的，不是使用默认的from django import forms
from . import forms
from django.conf import settings
import hashlib
import datetime
from mysite import settings
# Create your views here.
def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'login/confirm.html', locals())


def send_email(email, code):

    from django.core.mail import EmailMultiAlternatives

    subject = '来自艾春辉的注册确认邮件'

    text_content = '''感谢注册'''

    html_content = '''
                    <p>感谢注册<a href="http://{}/confirm/?code={}" target='_blank';>www.aichunhui.cn</a></p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user,)
    return code
def hash_code(s, salt = 'mysite'):
    #使用sha256
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())#update方法只接受bytes流类型
    return h.hexdigest()


def index(request):
    return render(request, 'login/index.html')




def login(request):
    if request.session.get('is_login',None):
        return redirect('/index/')
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = "请检查填写的内容"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            #用户名字符合法性验证
            #密码长度验证
            try :
                user = models.User.objects.get(name=username)
                # 1.
                # 导入models模块
                # 2.
                # models.User.objects.get(name=username)
                # 是Django提供的最常用的数据查询API, 因为我们之前设计好了数据库的表
                if not user.has_confirmed:#进行邮件确认
                    message = "用户还未通过邮件确认"
                    return render(request, 'login/login.html',locals())
                # if user.password == password:将密码与数据库里面值进行比对，而不是提取出来，浪费时间
                # 好像数据库里面的东西拿出来会自动反转
                print(user.password)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')

                else:
                    message = "密码不正确"
            except:
                message = "用户名不存在"
        #  return render(request, 'login/login.html', {"message": message})
        return render(request,'login/login.html',locals())#local更为强大，所有的有关内容，均传递
    login_form = forms.UserForm
    return render(request, 'login/login.html',locals())


def register(request):
    if request.session.get('is_login',None):
        #思考一下，登录状态下注册，肯定不可行
       return  redirect('index/')
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容"
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:
                message = "两次输入的密码不同"
                return  render(request,'login/register.html',locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户已经存在，请重新选择用户名'
                    return render(request,'login/register.html',locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱地址已经被注册，请使用别的邮箱'
                    return render(request,'login/register.html',locals())
                #当然在上述都没错误的话，我们开始使用我们的东西了
                new_user = models.User()#对于数据库里面表进行实例化，方便使用
                new_user.name = username
                new_user.password =hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()#进行保存


                code = make_confirm_string(new_user)
                send_email(email,code)
                return redirect(request,'login/confirm.html',locals())#跳转到等待邮件确认页面
    register_form = forms.RegisterForm()
    return render(request,'login/register.html',locals())


def logout(request):
    if not request.session.get('is_login',None):
        #如果本来就没有登录，也就没有等出一说
        return redirect("/index/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/index/")