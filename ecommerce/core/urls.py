from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="page"),
    path("page/<int:year>/<int:month>", views.dois, name="dois"),
    path("single-product/<int:pk>", views.product, name="single-product"),
    path("page/", views.dois, name="dois"),
    path("now/", views.time_now, name="time"),
    path("order/", views.order, name="order"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout_view, name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)