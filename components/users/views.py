from django.contrib.postgres.search import SearchVector
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View

from .forms import (
    SignInForm, SignUpForm,
    ChangeRoleAccountForm,
    AccountUpdateForm
)
from .models import User
from .decorators import admin_required


class SignUpView(View):
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': UserCreationForm})

    def post(self, request, *args, **kwargs):
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            login(request, user)

            return redirect(reverse('book:book-list'))


class SignInView(View):
    template_name = 'signin.html'
    form_class = SignInForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        signin_form = self.form_class(request.POST)
        if signin_form.is_valid():
            user = authenticate(username=signin_form.cleaned_data['email'],
                                password=signin_form.cleaned_data['password'])
            login(request, user)
            return redirect(reverse('book:book-list'))
        return render(request, self.template_name, {'form': self.form_class})


class SignOutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('users:signin'))


class ChangeRoleAccountView(View):
    template_name = 'change_user_role.html'
    form_class = ChangeRoleAccountForm

    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        change_role_account_form = ChangeRoleAccountForm(request.POST)
        if change_role_account_form.is_valid():
            user = User.objects.filter(username=change_role_account_form.cleaned_data['username']).first()
            if user:
                user.role = change_role_account_form.cleaned_data['role']
                return redirect(reverse('users:account-list'))
            return render(request, '404.html', {'message': f'User {user.username} not found'})


class AccountListView(View):
    template_name = 'users_list.html'

    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        users = User.objects.filter(is_activate=True)
        return render(request, self.template_name, {'users': users})


class AccountUpdateView(View):
    template_name = 'account_update.html'
    form_class = AccountUpdateForm

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        account = self.__get_user_id(request, **kwargs)
        if not account:
            return HttpResponseForbidden('403 Forbidden')

        init_data = {
            'email': account.user.email,
            'avatar': account.avatar
        }
        account_update_form = self.form_class(initial=init_data)
        return render(request, self.template_name, {'form': account_update_form, 'id': account.id})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        account_update_form = AccountUpdateForm(request.POST)
        if account_update_form.is_valid():
            email = account_update_form.cleaned_data['email']
            avatar = account_update_form.cleaned_data['avatar']

            account = self.__get_user_id(request, **kwargs)
            account.user.email = email
            account.user.save()

            account.avatar = avatar
            account.save()

            return redirect(reverse('users:account-detail', kwargs={'id': account.id}))

    def __get_user_id(self, request, **kwargs):
        account = get_object_or_404(Account, pk=kwargs.get('id'))
        if (account.role == '1' and request.user.id == account.user.id) or account.role == '0':
            return account


class AccountDetailView(View):
    template_name = 'account_detail.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        account_id = kwargs.get('id')
        account = get_object_or_404(Account, pk=account_id)
        if account.user.id != request.user.id:
            return HttpResponseForbidden('403 Forbidden')
        return render(request, self.template_name, {'account': account})


class AccountDeleteView(View):

    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        account = get_object_or_404(kwargs.get('id'))
        account.user.is_active = False
        account.user.save()

        return redirect(reverse('users:account-list'))


class AccountSearchView(View):
    template_name = 'account_list.html'

    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        search_text = request.GET.get('q')
        accounts_qs = Account.objects.annotate(
            search=SearchVector(
                'user__username', 'user__email'
            )
        ).filter(search=search_text).distinct('user__username')

        return render(request, self.template_name, {'accounts': accounts_qs})
