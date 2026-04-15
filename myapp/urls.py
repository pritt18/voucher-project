from django.urls import path
from . import views

urlpatterns = [

    # Alpha Group
    path('alphagroup/', views.alpha_group_list, name='alphagroup'),
    path('add/', views.add_group, name='add_group'),
    path('edit/<int:id>/', views.edit_group, name='edit_group'),
    #path('inactive/<int:id>/', views.inactive_group, name='inactive_group'),

    # Voucher
    path('voucher/', views.voucher, name='voucher'),
    path('edit_voucher/<int:id>/', views.edit_voucher, name='edit_voucher'),
    path('voucher_popup/', views.voucher_popup, name='voucher_popup'),
    path('delete_voucher/<int:id>/', views.delete_voucher, name='delete_voucher'),
    path('mark_deleted/<int:id>/', views.mark_deleted, name='mark_deleted'),
    path('toggle/<int:id>/', views.toggle_group_status, name='toggle_group'),
    path('voucher_list/', views.voucher_list, name="voucher_list"),

]