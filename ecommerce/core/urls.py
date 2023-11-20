from django.urls import path
from . import views

urlpatterns = [
    path("", views.page, name="page"),
    path("index.html", views.index, name="index"),
    path("page/<int:year>/<int:month>", views.dois, name="dois"),
    path("single-product.html", views.product, name="single-product"),
    path("page", views.dois, name="dois"),
    path("now", views.time_now, name="time"),
    path("order", views.order, name="order"),
    path("login", views.login, name="login"),
]

