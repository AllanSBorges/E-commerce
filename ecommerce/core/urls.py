from django.urls import path
from . import views

urlpatterns = [
    path("", views.page, name="page"),
    path("index/", views.index, name="index"),
    path("page/<int:year>/<int:month>", views.dois, name="dois"),
    path("single-product/", views.product, name="single-product"),
    path("page/", views.dois, name="dois"),
    path("now/", views.time_now, name="time"),
    path("order/", views.order, name="order"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout_view, name="logout"),
]

