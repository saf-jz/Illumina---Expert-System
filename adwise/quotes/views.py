from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View

from accounts.models import CustomUser
from quotes.forms import QuoteForm
from quotes.models import Quote, AdminDecision
from quotes.services.recommendation_engine import generate_and_save_recommendation


@method_decorator(login_required, name="dispatch")
class QuoteCreateView(View):
    def get(self, request):
        if request.user.role != CustomUser.SALESPERSON:
            messages.error(request, "You are not authorized to access this page.")
            return redirect("accounts:role_redirect")

        form = QuoteForm(user=request.user)
        return render(request, "quotes/quote_form.html", {"form": form})

    def post(self, request):
        if request.user.role != CustomUser.SALESPERSON:
            messages.error(request, "You are not authorized to perform this action.")
            return redirect("accounts:role_redirect")

        form = QuoteForm(request.POST, user=request.user)

        if form.is_valid():
            quote = form.save(commit=False)
            quote.created_by = request.user
            quote.customer_category = quote.customer.customer_category
            quote.save()

            messages.success(request, "Quote created successfully.")
            return redirect("quotes:quote_list")

        return render(request, "quotes/quote_form.html", {"form": form})


@method_decorator(login_required, name="dispatch")
class QuoteListView(View):
    def get(self, request):
        status_filter = request.GET.get("status")

        if request.user.role == CustomUser.SALESPERSON:
            quotes = Quote.objects.filter(created_by=request.user)
        elif request.user.role == CustomUser.ADMIN:
            quotes = Quote.objects.filter(status=Quote.SUBMITTED)
        else:
            messages.error(request, "You are not authorized to access this page.")
            return redirect("accounts:role_redirect")

        if status_filter:
            quotes = quotes.filter(status=status_filter)

        return render(request, "quotes/quote_list.html", {
            "quotes": quotes,
            "selected_status": status_filter,
        })


@method_decorator(login_required, name="dispatch")
class QuoteUpdateView(View):
    def get(self, request, pk):
        if request.user.role != CustomUser.SALESPERSON:
            messages.error(request, "You are not authorized to access this page.")
            return redirect("accounts:role_redirect")

        quote = get_object_or_404(Quote, pk=pk, created_by=request.user)

        if quote.status != Quote.DRAFT:
            messages.error(request, "Only draft quotes can be edited.")
            return redirect("quotes:quote_list")

        form = QuoteForm(instance=quote, user=request.user)
        return render(request, "quotes/quote_form.html", {
            "form": form,
            "object": quote
        })

    def post(self, request, pk):
        if request.user.role != CustomUser.SALESPERSON:
            messages.error(request, "You are not authorized to perform this action.")
            return redirect("accounts:role_redirect")

        quote = get_object_or_404(Quote, pk=pk, created_by=request.user)

        if quote.status != Quote.DRAFT:
            messages.error(request, "Only draft quotes can be edited.")
            return redirect("quotes:quote_list")

        form = QuoteForm(request.POST, instance=quote, user=request.user)

        if form.is_valid():
            quote = form.save(commit=False)
            quote.customer_category = quote.customer.customer_category
            quote.save()

            messages.success(request, "Quote updated successfully.")
            return redirect("quotes:quote_list")

        return render(request, "quotes/quote_form.html", {
            "form": form,
            "object": quote
        })


@method_decorator(login_required, name="dispatch")
class QuoteSubmitView(View):
    def post(self, request, pk):
        if request.user.role != CustomUser.SALESPERSON:
            messages.error(request, "You are not authorized to perform this action.")
            return redirect("accounts:role_redirect")

        quote = get_object_or_404(Quote, pk=pk, created_by=request.user)

        if quote.status != Quote.DRAFT:
            messages.error(request, "Only draft quotes can be submitted.")
            return redirect("quotes:quote_list")

        quote.status = Quote.SUBMITTED
        quote.customer_category = quote.customer.customer_category
        quote.save()

        generate_and_save_recommendation(quote)

        messages.success(request, "Quote submitted to admin successfully.")
        return redirect("quotes:quote_detail", pk=quote.pk)


@method_decorator(login_required, name="dispatch")
class QuoteDetailView(View):
    def get(self, request, pk):
        if request.user.role == CustomUser.SALESPERSON:
            quote = get_object_or_404(Quote, pk=pk, created_by=request.user)
        elif request.user.role == CustomUser.ADMIN:
            quote = get_object_or_404(Quote, pk=pk)
        else:
            messages.error(request, "You are not authorized to access this page.")
            return redirect("accounts:role_redirect")

        recommendation = getattr(quote, "system_recommendation", None)
        admin_decision = getattr(quote, "admin_decision", None)

        return render(request, "quotes/quote_detail.html", {
            "quote": quote,
            "recommendation": recommendation,
            "admin_decision": admin_decision,
        })

    def post(self, request, pk):
        if request.user.role != CustomUser.ADMIN:
            messages.error(request, "You are not authorized to perform this action.")
            return redirect("accounts:role_redirect")

        quote = get_object_or_404(Quote, pk=pk)

        decision = request.POST.get("admin_decision")
        notes = request.POST.get("admin_notes", "").strip()

        if decision not in ["APPROVED", "REJECTED"]:
            messages.error(request, "Invalid admin decision.")
            return redirect("quotes:quote_detail", pk=quote.pk)

        admin_decision, created = AdminDecision.objects.update_or_create(
            quote=quote,
            defaults={
                "admin_decision": decision,
                "admin_notes": notes,
                "reviewed_by": request.user,
            }
        )

        if decision == "APPROVED":
            quote.status = Quote.APPROVED
        else:
            quote.status = Quote.REJECTED

        quote.save()

        messages.success(request, "Admin decision saved successfully.")
        return redirect("quotes:quote_list")

