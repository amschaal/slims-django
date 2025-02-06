from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Run
from .forms import RunForm, LaneFormSet, RunLaneHelper

@user_passes_test(lambda u: u.is_staff)
def runs(request):
    return render(request, "runs.html", { })

@user_passes_test(lambda u: u.is_staff)
def run(request, pk):
    run = Run.objects.get(pk=pk)
    return render(request, "run.html", { "run": run})

def edit_run_old(request, pk):
    run = Run.objects.get(pk=pk)
    if request.method == 'POST':
        form = RunForm(request.POST, instance=run)
        if form.is_valid():
            instance = form.save()
            return redirect('run', pk=pk)
    else:
        form = RunForm(instance=run)
    
    return render(request, "edit_run.html", { "form": form})

@user_passes_test(lambda u: u.is_staff)
def edit_run(request, pk=None):
    helper = RunLaneHelper()
    if pk:
        run = Run.objects.get(pk=pk)
        run_form = RunForm(request.POST or None, instance=run)
        lane_formset = LaneFormSet(request.POST or None, instance=run)
    else:
        run_form = RunForm(request.POST or None)
        lane_formset = LaneFormSet(request.POST or None, instance=run)

    if request.method == 'POST' and run_form.is_valid() and lane_formset.is_valid():
        instance = run_form.save()
        lane_formset.save()
        return redirect('run', pk=instance.pk)
    
    return render(request, "edit_run.html", { "run_form": run_form, "lane_formset": lane_formset, "helper": helper})

@user_passes_test(lambda u: u.is_staff)
def users(request):
    return render(request, "users.html")

@user_passes_test(lambda u: u.is_staff)
def groups(request):
    return render(request, "groups.html")

@login_required
def profile(request, pk=None):
    if pk and not request.user.is_staff:
        return HttpResponseForbidden("Only staff have permission to view other user's profiles.")
    user = User.objects.get(pk=pk) if pk else request.user
    return render(request, "profile.html", {"profile_user": user})

@login_required
def group(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden("Only staff have permission to view group details.")
    group = Group.objects.get(pk=pk)
    return render(request, "group.html", {"group": group})