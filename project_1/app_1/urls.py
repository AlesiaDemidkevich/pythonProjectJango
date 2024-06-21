from django.urls import path
from .import views


urlpatterns = [
    path('', views.main, name='main'),
    path('items', views.show_all, name='show_all'),
    path('items/<int:item_id>', views.show_item, name='show_item'),
    path('admin_items', views.show_admin_item, name='show_admin_item'),
    path('update_item/<int:item_id>', views.update_item, name='update_item'),
    path('delete_item/<int:item_id>', views.delete_item, name='delete_item'),
    path('login', views.login, name='login'),
    path('register', views.SignUp.as_view(), name='register'),
]