from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views import View

from customers.forms import EnquiryAssignForm, CustomerForm
from customers.models import Enquiry, Customer
from accounts.models import CustomUser


@method_decorator(login_required, name="dispatch")
class EnquiryListView(View):
    def get(self, request):
        if request.user.role != CustomUser.ADMIN:
            return redirect("core:home")

        status = request.GET.get("status")
        enquiries = Enquiry.objects.select_related("customer", "assigned_to", "customer__account_manager")

        if status:
            enquiries = enquiries.filter(status=status)

        return render(request, "customers/enquiry_list.html", {
            "enquiries": enquiries,
            "current_status": status
        })


@method_decorator(login_required, name="dispatch")
class EnquiryAssignView(View):
    def get(self, request, pk):
        if request.user.role != CustomUser.ADMIN:
            return redirect("core:home")

        enquiry = get_object_or_404(
            Enquiry.objects.select_related("customer", "customer__account_manager"),
            pk=pk
        )
        form_instance = EnquiryAssignForm(instance=enquiry)

        return render(
            request,
            "customers/enquiry_assign.html",
            {"form": form_instance, "enquiry": enquiry}
        )

    def post(self, request, pk):
        if request.user.role != CustomUser.ADMIN:
            return redirect("core:home")

        enquiry = get_object_or_404(Enquiry, pk=pk)
        form_instance = EnquiryAssignForm(request.POST, instance=enquiry)

        if form_instance.is_valid():
            enquiry = form_instance.save(commit=False)
            enquiry.status = Enquiry.ASSIGNED
            enquiry.save()
            return redirect("customers:enquiry_list")

        return render(
            request,
            "customers/enquiry_assign.html",
            {"form": form_instance, "enquiry": enquiry}
        )


@method_decorator(login_required, name="dispatch")
class EnquiryCloseView(View):
    def get(self, request, pk):
        if request.user.role != CustomUser.ADMIN:
            return redirect("core:home")

        enquiry = get_object_or_404(Enquiry, pk=pk)
        enquiry.status = Enquiry.CLOSED
        enquiry.save()

        return redirect("customers:enquiry_list")


@method_decorator(login_required, name="dispatch")
class SalesEnquiryListView(View):
    def get(self, request):
        if request.user.role != CustomUser.SALESPERSON:
            return redirect("core:home")

        enquiries = Enquiry.objects.select_related(
            "customer",
            "customer__account_manager"
        ).filter(
            assigned_to=request.user,
           # status=Enquiry.ASSIGNED
        ).order_by("-created_at")

        return render(request, "customers/sales_enquiries.html", {
            "enquiries": enquiries
        })


@method_decorator(login_required, name="dispatch")
class CustomerCreateView(View):
    def get(self, request):
        if request.user.role != CustomUser.SALESPERSON:
            return redirect("core:home")

        form_instance = CustomerForm()
        return render(request, "customers/customer_form.html", {
            "form": form_instance,
            "is_conversion": False
        })

    def post(self, request):
        if request.user.role != CustomUser.SALESPERSON:
            return redirect("core:home")

        form_instance = CustomerForm(request.POST)

        if form_instance.is_valid():
            customer = form_instance.save(commit=False)
            customer.created_by = request.user
            customer.account_manager = request.user
            customer.save()
            return redirect("customers:customer_list")

        return render(request, "customers/customer_form.html", {
            "form": form_instance,
            "is_conversion": False
        })


@method_decorator(login_required, name="dispatch")
class CustomerListView(View):
    def get(self, request):
        if request.user.role != CustomUser.SALESPERSON:
            return redirect("core:home")

        customers = Customer.objects.filter(
            account_manager=request.user
        ).order_by("name")

        return render(request, "customers/customer_list.html", {
            "customers": customers
        })


@method_decorator(login_required, name="dispatch")
class ConvertToCustomerView(View):
    def get(self, request, pk):
        if request.user.role != CustomUser.SALESPERSON:
            return redirect("core:home")

        enquiry = get_object_or_404(
            Enquiry.objects.select_related("customer", "customer__account_manager"),
            pk=pk,
            assigned_to=request.user,
            status=Enquiry.ASSIGNED
        )

        if enquiry.customer:
            initial_data = {
                "name": enquiry.customer.name,
                "phone": enquiry.customer.phone,
                "email": enquiry.customer.email,
                "company_name": enquiry.customer.company_name,
                "address": enquiry.customer.address,
                "customer_category": enquiry.customer.customer_category,
            }
        else:
            initial_data = {
                "name": enquiry.customer_name,
                "phone": enquiry.phone,
                "email": enquiry.email,
            }

        form_instance = CustomerForm(initial=initial_data)

        return render(request, "customers/customer_form.html", {
            "form": form_instance,
            "is_conversion": True,
            "enquiry": enquiry,
        })

    def post(self, request, pk):
        if request.user.role != CustomUser.SALESPERSON:
            return redirect("core:home")

        enquiry = get_object_or_404(
            Enquiry.objects.select_related("customer", "customer__account_manager"),
            pk=pk,
            assigned_to=request.user,
            status=Enquiry.ASSIGNED
        )

        form_instance = CustomerForm(request.POST)

        if form_instance.is_valid():
            linked_customer = enquiry.customer

            if linked_customer:
                linked_customer.name = form_instance.cleaned_data["name"]
                linked_customer.phone = form_instance.cleaned_data["phone"]
                linked_customer.email = form_instance.cleaned_data["email"]
                linked_customer.company_name = form_instance.cleaned_data["company_name"]
                linked_customer.address = form_instance.cleaned_data["address"]
                linked_customer.customer_category = form_instance.cleaned_data["customer_category"]
                linked_customer.save()

                enquiry.customer = linked_customer
                enquiry.status = Enquiry.CLOSED
                enquiry.save()

                messages.info(
                    request,
                    "Existing customer record was updated and linked to this enquiry."
                )
                return redirect("customers:customer_list")

            existing_customer = Customer.objects.filter(
                phone=form_instance.cleaned_data["phone"]
            ).first()

            if not existing_customer and form_instance.cleaned_data["email"]:
                existing_customer = Customer.objects.filter(
                    email=form_instance.cleaned_data["email"]
                ).first()

            if existing_customer:
                existing_customer.name = form_instance.cleaned_data["name"]
                existing_customer.phone = form_instance.cleaned_data["phone"]
                existing_customer.email = form_instance.cleaned_data["email"]
                existing_customer.company_name = form_instance.cleaned_data["company_name"]
                existing_customer.address = form_instance.cleaned_data["address"]
                existing_customer.customer_category = form_instance.cleaned_data["customer_category"]
                existing_customer.save()

                enquiry.customer = existing_customer
                enquiry.status = Enquiry.CLOSED
                enquiry.save()

                messages.info(
                    request,
                    f"Existing customer found under account manager: {existing_customer.account_manager}. "
                    "The customer record was updated and linked to this enquiry."
                )
                return redirect("customers:customer_list")

            customer = form_instance.save(commit=False)
            customer.created_by = request.user
            customer.account_manager = request.user
            customer.save()

            enquiry.customer = customer
            enquiry.status = Enquiry.CLOSED
            enquiry.save()

            messages.success(
                request,
                "Customer created successfully and linked to this enquiry."
            )
            return redirect("customers:customer_list")

        return render(request, "customers/customer_form.html", {
            "form": form_instance,
            "is_conversion": True,
            "enquiry": enquiry,
        })


@method_decorator(login_required, name="dispatch")
class CustomerUpdateView(View):
    def get(self, request, pk):
        if request.user.role != CustomUser.SALESPERSON:
            return redirect("core:home")

        customer = get_object_or_404(Customer, pk=pk, account_manager=request.user)
        form_instance = CustomerForm(instance=customer)

        return render(request, "customers/customer_form.html", {
            "form": form_instance,
            "is_conversion": False
        })

    def post(self, request, pk):
        if request.user.role != CustomUser.SALESPERSON:
            return redirect("core:home")

        customer = get_object_or_404(Customer, pk=pk, account_manager=request.user)
        form_instance = CustomerForm(request.POST, instance=customer)

        if form_instance.is_valid():
            form_instance.save()
            return redirect("customers:customer_list")

        return render(request, "customers/customer_form.html", {
            "form": form_instance,
            "is_conversion": False
        })


@method_decorator(login_required, name="dispatch")
class EnquiryDetailView(View):
    def get(self, request, pk):
        enquiry = get_object_or_404(
            Enquiry.objects.select_related("customer", "assigned_to", "customer__account_manager"),
            pk=pk
        )

        if request.user.role == CustomUser.SALESPERSON and enquiry.assigned_to != request.user:
            return redirect("core:home")

        return render(request, "customers/enquiry_detail.html", {
            "enquiry": enquiry
        })



@method_decorator(login_required, name="dispatch")
class AdminCustomerListView(View):
    def get(self, request):
        if request.user.role != CustomUser.ADMIN:
            return redirect("core:home")

        customers = Customer.objects.select_related("account_manager").order_by("name")

        return render(request, "customers/admin_customer_list.html", {
            "customers": customers
        })