from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404;
from django.http import HttpResponse, Http404;
from django.contrib.auth.models import User;
from .models import WorkJob, WorkJobUpdate, ImageUpload, Comment, WorkNotification, PledgeNotification;
from job.models import Job;
from .forms import NewWorkJobUpdate, NewComment;
from job.views import detail;

@login_required
def post_update(request, workjob_id):
    workjob = get_object_or_404(WorkJob, pk=workjob_id);
    if (request.method == 'POST'):
        form = NewWorkJobUpdate(request.POST, request.FILES);
        if (form.is_valid()):
            title = form.cleaned_data['title'];
            description = form.cleaned_data['description'];
            newUpdate = WorkJobUpdate(workjob=workjob, title=title, description=description);
            newUpdate.save();
            for image in request.FILES.getlist('images'):
                image=ImageUpload(image=image);
                image.save();
                newUpdate.imageupload_set.add(image);
            sendUpdateNotifications(newUpdate);
    else:
        if (workjob.worker == request.user):
            context = {
                'workjob' : workjob,
                'update_form' : NewWorkJobUpdate(),
            }
            return render(request, 'jobuser/post_update.html', context);
    return redirect('/job/detail/' + workjob.job.pk);
    
@login_required    
def view_update(request, update_id):
    update = get_object_or_404(WorkJobUpdate, pk=update_id);
    context = {
        'user_is_working_on_job' : WorkJob.objects.filter(job=update.workjob.job, worker=request.user).exists(), 
        'update' : update,
    }
    return render(request, 'jobuser/view_update.html', context);
    
@login_required    
def view_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    context = {
        'user_is_working_on_job' : WorkJob.objects.filter(job=comment.update.workjob.job, worker=request.user).exists(), 
        'user_is_working_on_job' : WorkJob.objects.filter(job=comment.update.workjob.job, worker=request.user).exists(), 
        'comment' : comment,
    }
    return render(request, 'jobuser/view_comment.html', context);

@login_required    
def publish_comment(request):
    if (request.method == 'POST'):
        if (request.is_ajax()):
            image = request.POST['image'];
            is_complaint = request.POST['is_complaint'];
            if (is_complaint == 'y'):
                is_complaint = True;
            else:
                is_complaint = False;
            description = request.POST['comment'];
            newComment = Comment(commenter=request.user, is_complaint=is_complaint, description=description);
            newComment.save();
            ImageUpload(comment=newComment, image=image).save();
            id = request.POST['id'];
            if (request.POST['is_update'] == "true"):
                update = get_object_or_404(WorkJobUpdate, pk=id);
                update.comment_set.add(newComment);
            else:
                comment = get_object_or_404(Comment, pk=id);
                newComment.super_comment = comment;
                newComment.save();
                comment.save();
            sendCommentNotifications(newComment);
    return HttpResponse("");
    
@login_required    
def view_updates(request, workjob_id):
    workjob = get_object_or_404(WorkJob, pk=workjob_id);
    context = {
        'workjob' : workjob,
    }
    return render(request, 'jobuser/view_updates.html', context);
    
def sendUpdateNotifications(update):
    for workjob in update.workjob.job.workjob_set.all():
        if (workjob.worker != update.workjob.worker):
            WorkNotification(worker=workjob.worker, is_update=True, update=update).save();
    for pledgejob in update.workjob.job.pledgejob_set.all(): 
        PledgeNotification(pledger=pledgejob.pledger, is_update=True, update=update).save();   
        
def sendCommentNotifications(comment):    
    for workjob in comment.job.workjob_set.all():
        if (workjob.worker != comment.commenter):
            WorkNotification(worker=workjob.worker, is_comment=True, comment=comment).save();
    for pledgejob in comment.job.pledgejob_set.all():
        if (pledgejob.pledger != comment.commenter):
            PledgeNotification(pledger=pledgejob.pledger, is_comment=True, comment=comment).save();
            
def view_pledge_notification(request, notification_id):
    pledge_notification = get_object_or_404(PledgeNotification, pk=notification_id);
    if (pledge_notification.is_money_request):
        return detail(request, pledge_notification.job_pk);
    elif (pledge_notification.is_update):
        return view_update(request, pledge_notification.update.pk);
    elif (pledge_notification.is_comment):
        return view_comment(request, pledge_notification.comment.pk);
    return Http404();
    
def view_work_notification(request, notification_id):
    work_notification = get_object_or_404(WorkNotification, pk=notification_id);
    if (work_notification.is_update):
        return view_update(request, work_notification.update.pk);
    elif (work_notification.is_comment):
        return view_comment(request, work_notification.comment.pk);
    return Http404();
















