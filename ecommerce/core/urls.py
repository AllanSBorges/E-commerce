from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name="page"),
    path("page/<int:year>/<int:month>", views.dois, name="dois"),
    path("single-product/<int:pk>", views.product_view, name="single-product"),
    path("page/", views.dois, name="dois"),
    path("now/", views.time_now, name="time"),
    path("order/", views.order_view, name="order"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("category/<int:pk>", views.category_view, name='category'),
    path("categories/", views.categories_view, name='categories'),
    path("confirmar/", views.confirmar_view, name="confirmar"),
    path("avaliar/<int:pk>", views.avaliar_view, name="confirmar"),
    path("visualizar/<int:pk>", views.visualizar_view, name='visualizar'),
    path("perfil/", views.perfil_view, name='perfil/')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)