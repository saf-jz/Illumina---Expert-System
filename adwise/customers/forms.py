from django import forms
from customers.models import Enquiry, Customer
from accounts.models import CustomUser


class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ["customer_name", "email", "phone", "message"]



class EnquiryAssignForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ["assigned_to"]
        widgets = {
            "assigned_to": forms.Select(attrs={"class": "form-select bg-dark text-white border-0"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["assigned_to"].queryset = CustomUser.objects.filter(
            role=CustomUser.SALESPERSON
        )

        self.fields["assigned_to"].empty_label = "Select Salesperson"



class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            "name",
            "phone",
            "email",
            "company_name",
            "address",
            "customer_category"
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter customer name"
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter phone number"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Enter email address"
            }),
            "company_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter company name"
            }),
            "address": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter company address",
                "rows": 3
            }),
            "customer_category": forms.Select(attrs={
                "class": "form-select"
            }),
        }