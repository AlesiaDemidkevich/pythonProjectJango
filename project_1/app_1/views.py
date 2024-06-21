from django.shortcuts import render, redirect
from . models import Mebel
from . forms import UpdateItemForm
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator


def show_all(request):
    form = UpdateItemForm()
    mebels = Mebel.objects.all().order_by("price")

    paginator = Paginator(mebels, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'app_1/show_all.html',
        {
            'page_obj': page_obj,
            'form': form
         }
    )

def main(request):
    return render(request, 'app_1/main.html')

def page_not_found(request, exception):
    return redirect('main')

def show_item(request, item_id):
    item = Mebel.objects.get(id=item_id)
    return render(
        request,
        'app_1/show_item.html',
        {'item': item}
    )

def show_admin_item(request):
    form = UpdateItemForm()
    mebels = Mebel.objects.all().order_by("price")
    return render(
        request,
        'app_1/show_admin_item.html',
        {
            'form': form,
            'mebels': mebels
        }
    )

def update_item(request, item_id):
    if request.method == 'POST':
        new_description = dict(request.POST).get('description', '')
        new_price = dict(request.POST).get('price', '')
        Mebel.objects.filter(id=item_id).update(price=new_price[0], description=new_description[0])
    return redirect('show_admin_item')

def delete_item(request, item_id):
    Mebel.objects.filter(id=item_id).delete()
    return redirect('show_admin_item')

def login(request):
    return render(request, 'registration/login.html')


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'