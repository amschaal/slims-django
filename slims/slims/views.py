from django.shortcuts import render, redirect

from .models import Run
from .forms import RunForm


def runs(request):
    return render(request, "runs.html", { })

def run(request, pk):
    run = Run.objects.get(pk=pk)
    return render(request, "run.html", { "run": run})

def edit_run(request, pk):
    run = Run.objects.get(pk=pk)
    if request.method == 'POST':
        form = RunForm(request.POST, instance=run)
        if form.is_valid():
            instance = form.save()
            return redirect('run', pk=pk)
    else:
        form = RunForm(instance=run)
    
    return render(request, "edit_run.html", { "form": form})