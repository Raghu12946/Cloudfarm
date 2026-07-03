from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import UserRegistration, UserLogin
from .models import Fertilizer

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings


def register(request):
    if request.method == 'POST':
        number = request.POST['number']
        email = request.POST['email']
        name = request.POST['name']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if UserRegistration.objects.filter(number=number).exists():
            messages.error(request, "This number is already registered!")
            return redirect('register')

        if UserRegistration.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered!")
            return redirect('register')

        user = UserRegistration(number=number, email=email, name=name, password=password)
        user.save()
        messages.success(request, "Registration successful!")
        return redirect('login')
    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = UserRegistration.objects.get(email=email, password=password)
            messages.success(request, f"Welcome back, {user.name}!")
            return redirect('dashboard')  # Redirect to the dashboard or homepage
        except UserRegistration.DoesNotExist:
            messages.error(request, "Invalid login credentials!")
            return redirect('login')
    return render(request, 'login.html')


# ML INTEGRATION

from django.shortcuts import render
from .ml_utils import predict_crop_and_fertilizer

def prediction(request):
    result = {}
    if request.method == "POST":
        n = float(request.POST.get("nitrogen"))
        p = float(request.POST.get("phosphorus"))
        k = float(request.POST.get("potassium"))
        rainfall = float(request.POST.get("rainfall"))
        ph = float(request.POST.get("ph"))

        result = predict_crop_and_fertilizer(n, p, k, rainfall, ph)


        result = predict_crop_and_fertilizer(n, p, k, rainfall, ph)

    return render(request, "prediction.html", {"result": result})

def fertilizer_list(request):
    fertilizers = Fertilizer.objects.all()
    return render(request, 'fertilizer_list.html', {'fertilizers': fertilizers})

def fertilizer_detail(request, pk):
    fertilizer = get_object_or_404(Fertilizer, pk=pk)
    return render(request, 'fertilizer_detail.html', {'fertilizer': fertilizer})

from django.shortcuts import render

# Home view
def home(request):
    return render(request, 'home.html')

# Fertilizer list page view
def fertilizer_list(request):
    return render(request, 'fertilizer_list.html')

# About Us page view
def about_us(request):
    return render(request, 'Aboutus.html')

from django.shortcuts import redirect
from django.contrib.auth import logout

def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('login.html')  # Redirects to the login page

from django.shortcuts import render

def buy_products(request):
    return render(request, 'buy_products.html')


from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# View to display the cart
def view_cart(request):
    # Get the cart from the session, or set it to an empty list if not found
    cart_items = request.session.get('cart', [])
    
    return render(request, 'view_cart.html', {'cart_items': cart_items})

def add_to_cart(request, product_id):
    # Retrieve cart from session, or initialize an empty list if not found
    cart = request.session.get('cart', [])
    
    # Add product ID to the cart (ensure no duplicates)
    if product_id not in cart:
        cart.append(product_id)
    
    # Save the cart back to the session
    request.session['cart'] = cart
    request.session.modified = True  # Mark session as modified
    
    return redirect('view_cart')  # Redirect to the cart view after adding

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    request.session['cart'] = cart
    return redirect('view_cart')

from django.shortcuts import render, redirect
from django.http import HttpResponse

def add_to_cart(request):
    # Get the cart from the session or initialize an empty list if not present
    cart = request.session.get('cart', [])
    
    # Get product details from the form submission or URL parameters
    product_id = request.POST.get('product_id')
    product_name = request.POST.get('product_name')
    product_price = float(request.POST.get('product_price'))
    quantity = int(request.POST.get('quantity'))

    # Add the product to the cart
    cart.append({
        'id': product_id,
        'name': product_name,
        'price': product_price,
        'quantity': quantity,
    })

    # Save the updated cart to the session
    request.session['cart'] = cart
    request.session.modified = True  # Make sure the session is marked as modified

    # Redirect to the checkout page
    return redirect('checkout')

def checkout(request):
    # Retrieve the cart from the session
    cart = request.session.get('cart', [])
    
    # Calculate the total price
    total_price = sum(item['price'] * item['quantity'] for item in cart)

    # Pass cart items and total price to the template
    return render(request, 'checkout.html', {'cart_items': cart, 'total_price': total_price})

def clear_cart(request):
    # Clear the cart from the session after checkout
    if 'cart' in request.session:
        del request.session['cart']
    return redirect('home')

def bill(request):
    return render(request, 'bill.html')

from django.shortcuts import render, redirect
from django.contrib import messages

def payment(request):
    """
    Render the payment page.
    """
    return render(request, 'payment.html')

def thank_you(request):
    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')
        name = request.POST.get('name')
        email = request.POST.get('email')

        # Assuming payment processing logic goes here and succeeds
        payment_status = True

        if payment_status:
            # Generate a simple bill
            bill_details = f"""
            Thank you for your payment.
            --------------------------
            Name: {name}
            Card Number: **** **** **** {card_number[-4:]}
            Expiry Date: {expiry_date}
            Amount Paid: ₹100 
            --------------------------
            """

            # Send email to user
            send_mail(
                'Payment Receipt - CloudFarm',
                bill_details,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            return render(request, 'thank_you.html', {'email': email})
        # else:
        #     return render(request, 'payment_failed.html')

def help(request):
    """
    Render a simple help page.
    """
    return render(request, 'help.html', {'message': 'For payment issues, contact support@example.com'})


from django.shortcuts import render
import pandas as pd

# Path to your dataset
DATASET_PATH = r"C:\Users\nanda\OneDrive\Desktop\CloudFarm-main\CloudFarm-main\cloudfarm_app\filled_crop_fertilizer_dataset - filled_crop_fertilizer_dataset.csv.csv"

def croptable(request):
    import pandas as pd  # Ensure pandas is imported
    # Load dataset
    data = pd.read_csv(DATASET_PATH)
    data = data.drop(columns=["humidity"], errors="ignore")  # Drop 'humidity' if present

    # Ensure N, P, K, and pH values are positive
    columns_to_fix = ['N', 'P', 'K', 'ph']
    for col in columns_to_fix:
        if col in data.columns:
            data[col] = data[col].abs()  # Convert negative values to positive

    # Get the crop name from the search form
    query = request.GET.get('crop_name', '').strip().lower()

    # Filter dataset for the entered crop name
    filtered_data = data[data['label'].str.lower().str.contains(query)] if query else None

    # Prepare context: Only get the first result for simplicity
    result = None
    if filtered_data is not None and not filtered_data.empty:
        result = filtered_data.iloc[0]  # Get the first matching row..-

    context = {
        "result": result.to_dict() if result is not None else None,
        "query": query,
    }

    # Render the search page
    return render(request, "croptable.html", context)


# def thank_you(request):
#     return render(request, 'thank_you.html')