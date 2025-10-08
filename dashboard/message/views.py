# ==========================================
# message/views.py (contoh)
# ==========================================
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import MessageForm

def contact_view(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('message:success')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MessageForm()
    
    return render(request, 'message/contact.html', {'form': form})

def success_view(request):
    return render(request, 'message/success.html')
