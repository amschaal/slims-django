from django.shortcuts import render

from .models import Run


def runs(request):
    return render(request, "runs.html", { })

def run(request, pk):
    run = Run.objects.get(pk=pk)
    return render(request, "run.html", { "run": run})