from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from . import views




urlpatterns = [
    path("", views.index_view, name="page/"),
    path("page/<int:year>/<int:month>", views.dois, name="dois"), # Remover ...
    path("single-product/<int:pk>", views.product_view, name="single-product"),
    path("page/", views.dois, name="dois"), # Remover ...
    path("now/", views.time_now, name="time"), # Remover ...
    path("order/", views.order_view, name="order/"),
    path("login/", views.login_view, name="login/"),
    path("signup/", views.signup_view, name="signup/"),
    path("logout/", views.logout_view, name="logout/"),
    path("category/<int:pk>", views.category_view, name='category/'),
    path("categories/", views.categories_view, name='categories/'),
    path("conclusao/", views.conclusao_view, name="conclusao/"),
    path("avaliar/<int:pk>", views.avaliar_view, name="confirmar/"),
    path("visualizar/<int:pk>", views.visualizar_view, name='visualizar/'),
    path("perfil/", views.perfil_view, name='perfil/'),
    path("alterar_senha/", views.alterar_senha_view, name='alterar_senha/'),
    path("pedidos/", views.pedidos_view, name='pedidos/'),
    path("enderecos/", views.enderecos_view, name='enderecos/'),
    path("entrega/", views.entrega_view, name="entrega/"),
    path("forma_pagamento/", views.forma_pagamento_view, name="forma_pagamento/"),
    path("pedido/<int:pk>", views.pedido_view, name="pedido/"),
    path("recuperar/", views.recuperar_view, name="recuperar/"),
    path("nova_senha/", views.nova_senha_view, name="nova_senha/"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)