from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from accounts.forms import LoginForm
from accounts.models import CustomUser
from customers.models import Enquiry, Customer
from quotes.models import Quote


class SigninView(View):
    def get(self, request):
        form_instance = LoginForm()
        return render(request, 'accounts/login.html', {'form': form_instance})

    def post(self, request):
        form_instance = LoginForm(request.POST)

        if form_instance.is_valid():
            username = form_instance.cleaned_data['username']
            password = form_instance.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user:
                login(request, user)

                if user.role == CustomUser.ADMIN:
                    return redirect('accounts:admindashboard')
                elif user.role == CustomUser.SALESPERSON:
                    return redirect('accounts:salesdashboard')

            return render(request, 'accounts/login.html', {
                'form': form_instance,
                'error': 'Invalid username or password'
            })

        return render(request, 'accounts/login.html', {'form': form_instance})


@method_decorator(login_required, name='dispatch')
class SignoutView(View):
    def get(self, request):
        logout(request)
        return redirect('accounts:signin')


@method_decorator(login_required, name="dispatch")
class AdminDashboardView(View):
    def get(self, request):
        if request.user.role != CustomUser.ADMIN:
            return redirect("core:home")

        new_count = Enquiry.objects.filter(status=Enquiry.NEW).count()
        assigned_count = Enquiry.objects.filter(status=Enquiry.ASSIGNED).count()
        closed_count = Enquiry.objects.filter(status=Enquiry.CLOSED).count()
        customer_count = Customer.objects.count()
        submitted_quote_count = Quote.objects.filter(status=Quote.SUBMITTED).count()

        return render(request, "accounts/admindashboard.html", {
            "new_count": new_count,
            "assigned_count": assigned_count,
            "closed_count": closed_count,
            "customer_count": customer_count,
            "submitted_quote_count": submitted_quote_count,
        })


@method_decorator(login_required, name='dispatch')
class SalespersonDashboardView(View):
    def get(self, request):
        if request.user.role != CustomUser.SALESPERSON:
            return redirect('accounts:admindashboard')

        assigned_count = Enquiry.objects.filter(
            assigned_to=request.user,
            status=Enquiry.ASSIGNED
        ).count()

        customer_count = Customer.objects.filter(
            account_manager=request.user
        ).count()

        draft_quote_count = Quote.objects.filter(
            created_by=request.user,
            status=Quote.DRAFT
        ).count()

        submitted_quote_count = Quote.objects.filter(
            created_by=request.user,
            status=Quote.SUBMITTED
        ).count()

        approved_quote_count = Quote.objects.filter(
            created_by=request.user,
            status=Quote.APPROVED
        ).count()

        rejected_quote_count = Quote.objects.filter(
            created_by=request.user,
            status=Quote.REJECTED
        ).count()

        reviewed_quote_count = approved_quote_count + rejected_quote_count

        return render(request, 'accounts/salesdashboard.html', {
            'assigned_count': assigned_count,
            'customer_count': customer_count,
            'draft_quote_count': draft_quote_count,
            'submitted_quote_count': submitted_quote_count,
            'approved_quote_count': approved_quote_count,
            'rejected_quote_count': rejected_quote_count,
            'reviewed_quote_count': reviewed_quote_count,
        })