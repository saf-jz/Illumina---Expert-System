from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.views import View

from customers.forms import EnquiryForm
from customers.models import Customer


class HomePageView(View):
    def get(self, request):
        form_instance = EnquiryForm()
        return render(request, "core/home.html", {"form": form_instance})

    def post(self, request):
        form_instance = EnquiryForm(request.POST)

        if form_instance.is_valid():
            enquiry = form_instance.save(commit=False)

            existing_customer = Customer.objects.filter(
                phone=enquiry.phone
            ).first()

            if not existing_customer and enquiry.email:
                existing_customer = Customer.objects.filter(
                    email=enquiry.email
                ).first()

            if existing_customer:
                enquiry.customer = existing_customer

            enquiry.save()

            messages.success(request, "Your enquiry has been sent successfully.")
            return redirect("core:home")

        return render(request, "core/home.html", {"form": form_instance})


class ServiceDetailsView(TemplateView):
    template_name = "core/services.html"