from django.contrib import admin
from django.urls import path, include
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.contrib.auth import views as auth_views

schema_view = get_schema_view(
    openapi.Info(
        title="Book API",
        default_version='v1',
        description="A sample API for books, authors, and reviews",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@bookapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    # 앱 URL들
    path("authors/", include("authors.urls")),
    path("books/", include("books.urls")),
    path("reviews/", include("reviews.urls")),

    # API URL들
    path("api/books/", include("books.api_urls")),      # ✅ ViewSet + Router 구조 유지
    path("api/reviews/", include("reviews.api_urls")),
    path("api/authors/", include("authors.api_urls")),

    # Swagger
    path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("redoc/", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # 로그인/로그아웃/회원가입
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('signup/', views.signup, name='signup'),
]
