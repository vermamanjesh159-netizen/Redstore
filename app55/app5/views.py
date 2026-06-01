from django.shortcuts import render, redirect
from . import models
from .database import get_db_session
import time
from . import emailAPI

# middleware to check session for mainapp routes
def sessioncheck_middleware(get_response):
    def middleware(request):
        if request.path == '/home/' or request.path == '/about/' or request.path == '/contact/' or request.path == '/login/' or request.path == '/register/':
            request.session['sunm'] = None
            request.session['sroll'] = None
            response = get_response(request)
        else:
            response = get_response(request)        
        return response    
    return middleware

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')    

def register(request):
    if request.method == "GET":
        return render(request, 'register.html', {"output": ""})
    else:
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        city = request.POST.get("city")
        gender = request.POST.get("gender")
        
        session = get_db_session()
        
        # Check if email already exists
        existing_user = session.query(models.Register).filter(models.Register.email == email).first()
        if existing_user:
            session.close()
            return render(request, 'register.html', {"error": "Email already exists."})

        p = models.Register(
            name=name, email=email, password=password, mobile=mobile,
            address=address, city=city, gender=gender, status=1, roll="user", info=time.asctime()
        )
        session.add(p)
        session.commit()
        session.close()

        # emailAPI.sendMail(email, password)

        return render(request, 'register.html', {"output": "User Register Successfully"})   

def login(request):
    cunm, cpass = "", ""
    if request.COOKIES.get("cunm") is not None:
        cunm = request.COOKIES.get("cunm")
        cpass = request.COOKIES.get("cpass")

    if request.method == "GET":
        return render(request, 'login.html', {"cunm": cunm, "cpass": cpass, "output": ""})
    else:
        email = request.POST.get("email")
        password = request.POST.get("password")      
        
        session = get_db_session()
        userDetails = session.query(models.Register).filter(
            models.Register.email == email,
            models.Register.password == password
        ).all()
        session.close()

        if len(userDetails) > 0:
            user = userDetails[0]
            if user.roll == "admin" or user.status == 1:
                request.session["sunm"] = user.email
                request.session["sroll"] = user.roll

                if user.roll == "admin":
                    response = redirect("/myadmin/")
                else:
                    response = redirect("/user/")
                
                if request.POST.get("chk") is not None:
                    response.set_cookie("cunm", user.email, max_age=3600*24*365)
                    response.set_cookie("cpass", user.password, max_age=3600*24*365)
                return response     
            else:  
                return render(request, 'login.html', {"cunm": cunm, "cpass": cpass, "output": "Your account is not active or verified."})
        else:  
            return render(request, 'login.html', {"cunm": cunm, "cpass": cpass, "output": "Invalid user or password."})

def verify(request):
    vemail = request.GET.get("vemail")
    session = get_db_session()
    session.query(models.Register).filter(models.Register.email == vemail).update({models.Register.status: 1})
    session.commit()
    session.close()
    return redirect("/login/")

def test1(request):
    if request.method == "GET":
        return render(request, 'test1.html', {"output": ""})
    else:
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        
        session = get_db_session()
        p = models.test1(name=name, email=email, password=password, mobile=mobile, address=address, gender=gender)
        session.add(p)
        session.commit()
        session.close()  
        return render(request, 'test1.html', {"output": "User Register Successfully"})