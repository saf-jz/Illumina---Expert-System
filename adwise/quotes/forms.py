from django import forms
from .models import Quote


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = [
            "customer",
            "service_type",
            "material",
            "quantity",
            "size",
            "urgency",
            "installation_required",
            "job_description",
        ]
        widgets = {
            "customer": forms.Select(attrs={"class": "form-select"}),
            "service_type": forms.Select(attrs={"class": "form-select"}),
            "material": forms.Select(attrs={"class": "form-select"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "size": forms.Select(attrs={"class": "form-select"}),
            "urgency": forms.Select(attrs={"class": "form-select"}),
            "installation_required": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "job_description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Enter details about the job, requirements, finishes, dimensions, references, or special notes..."
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        self.fields["service_type"].required = False
        self.fields["material"].required = False
        self.fields["size"].required = False

        self.fields["size"].choices = [("", "---")] + list(Quote.SIZE_CHOICES)

        if user and user.role == user.SALESPERSON:
            self.fields["customer"].queryset = self.fields["customer"].queryset.filter(
                account_manager=user
            )