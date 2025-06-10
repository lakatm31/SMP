from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import TransmitterForm
from .utils import calculate_max_distance

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
def simulation(request):
    lat = 47.497913  # Budapest alapértelmezett
    lng = 19.040236
    zoom = 10
    result = None

    if request.method == 'POST':
        form = TransmitterForm(request.POST)
        if form.is_valid():
            lat = form.cleaned_data['latitude']
            lng = form.cleaned_data['longitude']
            power_kw = form.cleaned_data['power_kw']
            frequency_mhz = form.cleaned_data['frequency_mhz']
            target_field_strength = form.cleaned_data['target_field_strength']

            #antenna_height = 30   fix érték vagy később űrlapról

            try:
                result = calculate_max_distance(
                    #lat, lng,
                    power_kw,  # kW
                    #antenna_height,
                    frequency_mhz,
                    target_field_strength
                )
            except Exception as e:
                result = f"Hiba a számítás során: {e}"
    else:
        form = TransmitterForm()

    context = {
        'form': form,
        'result': result,
        'kord': {
            'lat': lat,
            'lng': lng,
            'zoom': zoom,
        }
    }

    return render(request, 'simulation.html', context)

