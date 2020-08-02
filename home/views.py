from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Interface, ProductDetails, Category, Profile, Following
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
import json

# Create your views here.
def home(request):
    interface = Interface.objects.all()
    product = ProductDetails.objects.all().order_by('-date')
    category = Category.objects.all().order_by('name')
    context={
        'interface':interface,
        'product':product,
        'category':category,
    }
    return render(request, 'home/index.html',{'data':context})

def Details(request, pkId):
    interface = Interface.objects.all()
    product = ProductDetails.objects.get(pk=pkId)
    context = {
        'product':product,
        'interface':interface,
    }
    print(product)
    return render(request, 'home/product_details.html', {'data':context})

def categoryProduct(request, categoryname):
    product = ProductDetails.objects.filter(category__name__contains = categoryname)
    context = {
        'product':product,
    }
    return render(request,'home/category.html',{'data':context})

@login_required
def sell(request):
    category1 = Category.objects.all()
    if request.method == 'POST':
        user = request.user
        category_ = request.POST.get('drop1','')
        book_name = request.POST.get('bookname','')
        author = request.POST.get('author','')
        img_1 = request.FILES.get('img_1')
        img_2 = request.FILES.get('img_2')
        img_3 = request.FILES.get('img_3')
        img_4 = request.FILES.get('img_4')
        img_5 = request.FILES.get('img_5')
        price = request.POST.get('price')
        contact_no = request.POST.get('contact_no')
        address = request.POST.get('address','')
        district = request.POST.get('district','')
        state = request.POST.get('drop2','')
        details = request.POST.get('details','')
        
        cat_data = Category.objects.get(name = category_)
        print(cat_data)
        prod_obj = ProductDetails(category = cat_data, user=user, product=book_name, author=author, product_img1=img_1, product_img2=img_2, product_img3 = img_3, product_img4=img_4, product_img5=img_5, product_price=price, address=address, district=district, state=state, contact_no = contact_no, product_description = details )
        
        prod_obj.save()
        messages.success(request, 'successfully added!')
    
    context = {
        'category':category1
    }
    return render(request, 'home/adds.html',{'data':context})

def account(request, username):
    user = User.objects.filter(username = username)
    if request.method == "POST":
        prof_image = request.FILES.get('profile_image')
        prof = Profile.objects.get(user=user[0])
        prof.pro_img = prof_image
        prof.save()
    if user:
        profile = Profile.objects.get(user=user[0])
        product_ = ProductDetails.objects.filter(user=user[0])
        pro_img_ = profile.pro_img
        bio_ = profile.bio
        email_ = profile.email
        contact_no_ = profile.contact_no
        name_ = profile.name

        is_follow = Following.objects.filter(user = request.user, followed = user[0])

        following_obj = Following.objects.get(user = user[0])
        followers, following = following_obj.follower.count(), following_obj.followed.count()
        context = {
            'username':user[0],
            'pro_img':pro_img_,
            'bio' : bio_,
            'follower': followers,
            'following' : following,
            'product' : product_,
            'email' : email_,
            'contact_no' : contact_no_,
            'name': name_,
            'connection':is_follow,
        }
    return render(request, 'home/profile.html', {'data':context})

def delProfile(request):
    profile = Profile.objects.get(pk=1)
    profile.pro_img.delete(save=True)
    return redirect(account, str(request.user))

def editProfile(request, username):
    user = User.objects.filter(username = username)
    if request.method == "POST":
        name = request.POST.get('name', '')
        bio = request.POST.get('bio', '')
        contact = request.POST.get('contact', '')
        email = request.POST.get('email','')
        prof_obj = Profile.objects.get(user=request.user)
        prof_obj.name = name
        prof_obj.bio = bio
        prof_obj.email = email
        prof_obj.contact_no = contact
        prof_obj.save()
        messages.success(request, 'successfully updated!')
        return redirect(account, str(request.user))
    if user:
        profile = Profile.objects.get(user=user[0])
        bio_ = profile.bio
        email_ = profile.email
        contact_no_ = profile.contact_no
        name_ = profile.name
        context = {
            'bio' : bio_,
            'email': email_,
            'name' : name_,
            'contact_no' : contact_no_,
        }
    return render(request, 'home/account_edit.html', {'data':context})

def delAds(request, pkId):
    pro_obj = ProductDetails.objects.get(pk=pkId)
    pro_obj.delete()
    messages.success(request, "successfully deleated!")
    return redirect(account, str(request.user))

def follow(request, username):
    main_user = request.user
    to_follow = User.objects.get(username = username)
    print(to_follow)
    following = Following.objects.filter(user = main_user, followed = to_follow)
    if following:
        is_following = True
    else:
        is_following = False
    
    if is_following:
        print(to_follow)
        print(main_user)
        Following.unFollow(main_user, to_follow)
        is_following = False
    else:
        print(main_user)
        print(to_follow)
        Following.follow(main_user, to_follow)
        is_following = True

    resp = {
        "following" : is_following
    }

    response = json.dumps(resp)
    return HttpResponse(response, content_type = "application/json")
