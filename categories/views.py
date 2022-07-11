from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from utils.mixins import AdminAccessMixin

from .forms import CategoryForm
from .models import Category

# Create your views here.


class ParentCategoryListView(AdminAccessMixin, ListView):
    queryset = Category.objects.filter(parent=None)
    template_name = "category/list.html"


class CategoryCreateView(AdminAccessMixin, SuccessMessageMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "category/create.html"
    success_url = reverse_lazy("category:parent")
    success_message = "دسته یندی با موفقیت اضافه شذ"

    def form_invalid(self, form):
        messages.error(self.request, "", "danger")
        return super(CategoryCreateView, self).form_invalid(form)


class CategoryUpdateView(AdminAccessMixin, SuccessMessageMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "category/update.html"
    success_url = reverse_lazy("category:parent")
    success_message = ""

    def form_invalid(self, form):
        messages.error(self.request, "", "danger")
        return super(CategoryUpdateView, self).form_invalid(form)


class CategoryDetailView(AdminAccessMixin, SuccessMessageMixin, DetailView):
    model = Category
    template_name = ""


class CategoryDeleteVIew(AdminAccessMixin, View):
    def get(self, request, *args, **kwargs):
        category_id = kwargs.get("pk")
        category_obj = get_object_or_404(Category, id=category_id)
        category_obj.delete()
        messages.success(request, "", "success")
        return redirect("")
