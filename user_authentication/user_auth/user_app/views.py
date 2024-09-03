from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Contact, Blogs
from django.conf import settings
# from django.core.mail import send_mail
from django.core import mail
# from django.core.mail.message import EmailMessage


def signup(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password")
        confirmpassword = request.POST.get("confirmpassword")
        # print(uname, email, password, confirmpassword)
        if password1 != confirmpassword:
            messages.warning(request, "Password mismatch")
            return redirect("/signup")

        # Check if the username is already taken
        if User.objects.filter(username=uname).exists():
            messages.warning(request, "Username already taken")
            return redirect("/signup")
        # Check if the email is already taken
        if User.objects.filter(email=email).exists():
            messages.warning(request, "Email already taken")
            return redirect("/signup")

        myuser = User.objects.create_user(uname, email, password1)  # noqa
        myuser.save()
        messages.success(request, "Signup Success please login")
        return redirect("/login")
    return render(request, "signup.html")


def handlelogin(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        password1 = request.POST.get("password")

        myuser = authenticate(username=uname, password=password1)
        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Login Success")
            return redirect("/")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("/login")
    return render(request, "login.html")


def handlelogout(request):
    logout(request)
    messages.info(request, "Logout Success")
    return redirect("/login")


def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def contact(request):
    if request.method == "POST":
        fname = request.POST.get("name")
        femail = request.POST.get("email")
        phone = request.POST.get("phone")
        desc = request.POST.get("desc")
        query = Contact(name=fname, email=femail, phone=phone, desc=desc)
        query.save()

        from_email = settings.EMAIL_HOST_USER
        connection = mail.get_connection()
        connection.open()
        email_message = mail.EmailMessage(
            f"Email from {fname}",
            f"UserEmail : {femail}\nUserPhoneNumber : {phone}\n\n\n QUERY : {desc}",  # noqa
            from_email,
            ["pushpakallesh23@gmail.com", "pushpakallesh@gmail.com"],
            connection=connection,
        )
        email_client = mail.EmailMessage(
            "Email Response",
            from_email,
            [femail],
            connection=connection,
        )
        connection.send_message([email_message, email_client])
        connection.close()
        messagesinfo(request, "Thanks For Reaching Us! We will get back you soon....") # noqa
        return redirect('/contact')
    return render(request, "contact.html")


def handleBlog(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Hey just login and Use my website")
        return redirect('/login')
    allPosts = Blogs.objects.all()
    context = {'allPosts': allPosts}
    print(allPosts)
    return render(request, 'blog.html', context)


def search(request):
    query = request.GET['search']
    if len(query) > 100:
        allPosts = Blogs.objects.none()
    else:
        allPostsTitle = Blogs.objects.filter(title__icontains=query)
        allPostsDescription = Blogs.objects.filter(description__icontains=query) # noqa
        allPosts = allPostsTitle.union(allPostsDescription)
    if allPosts.count() == 0:
        messages.warning(request, "No search results found")
    params = {'allPosts': allPosts, 'query': query}

    return render(request, 'search.html', params)
