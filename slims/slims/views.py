from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test

from coreomics.models import Submission
from .models import Run, RunLane
from .forms import RunForm, LaneFormSet, RunLaneHelper

@user_passes_test(lambda u: u.is_staff)
def runs(request):
    return render(request, "runs.html", { })

@login_required
def run(request, pk):
    run = Run.objects.get(pk=pk)
    lanes = run.ordered_lanes(user=request.user)
    if not request.user.is_staff and lanes.count() == 0:
        return HttpResponseForbidden("You do not have access to any lanes in this run.")
    return render(request, "run.html", { "run": run, "lanes": lanes})

@user_passes_test(lambda u: u.is_staff)
def delete_run(request, pk):
    run = Run.objects.get(pk=pk)
    if not run.can_delete:
        return HttpResponseForbidden("You may not delete this run.")
    RunLane.objects.filter(run=run).delete()
    run.delete()
    return render(request, "run_deleted.html", { "run": run})

@user_passes_test(lambda u: u.is_staff)
def edit_run(request, pk=None):
    helper = RunLaneHelper()
    run = Run()
    if pk:
        run = Run.objects.get(pk=pk)
        if not run.can_modify:
            lanes = run.ordered_lanes(user=request.user)
            return render(request, run.run_class.run_template, { "run": run, "lanes": lanes, "message": "This run may no longer be modified."})
    
    run_form = run.run_class.run_form(request.POST or None, instance=run)
    lane_formset = run.run_class.lane_formset(request.POST or None, instance=run)

    if request.method == 'POST':
        if run_form.is_valid() and lane_formset.is_valid():
            run = run_form.save()
            lane_formset = run.run_class.lane_formset(request.POST, instance=run)
            lane_formset.is_valid()
            lane_formset.save()
            return redirect('run', pk=run.pk)

    return render(request, "edit_run.html", { "run_form": run_form, "lane_formset": lane_formset, "run": run, "helper": helper})

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
    group = Group.objects.get(pk=pk)
    if request.user.is_staff:
        return render(request, "group_staff.html", {"group": group})
    elif group not in request.user.groups.all():
        return HttpResponseForbidden("You must be a member of the group to view this page.")
    return render(request, "group.html", {"group": group})

@user_passes_test(lambda u: u.is_staff)
def submissions(request):
    return render(request, "submissions.html")

@user_passes_test(lambda u: u.is_staff)
def submission(request, pk):
    submission = Submission.objects.get(pk=pk)
    return render(request, "submission.html", {"submission": submission})