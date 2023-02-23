from django.shortcuts import render
from django.http import HttpResponse

from django.conf import settings
from .models import Cause

#PAYPAL Imports
from django.views.decorators.csrf import csrf_exempt
from .forms import CartForm, CheckoutForm
from paypal.standard.forms import PayPalPaymentsForm
from django.shortcuts import get_object_or_404, reverse
from . import cart
#----

# Create your views here.

#function extends from index.html, which contains navbar, but renders home. donate.html and starp.html templates extend index.html
def index(request):
    return render(request, "bpFund/home.html")

def donate(request):
    causes = Cause.objects.all()
    return render(request, "bpFund/donate.html", {
        'causes': causes,
    })

def starp(request):
    return render(request, "bpFund/starp.html")

def createProject(request):
    if request.method == "POST":
        print("In createProject() POST method.")
        name = request.POST["name"]
        email = request.POST["emailForm"]
        orgSchool = request.POST["org"]
        problem = request.POST["prob"]
        sol = request.POST["sol"]
        location = request.POST["location"]
        date = request.POST["date"]
        targetAmount = request.POST["targetAmount"]

        causeModel = Cause(
            name=name,
            email=email,
            orgSchool=orgSchool,
            problem=problem,
            sol=sol,
            location=location,
            date=date,
            targetAmount=targetAmount
        )

        causeModel.save()

        causes = Cause.objects.all()

        #products = Products.objects.all()
        #userstamp = request.user
        #user_rec = User.objects.get(username=userstamp)
        #Tutor.objects.all().filter(active='Y').order_by('subject')
        print("CAUSE MODEL: ", causes)

        return render(request, 'bpFund/donate.html', {
            causes: causes,
        })
    return HttpResponse("None")



#PAYPAL Integration


def product_detail(request, product_id, product_slug):
    product = Product.objects.get(id=product_id)

    if request.method == "POST":
        form = CartForm(request, request.POST)
        if form.is_valid():
            request.form_data = form.cleaned_data
            cart.add_item_to_cart(request)
            return redirect("show_cart")
        else:
            print("Error: Bad Form")

    form = CartForm(request, initial={"product_id": product_id})
    return render(request, "bpFund/product_detail.html", {
        "product": product,
        "form": form,
    })

def show_cart(request):
    if request.method == "POST":
        if request.POST.get('submit') == 'Update':
            cart.update_item(request)

        if request.POST.get('submit') == 'Remove':
            cart.remove_item(request)

    cart_items = cart.get_all_cart_items(request)
    print(cart_items)
    cart_subtotal = cart.subtotal(request)
    return render(request, "bpFund/cart.html", {
        "cart_items": cart_items,
        "cart_subtotal": cart_subtotal
    })

def checkout(request):
    print('checkout')
    if request.method == 'POST':
        print('step1')
        form = CheckoutForm(request.POST)
        print('step2')
        if form.is_valid():
            print('step3')
            cleaned_data = form.cleaned_data
            print('step4')
            o = Order(
                name = cleaned_data.get('name'),
                email = cleaned_data.get('email'),
                postal_code = cleaned_data.get('postal_code'),
                address = cleaned_data.get('address'),
            )
            o.save()
            print('step5')

            all_items = cart.get_all_cart_items(request)
            print('step6')
            for cart_item in all_items:
                li = LineItem(
                    product_id = cart_item.product_id,
                    price = cart_item.price,
                    quantity = cart_item.quantity,
                    order_id = o.id
                )

                li.save()

            print('step7')
            cart.clear(request)
            print('step8')
            print('o.id=',o.id)
            request.session['order_id'] = o.id
            print('step9')
            return redirect('process_payment')

            messages.add_message(request, messages.INFO, 'Order Placed!')
            return redirect('checkout')
    else:
        print('step2')
        form = CheckoutForm()
        print('form=', form)
        return render(request, "bpFund/checkout.html", {
            "form": form
        })

def process_payment(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % order.total_cost(),
        'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment_cancelled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, "bpFund/process_payment.html", {
        "order": order,
        "form": form
    })

@csrf_exempt
def payment_done(request):
    order_id = request.session.get('order_id')
    order_rec = Order.objects.get(id=order_id)
    order_rec.paid = True
    order_rec.save()
    return render(request, "bpFund/payment_done.html")


@csrf_exempt
def payment_cancelled(request):
    order_id = request.session.get('order_id')
    order_rec = Order.objects.filter(id=order_id)
    order_rec.delete()
    return render(request, "bpFund/payment_cancelled.html")
