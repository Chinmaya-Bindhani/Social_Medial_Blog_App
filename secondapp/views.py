from django.shortcuts import render,redirect
from .forms import User,UserRegisterForm,UserUpdate,ProfileUpdate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from .models import Profile
from django.contrib.auth import get_user_model
User = get_user_model()


def log_out(request):
    logout(request)
    return render(request,'blog/logout.html')

def register(request):
    if request.method=='POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=request.POST.get('username')
            messages.success(request,f'{username} account has been created successfully')
            return redirect('home')

        else:
            username=request.POST.get('username')
            messages.warning(request,f'{username} account not created successfully')
            return redirect('register')
    else:
        form =UserRegisterForm()
        context={
            'form':form
        }
        return render(request,'blog/register.html',context)



@login_required(login_url='/lg_out/login/')
def profile(request):
    profile_obj, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':
        u_form = UserUpdate(request.POST, instance=request.user)
        p_form = ProfileUpdate(
            request.POST,
            request.FILES,
            instance=profile_obj
        )

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Account updated successfully')
            return redirect('profile')

    else:
        u_form = UserUpdate(instance=request.user)
        p_form = ProfileUpdate(instance=profile_obj)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user': request.user
    }

    return render(request, 'blog/profile.html', context)