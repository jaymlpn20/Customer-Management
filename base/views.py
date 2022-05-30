from django.shortcuts import render, redirect
from .models import *
from .forms import OrderForm
from django.forms import inlineformset_factory
from.filters import OrderFilter

# Create your views here.
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()


    context = {
        'orders': orders, 'customers': customers, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending,
        'total_customers':total_customers
    }
    return render(request, 'base/dashboard.html', context)

def products(request):
    products = Product.objects.all()
    return render(request, 'base/products.html', {'products': products})

def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter()

    context = {'customer':customer, 'orders':orders, 'order_count':order_count, 'myFilter':myFilter}
    return render(request, 'base/customer.html', context)


def createOrder(request, pk):
    orderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = orderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer})
    context = {'formset':formset}
    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset = orderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    return render(request, 'base/order_form.html', context)

def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    context = {'form': form}
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, 'base/order_form.html', context)

def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'base/delete.html', context)
