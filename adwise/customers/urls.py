"""
URL configuration for adwise project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from customers import views

app_name = "customers"

urlpatterns = [
    path("enquiries/", views.EnquiryListView.as_view(), name="enquiry_list"),
    path("enquiries/<int:pk>/assign/", views.EnquiryAssignView.as_view(), name="enquiry_assign"),
    path("enquiries/<int:pk>/close/", views.EnquiryCloseView.as_view(), name="enquiry_close"),
    path("customers/", views.CustomerListView.as_view(), name="customer_list"),
    path("customers/create/", views.CustomerCreateView.as_view(), name="customer_create"),
    path("my-enquiries/", views.SalesEnquiryListView.as_view(), name="sales_enquiries"),
    path("convert/<int:pk>/", views.ConvertToCustomerView.as_view(), name="convert_to_customer"),
    path("update/<int:pk>/", views.CustomerUpdateView.as_view(), name="customer_update"),
    path('enquiry/<int:pk>/', views.EnquiryDetailView.as_view(), name='enquiry_detail'),
    path("admin/customers/", views.AdminCustomerListView.as_view(), name="admin_customer_list"),
]
