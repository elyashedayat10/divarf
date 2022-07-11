from braces.views import AnonymousRequiredMixin, SuperuserRequiredMixin
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, View

from .forms import AdminForm, AdminPasswordChangeForm, AuthForm

user = get_user_model()


# Create your views here.


class UserLoginView(AnonymousRequiredMixin, FormView):
    form_class = AuthForm
    template_name = "accounts/login.html"
    success_url = reverse_lazy("config:panel")

    def form_valid(self, form):
        clean_data = form.cleaned_data
        user = authenticate(
            self.request,
            phone_number=clean_data["phone_number"],
            password=clean_data["password"],
        )
        print(user)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, "با موفقیت وارد شدید", "success")
        else:
            messages.error(self.request, "خطا در ورود", "danger")
            return redirect('accounts:login')
        return super(UserLoginView, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, "", "danger")
        return super(UserLoginView, self).form_invalid(form)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "با موفقیت خارج شدید", "success")
        return redirect("accounts:login")


class AdminUserListView(SuperuserRequiredMixin, ListView):
    queryset = user.objects.filter(is_admin=True).exclude(is_superuser=True)
    template_name = "accounts/admin_list.html"
    context_object_name = "admin_list"


class AdminCreateView(SuperuserRequiredMixin, SuccessMessageMixin, FormView):
    form_class = AdminForm
    success_message = "ادمین با موققیت اضافه شد"
    success_url = reverse_lazy("accounts:admin_list")
    template_name = "accounts/admin_create.html"

    def form_valid(self, form):
        clean_data = form.cleaned_data
        user.objects.create_admin(
            phone_number=clean_data["phone_number"], password=clean_data["password"]
        )
        return super(AdminCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors, "danger")
        return super(AdminCreateView, self).form_invalid(form)


class UserDeleteView(SuperuserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        user_obj = get_object_or_404(user, id=user_id)
        user_obj.delete()
        messages.success(request, "", "success")
        return redirect("accounts:admin_list")


class AdminPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    form_class = AdminPasswordChangeForm
    template_name = ""
    success_url = reverse_lazy("")
    success_message = ""

    def form_invalid(self, form):
        messages.error(self.request, "", "danger")
        return super(AdminPasswordChangeView, self).form_invalid(form)
