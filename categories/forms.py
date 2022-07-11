from django import forms

from .models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("parent", "name", "paid")
        labels = {
            "name": "نام دسته بندی",
            "parent": "دسته مادر",
            "paid": "غیر رایگان",
        }

        widgets = {
            "parent": forms.Select(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields["parent"].empty_label = "انتخاب کنید"
