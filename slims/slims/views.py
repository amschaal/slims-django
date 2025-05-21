from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test

from coreomics.models import Submission
from bioshare.models import SubmissionShare
from coreomics.utils import import_submission, import_submissions
from .run_type import RunTypeRegistry
from .models import LaneData, Run, RunLane, RunType
from .forms import RunForm, LaneFormSet, RunLaneHelper, LaneDataForm

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    elif request.user.is_staff:
        return redirect('runs')
    else:
        return redirect('profile')

@user_passes_test(lambda u: u.is_staff)
def runs(request):
    return render(request, "runs.html", { 'run_types':  RunType.objects.filter(enabled=True)}) #RunTypeRegistry.choices()

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
def edit_run(request, pk=None, run_type=None):
    helper = RunLaneHelper()
    run_type = RunType.objects.filter(id=run_type).first()
    run = Run(type=run_type)
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
            run.update_data_status()
            return redirect('run', pk=run.pk)

    return render(request, run.run_class.run_form_template, { "run_form": run_form, "lane_formset": lane_formset, "run": run, "helper": helper})

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
    if request.method == 'POST' and 'update' in request.POST:
        import_submissions(days=7)
    return render(request, "submissions.html")

@user_passes_test(lambda u: u.is_staff)
def submission(request, pk, update=False):
    if update:
        submission = import_submission(pk)
    else:
        submission = Submission.objects.get(pk=pk)
    # if hasattr(submission,'share'):
    #     submission.share.share_with_group_and_participants()
    return render(request, "submission.html", {"submission": submission})

# @user_passes_test(lambda u: u.is_staff)
# def share_data(request, run_id):
#     run = Run.objects.get(pk=run_id)
#     data_ids = request.POST.getlist('data')
#     # raise Exception('data', data_ids, request.POST['action'])
#     data = LaneData.objects.filter(lane__run_id=run_id, id__in=data_ids)
#     shares_created = []
#     for d in data:
#         d.status_before = d.status
#         if not hasattr(d.lane.submission, 'share'):
#             shares_created.append(d.lane.submission.create_share())
#         d.share()
#     return render(request, "share_data.html", {"data": data, "run_id": run_id, "shares_created": shares_created})

@user_passes_test(lambda u: u.is_staff)
def run_data(request, pk):
    run = Run.objects.get(pk=pk)
    action = request.POST.get('action')
    data_ids = [int(id) for id in request.POST.getlist('data')]
    filtered_data = LaneData.objects.filter(lane__run=run, id__in=data_ids)
    context = {"run": run, "action": action, "shares_created": []}
    # raise Exception(filtered_data)
    if action == 'share':
        for d in filtered_data:
                if not hasattr(d.lane.submission, 'share'):
                    context["shares_created"].append(d.lane.submission.create_share())
                d.share()
        run.update_data_status()
    # elif action == 'delete':
    #     context['deleted'] = filtered_data.exclude(status=LaneData.STATUS_COMPLETE).delete()
    context['data'] = LaneData.objects.filter(lane__run=run)
    context['lanes'] =  RunLane.objects.filter(run=run)
    return render(request, "run_data.html", context)

@user_passes_test(lambda u: u.is_staff)
def create_submission_share(request, pk):
    submission = Submission.objects.get(pk=pk)
    submission.create_share()
    return redirect('submission', pk=pk)

@user_passes_test(lambda u: u.is_staff)
def create_edit_lanedata(request, lane_id=None, pk=None):
    instance = LaneData.objects.get(pk=pk) if pk else None
    lane = instance.lane if instance else RunLane.objects.get(pk=lane_id)
    if 'regenerate' in request.GET:
        instance.regenerate()
    form = LaneDataForm(request.POST or None,lane=lane, instance=instance)
    if request.method == 'POST':
        if form.is_valid():
            lane_data = form.save()
            lane_data.lane.run.update_data_status()
            return redirect('run_data', pk=lane.run.pk)
    return render(request, 'run_forms/run_data_form.html', { "form": form, "lane": lane})

@user_passes_test(lambda u: u.is_staff)
def delete_lanedata(request, pk=None):
    instance = LaneData.objects.get(pk=pk)
    if instance.can_delete:
        run = instance.lane.run
        instance.delete()
        run.update_data_status()
    return redirect('run_data', pk=instance.lane.run.pk)

# @user_passes_test(lambda u: u.is_staff)
# def edit_run_data(request, pk):
#     lanes = RunLane.objects.filter(run_id=pk)
#     formsets = []

#     if request.method == 'POST':
#         is_valid = True
#         formsets = []

#         for lane in lanes:
#             formset = LaneDataFormSet(
#                 request.POST,
#                 queryset=LaneData.objects.filter(lane=lane).exclude(status__in=[LaneData.STATUS_COMPLETE, LaneData.STATUS_IN_PROGRESS]),
#                 prefix=f'lane_{lane.pk}'
#             )

#             if not formset.is_valid():
#                 is_valid = False

#             formsets.append((lane, formset))

#         if is_valid:
#             for lane, formset in formsets:
#                 instances = formset.save(commit=False)
#                 for instance in instances:
#                     instance.lane = lane
#                     instance.save()
#                 for obj in formset.deleted_objects:
#                     obj.delete()

#             return redirect('run_data', pk=pk)

#     else:
#         for lane in lanes:
#             formset = LaneDataFormSet(
#                 queryset=LaneData.objects.filter(lane=lane).exclude(status__in=[LaneData.STATUS_COMPLETE, LaneData.STATUS_IN_PROGRESS]),
#                 prefix=f'lane_{lane.pk}'
#             )
#             formsets.append((lane, formset))

#     return render(request, 'run_forms/run_data_formset.html', {
#         'formsets': formsets
#     })