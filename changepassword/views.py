from .utils import send_otp_email, verify_otp
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import CustomPasswordChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()

def send_otp_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        request.session["otp_email"] = email
        request.session.modified = True
        send_otp_email(email)
        return redirect("verify_otp")  # redirect instead of render
    return render(request, "blog/send_otp.html")

def verify_otp_view(request):
    if request.method == "POST":
        email = request.session.get("otp_email")
        user_otp = request.POST.get("otp")

        result = verify_otp(email, user_otp)

        if result == "success":
            return render(request, "blog/password_change.html")
        elif result == "expired":
            error = "OTP expired. Request a new one."
        elif result == "blocked":
            error = "Too many attempts. Request a new OTP."
        elif result == "invalid":
            error = "Wrong OTP. Try again."
        return render(request, "blog/verify.html", {"error": error, "email": email})
    return render(request, "blog/verify.html")

@login_required(login_url='login')
def new_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            return redirect('home')
        else:
            return render(request, 'blog/passwordreplace.html', {'form': form, 'error': form.errors})
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'blog/passwordreplace.html', {'form': form})

def change_password_after_otp(request):
    email = request.session.get('otp_email')
    print("Session email:", email)

    if not email:
        return redirect('/lg_out/login/')

    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        print("Password1:", password1)
        print("Password2:", password2)

        if password1 != password2:
            return render(request, 'blog/password_change.html', {'error': 'Passwords do not match'})

        if len(password1) < 6:
            return render(request, 'blog/password_change.html', {'error': 'Password too short'})

        try:
            print("All users:", list(User.objects.values_list('email', flat=True)))
            user = User.objects.get(email=email)
            print("User found:", user.username)
            user.set_password(password1)
            user.save()
            print("Password saved successfully")

            request.session.flush()

            messages.success(request, 'Password changed! Please login.')
            return redirect('login')  # ← HARDCODED

        except User.DoesNotExist:
            print("No user found with email:", email)
            return render(request, 'blog/password_change.html', {'error': 'User not found'})
    return render(request, 'blog/password_change.html')