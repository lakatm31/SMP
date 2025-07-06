from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import TransmitterForm
from .utils import calculate_max_distance
from .models import SimulationRecord 

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('simulation')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('simulation')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
@login_required
def simulation(request):
    result = None
    if request.method == "POST":
        form = TransmitterForm(request.POST)
        if form.is_valid():
            latitude = form.cleaned_data['latitude']
            longitude = form.cleaned_data['longitude']
            power_kw = form.cleaned_data['power_kw']
            frequency_mhz = form.cleaned_data['frequency_mhz']
            target_field_strength = form.cleaned_data['target_field_strength']

            
            result = calculate_max_distance(power_kw, frequency_mhz, target_field_strength)

            SimulationRecord.objects.create(
                user=request.user,
                latitude=latitude,
                longitude=longitude,
                power_kw=power_kw,
                frequency_mhz=frequency_mhz,
                target_field_strength=target_field_strength,
                result_distance=result['max_distance_m'],
                method_used=result['method']
            )
          
            decimal_lat = latitude
            decimal_lng = longitude

            return render(request, "simulation.html", {
                'form': form,
                'result': result,
                'decimal_lat': decimal_lat,
                'decimal_lng': decimal_lng,
            })
    else:
        form = TransmitterForm()

    return render(request, "simulation.html", {'form': form, 'result': result})


