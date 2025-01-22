from django.shortcuts import render

from .models import Run


def runs(request):
    runs = Run.objects.all()[:5]
    return render(request, "runs.html", { "runs": runs})