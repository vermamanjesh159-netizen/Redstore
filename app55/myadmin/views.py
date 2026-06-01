from django.shortcuts import render, redirect
from django.http import HttpResponse
from app5 import models as app5_models
from app5.database import get_db_session
from django.core.files.storage import FileSystemStorage
from . import models
from user import models as user_models
import time

# Middleware to check session for admin routes.
def sessioncheckmyadmin_middleware(get_response):
    def middleware(request):
        if request.path.startswith('/myadmin/'):
            if request.session.get('sunm') is None or request.session.get('sroll') != "admin":
                response = redirect('/login/')
            else:
                response = get_response(request)
        else:
            response = get_response(request)		
        return response	
    return middleware

def adminhome(request):
    return render(request, "adminhome.html", {"sunm": request.session["sunm"]})

def manageusers(request):
    session = get_db_session()
    uDetails = session.query(app5_models.Register).filter(app5_models.Register.roll == "user").all()
    session.close()
    return render(request, "manageusers.html", {"uDetails": uDetails, "sunm": request.session["sunm"]})    

def manageuserstatus(request):
    regid = int(request.GET.get("regid"))
    s = request.GET.get("s")
    
    session = get_db_session()
    q = session.query(app5_models.Register).filter(app5_models.Register.regid == regid)
    if s == "verify":
        q.update({app5_models.Register.status: 1})
        session.commit()
    elif s == "block":
        q.update({app5_models.Register.status: 0})
        session.commit()
    else:
        q.delete()
        session.commit()
    session.close()
    
    return redirect("/myadmin/manageusers/")

def products(request):
    if request.method == "GET":
        return render(request, "products.html", {"sunm": request.session["sunm"], "output": ""})
    else:
        title = request.POST.get("title")
        subcatname = "General"
        description = request.POST.get("description")
        ldate = request.POST.get("ldate")
        edate = request.POST.get("edate")
        price = float(request.POST.get("price", 0.0))
        quantity = int(request.POST.get("quantity", 0))

        prodimage = request.FILES.get("prodimage")
        filename = ""
        if prodimage:
            fs = FileSystemStorage()
            filename = fs.save(prodimage.name, prodimage)

        session = get_db_session()
        p = models.products(
            title=title, 
            subcatname=subcatname, 
            description=description, 
            ldate=ldate, 
            edate=edate, 
            info=time.asctime(),
            prodimage=filename,
            price=price,
            quantity=quantity
        )
        session.add(p)
        session.commit()
        session.close()
        
        return render(request, "products.html", {"sunm": request.session["sunm"], "output": "Products Added Successfully!"})


def viewuserfunds(request):
    session = get_db_session()
    fDetails = session.query(user_models.Payment).all()
    session.close()
    return render(request, "viewuserfunds.html", {"sunm": request.session["sunm"], "fDetails": fDetails})

def epadmin(request):
    sunm = request.session["sunm"]
    session = get_db_session()
    
    if request.method == "GET":
        if request.GET.get("result") == None:
            output = ""
        else:
            output = "Admin Details Updated Successfully...."		
        
        adminDetails = session.query(app5_models.Register).filter(app5_models.Register.email == sunm).all()
        m, f = "", ""
        if len(adminDetails) > 0:
            if adminDetails[0].gender == "male":
                m = "checked"
            else:
                f = "checked"			
            admin_data = adminDetails[0]
        else:
            admin_data = None
        
        session.close()
        return render(request, "epadmin.html", {"sunm": sunm, "adminDetails": admin_data, "output": output, "m": m, "f": f})
    else:
        name = request.POST.get("name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        city = request.POST.get("city")
        gender = request.POST.get("gender")
        
        session.query(app5_models.Register).filter(app5_models.Register.email == email).update({
            app5_models.Register.name: name,
            app5_models.Register.mobile: mobile,
            app5_models.Register.address: address,
            app5_models.Register.city: city,
            app5_models.Register.gender: gender
        })
        session.commit()
        session.close()
        
        return redirect("/myadmin/epadmin/?result=1")
