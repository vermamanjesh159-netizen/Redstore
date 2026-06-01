from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from myadmin import models as myadmin_models
from app5 import models as app5_models
from app5.database import get_db_session
from . import models
import time
import os
import stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', '')
media_url = settings.MEDIA_URL


# middleware to check session for user routes
def sessioncheckuser_middleware(get_response):
    def middleware(request):
        if request.path.startswith('/user/'):
            if request.session.get('sunm') is None or request.session.get('sroll') != "user":
                response = redirect('/login/')
            else:
                response = get_response(request)
        else:
            response = get_response(request)
        return response
    return middleware


def userhome(request):
    session = get_db_session()
    plist = session.query(myadmin_models.products).all()
    session.close()
    return render(request, "userhome.html", {"sunm": request.session["sunm"], "plist": plist, "media_url": media_url})





def funds(request):
    paypalURL = "https://www.sandbox.paypal.com/cgi-bin/webscr"
    paypalID = "sb-l47du4722346795@business.example.com"
    amt = 100
    return render(request, "funds.html", {"sunm": request.session["sunm"], "paypalURL": paypalURL, "paypalID": paypalID, "amt": amt})


def payment(request):
    uid = request.GET.get("uid")
    amt = request.GET.get("amt")
    
    session = get_db_session()
    p = models.Payment(uid=uid, amt=amt, info=time.asctime())
    session.add(p)
    session.commit()
    session.close()
    
    # Clear cart on successful mock payment
    if 'cart' in request.session:
        del request.session['cart']
        request.session.modified = True
        
    return redirect("/user/success/")


def success(request):
    amt = request.GET.get("amt", "0")
    uid = request.session.get("sunm")
    
    if amt and amt != "0" and uid:
        session = get_db_session()
        p = models.Payment(uid=uid, amt=str(amt), info=time.asctime())
        session.add(p)
        session.commit()
        session.close()
        
    # Clear cart on Stripe payment success
    if 'cart' in request.session:
        del request.session['cart']
        request.session.modified = True
        
    return render(request, "success.html", {"sunm": request.session["sunm"]})


def cancel(request):
    return render(request, "cancel.html", {"sunm": request.session["sunm"]})


def add_to_cart(request, prodid):
    cart = request.session.get('cart', {})
    cart[str(prodid)] = cart.get(str(prodid), 0) + 1
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('/user/cart/')


def remove_from_cart(request, prodid):
    cart = request.session.get('cart', {})
    if str(prodid) in cart:
        del cart[str(prodid)]
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('/user/cart/')


def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    
    session_db = get_db_session()
    
    for prodid_str, qty in cart.items():
        prodid = int(prodid_str)
        p = session_db.query(myadmin_models.products).filter(myadmin_models.products.prodid == prodid).first()
        if p:
            price = p.price
            item_total = price * qty
            total += item_total
            cart_items.append({
                'product': p,
                'price': price,
                'quantity': qty,
                'total': item_total
            })
            
    session_db.close()
    
    return render(request, "cart.html", {
        "sunm": request.session["sunm"],
        "cart_items": cart_items,
        "total": total,
        "media_url": media_url
    })


def create_checkout_session(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('/user/cart/')
        
    session_db = get_db_session()
    line_items = []
    total_amount = 0
    
    for prodid_str, qty in cart.items():
        prodid = int(prodid_str)
        p = session_db.query(myadmin_models.products).filter(myadmin_models.products.prodid == prodid).first()
        if p:
            price = p.price
            total_amount += price * qty
            
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': p.title,
                        'description': p.description[:100],
                    },
                    'unit_amount': int(price * 100), # Stripe accepts cents
                },
                'quantity': qty,
            })
            
    session_db.close()
    
    if not line_items:
        return redirect('/user/cart/')
        
    host = request.get_host()
    scheme = 'https' if request.is_secure() else 'http'
    success_url = f"{scheme}://{host}/user/success/?session_id={{CHECKOUT_SESSION_ID}}&amt={total_amount}"
    cancel_url = f"{scheme}://{host}/user/cancel/"
    
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={
                'user_email': request.session.get('sunm')
            }
        )
        return redirect(checkout_session.url, status=303)
    except Exception as e:
        print("Stripe session creation error:", e)
        # Fallback to local payment view if Stripe raises any connection/validation issue
        uid = request.session.get('sunm')
        return redirect(f"/user/payment/?uid={uid}&amt={total_amount}")


def viewfunds(request):
    session = get_db_session()
    fDetails = session.query(models.Payment).all()
    session.close()
    return render(request, "viewfunds.html", {"sunm": request.session["sunm"], "fDetails": fDetails})


def cpuser(request):
    sunm = request.session["sunm"]
    if request.method == "GET":
        return render(request, "cpuser.html", {"sunm": sunm})
    else:
        opass = request.POST.get("opass")
        npass = request.POST.get("npass")
        cnpass = request.POST.get("cnpass")

        session = get_db_session()
        userDetails = session.query(app5_models.Register).filter(
            app5_models.Register.email == sunm, 
            app5_models.Register.password == opass
        ).all()
        
        if len(userDetails) > 0:
            if npass == cnpass:
                session.query(app5_models.Register).filter(app5_models.Register.email == sunm).update({
                    app5_models.Register.password: cnpass
                })
                session.commit()
                session.close()
                return render(request, "cpuser.html", {"sunm": sunm, "output": "Password Changed Successfully.."})
            else:
                session.close()
                return render(request, "cpuser.html", {"sunm": sunm, "output": "New & Confirm New Password Mismatch"})
        else:
            session.close()
            return render(request, "cpuser.html", {"sunm": sunm, "output": "Invalid Old Password"})


def epuser(request):
    sunm = request.session["sunm"]
    session = get_db_session()
    
    if request.method == "GET":
        if request.GET.get("result") == None:
            output = ""
        else:
            output = "User Details Updated Successfully...."		
        
        userDetails = session.query(app5_models.Register).filter(app5_models.Register.email == sunm).all()
        m, f = "", ""
        if len(userDetails) > 0:
            if userDetails[0].gender == "Male" or userDetails[0].gender == "male":
                m = "checked"
            else:
                f = "checked"			
            user_data = userDetails[0]
        else:
            user_data = None
            
        session.close()
        return render(request, "epuser.html", {"sunm": sunm, "userDetails": user_data, "output": output, "m": m, "f": f})
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
        
        return redirect("/user/epuser/?result=1")