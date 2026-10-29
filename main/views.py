from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect
# Create your views here.
from main.models import App, Category, Review
from django.db.models import Q, Avg, Count
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView, DetailView
from .forms import ReviewForm, AppForm, UserRegistrationForm
from django.contrib.auth import login

from django.db import transaction

from django.contrib import messages
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import reverse, reverse_lazy


@require_GET
def hw(request):
    return HttpResponse("This is my homework")


class AppListView(ListView):
    model = App
    template_name = 'main/index.html'
    paginate_by =4
    context_object_name = 'apps'

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        sort=self.request.GET.get('sort', 'new')

        if q:
            apps = App.objects.filter(Q(name__icontains=q) | Q(description__icontains=q)).order_by('name')

        else:
            apps = App.objects.order_by('-created_at')

        return apps.select_related('author')


class AboutView(TemplateView):
    template_name = 'main/about.html'



class AppDetailView(DetailView):
    model = App
    template_name = 'main/app_detail.html'
    context_object_name = 'app'
    pk_url_kwarg = 'app_id'
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.name != self.kwargs['app_name']:
            return redirect(
                'main:app_detail',
                self.object.id,
                self.object.name
            )


        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = ReviewForm()
        context['reviews'] = self.object.review_set.order_by('-created_at')
        context['app_form'] = AppForm(instance=self.object)

        context['is_favorite'] = (
                self.request.user.is_authenticated
                and self.object.favorited_by.filter(id=self.request.user.pk).exists()
        )


        return context

@login_required
def add_review(request, app_id, app_name):
    app = get_object_or_404(App, id=app_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        review=form.save(commit=False)
        review.app=app
        review.username=request.user.username
        review.save()
        return redirect('main:app_detail', app_id=app.id, app_name=app_name)
    if request.user.is_authenticated and 'username' in form.fields:
        form.fields.pop('username')

    reviews = app.review_set.order_by('-created_at')
    return render(request, 'main/app_detail.html',
    {
        'reviews': reviews,
        'app': app,
        'app_form': AppForm(instance=app),
        'form': form,
        'is_favorite': (request.user.is_authenticated and app.favorited_by.filter(pk=request.user.pk).exists() ),
        })




@require_GET
def review_detail(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    data={
        'review_id': review.id,
        'app': review.app.name,
        'username': review.username,
        'comment': review.comment,
        'stars': review.stars,
        'recommended': review.recommended,
        'created_at': review.created_at,
    }

    return JsonResponse(data)




@require_GET
def reviews(request):
    reviews=Review.objects.all().order_by('-created_at')
    return render(request, 'main/reviews.html', {'reviews': reviews})


@require_GET
def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    q = request.GET.get('q', '')

    if q:
        apps = App.objects.filter(Q(name__icontains=q) | Q(description__icontains=q), category=category)

    else:
        apps = App.objects.order_by('-created_at').filter(category=category)

    paginator = Paginator(apps, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, 'main/category_detail.html', {
        'category': category,
        'apps': apps,
        'page_obj': page_obj,
        'q': q,
    })




@require_GET
def free(request):
    apps=App.objects.free()
    return render(request, 'main/free.html' , {'apps': apps})

@require_GET
def new(request):
    apps = App.objects.new()
    paginator = Paginator(apps, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)




    return render(request, 'main/new.html', {
        'page_obj': page_obj,

    })


@require_GET
def cheap_apps(request, min_price=None, max_price=None):
    if min_price is not None:
        apps = App.objects.expensive(min_price)
    elif max_price is not None:
        apps = App.objects.cheap(max_price)

    paginator = Paginator(apps, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, 'main/cheap.html', {'page_obj': page_obj})

@login_required
def edit_app(request, app_id, app_name):
    app = get_object_or_404(App, id=app_id)
    is_favorite = app.favorited_by.filter(pk=request.user.pk).exists()
    if not (
            request.user.has_perm('main.change_app') or request.user.is_staff or app.author_id == request.user.id
    ):
        messages.error(request, 'Редактировать приложение может только её автор')
        return redirect('main:app_detail', app_id=app.id, app_name=app_name)
    if request.method == 'POST' :
        app_form = AppForm(request.POST, request.FILES, instance=app)
        if app_form.is_valid():
            app = app_form.save()
            return redirect('main:app_detail',app_id=app.id, app_name=app_name)


    else:
        app_form = AppForm(instance=app)

    return render(request,'main/app_detail.html', {'app_form': app_form, 'app': app, 'is_favorite':is_favorite})



def register(request):
    if request.user.is_authenticated:
        return redirect('main:index')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('main:index')
    else:
        form = UserRegistrationForm()
    return render(request, 'main/register.html', {'form': form})


class LoginView(LoginView):
    template_name = 'main/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, 'Вы успешно вошли!')
        return super().form_valid(form)



class LogoutView(LogoutView):
    next_page = reverse_lazy('main:index')

@login_required
def add_app(request):
    if request.method == 'POST':
        form = AppForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.author = request.user
            app.save()
            messages.success(request, f"Приложение успешно{app.name} опубликовано")
            return redirect('main:app_detail', app_id=app.id, app_name=app.name)
    else:
        form = AppForm()
    return render(request, 'main/add_app.html', {'form': form})


@login_required
def my_apps(request):
    apps = App.objects.filter( author=request.user).order_by('-created_at')
    return render(request, 'main/my_apps.html', {'apps': apps})



class StorePasswordResetView(PasswordResetView):
    template_name = 'main/password_reset.html'
    email_template_name = 'main/store_password_reset_email.html'
    subject_template_name = 'main/store_password_reset_subject.txt'
    success_url = reverse_lazy('main:password_reset_done')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['email'].label='Email'
        return form

class StorePasswordResetDoneView(PasswordResetDoneView):
    template_name='main/store_password_reset_done.html'

class StorePasswordResetConfirmView(PasswordResetConfirmView):
    template_name='main/password_reset_confirm.html'
    success_url=reverse_lazy('main:password_reset_complete')

    def get_form(self, form_class=None):
        form=super().get_form(form_class)
        if form is not None and 'new_password1' in form.fields:
            form.fields['new_password1'].label='Новый пароль'
            form.fields['new_password2'].label='Повтор'
        return form

class StorePasswordResetCompleteView(PasswordResetCompleteView):
    template_name='main/password_reset_complete.html'


@require_POST
def toggle_favorite_app(request, app_id, app_name):
    app = get_object_or_404(App, id=app_id)

    if not request.user.is_authenticated:
        login_url=reverse('main:login')
        next_url=reverse('main:app_detail', args=[app.id, app_name] )
        return redirect(f"{login_url}?next={next_url}")

    if app.favorited_by.filter(id=request.user.id).exists():
        app.favorited_by.remove(request.user)
        messages.success(request, f'Приложение {app.name} удалено из списка избранные')

    else:
        app.favorited_by.add(request.user)
        messages.success(request, f'Приложение {app.name} добавлено в список избранные')


    return redirect('main:app_detail', app_id=app.id, app_name=app.name)


@login_required
def favorites(request):
    apps = (
        request.user.favorite_apps.select_related('author',  'category').order_by('-created_at')
    )

    return render(request, 'main/favorites.html', {'apps': apps})


@login_required
def discount(request):
    if not request.user.is_staff:
        messages.error(request, 'Распродажу может запустить только персонал')
        return redirect('main:index')


    if request.method == 'POST':
        category_id = int(request.POST.get('category'))
        category = Category.objects.get(pk=category_id)

        updated = App.discount_incategory(category_id,10)

        messages.success(request, f"Скидка 10% применена к платным приложениям в категории' {category.name}': {updated}")
        return redirect('main:index')


    return render(request, 'main/discount.html', {'categories': Category.objects.all(),})


@login_required
def close_category(request, category_id):
    if not request.user.is_staff:
        messages.error(request, 'Категории может закрывать только персонал ')
        return redirect('main:index')
    source = get_object_or_404(Category, pk=category_id)
    targets = Category.objects.exclude(pk=category_id)
    if request.method == 'POST':
        target_id = request.POST.get('target_id')

        if not target_id or not target_id.isdigit():
            messages.error(request, 'Нужно выбрать категорию')
            return redirect('main:close_category', category_id=source.pk)
        try:
            target = get_object_or_404(Category, pk=target_id)
            App.objects.move_to_category(source, target)
        except ValueError as exc:
            messages.error(request, str(exc))
            return redirect('main:close_category', category_id=source.pk)
        return redirect('main:category', category_id=target.pk)
    return render(request, 'main/close_category.html', {
        'source': source,
        'targets': targets
    })