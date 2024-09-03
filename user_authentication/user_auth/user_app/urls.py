from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path("signup", views.signup, name="signup"),
    path("login", views.handlelogin, name="handlelogin"),
    path("logout", views.handlelogout, name="handlelogout"),
    path("blog", views.handleBlog, name="handleblog"),
    path("search", views.search, name="search"),

]
