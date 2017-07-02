from django.contrib.auth.decorators import login_required;
from django.shortcuts import render, get_object_or_404, redirect;
from django.http import HttpResponse, Http404;
from django.contrib.auth.models import User;
from .models import JobUser, Update, ImageUpload, Pay;
from user.models import Notification;
from job.models import Job;
from .forms import UpdateForm;
import stripe;
import ourjobfund.settings

@login_required
def post_update(request, jobuser_id):
    jobuser = get_object_or_404(JobUser, pk=jobuser_id);
    if (request.method == 'POST'):
        form = UpdateForm(request.POST);
        if (form.is_valid()):
            title = form.cleaned_data['title'];
            description = form.cleaned_data['description'];
            update = Update(jobuser=jobuser, title=title, description=description);
            update.save();
            for image in request.FILES.getlist('images'):
                image=ImageUpload(image=image, update=update);
                image.save();
            sendNotifications(update);
            return redirect('job:detail', job_random_string=jobuser.job.random_string);
    if (jobuser.user == request.user):
        context = {
            'jobuser' : jobuser,
            'form' : UpdateForm(),
        }
        return render(request, 'jobuser/post_update.html', context);
    return redirect('/job/' + jobuser.job.random_string);
    
@login_required    
def view_update(request, update_id):
    update = get_object_or_404(Update, pk=update_id);
    context = {
        'user_is_working_on_job' : WorkJob.objects.filter(job=update.job, worker=request.user).exists(), 
        'update' : update,
    }
    return render(request, 'jobuser/view_update.html', context);
    
def sendNotifications(update):
    users = User.objects.filter(jobuser__job=update.jobuser.job).exclude(email=update.jobuser.user.email);
    for user in users:
        if not user.notification_set.filter(job=update.jobuser.job).exists():
            notification = Notification(user=user, job=update.jobuser.job);
            notification.save();
            
@login_required            
def pay(request, jobuser_id):
    jobuser = get_object_or_404(JobUser, pk=jobuser_id);
    if (request.method == "POST" and 'stripeToken' in request.POST):
        stripe.api_key = settings.STRIPE_API_KEY;
        token = request.form['stripeToken'];
        plan = stripe.Plan.retrieve(request.POST['plan']);
        receiver_amount = plan.amount - (.05 * plan.amount);
        charge = stripe.Charge.create(
            amount = plan.amount,
            currency = "usd",
            source = token,
            destination = {
                amount : receiver_amount,
                account : jobuser.user.userprofile.stripe_account_id,
            },
        );
        charge = stripe.Charge.create(
            amount = plan.amount - receiver_amount,
            currency = "usd",
            source = token,
        );
        origJobuser = JobUser.objects.get(user=request.user, job=jobuser.job);
        payment = Pay(jobuser=origJobuser, receiver=jobuser.user, amount=plan.amount);
        origJobuser.amount_paid = origJobuser.amount_paid + plan.amount;
        return redirect('Job:detail', jobuser.job.random_string);
    context = {
        'amount' : request.GET.get('amount_paying'),
        'jobuser' : jobuser,
    }
    return render(request, 'jobuser/pay.html', context);
    
    
    
    
    
    
    
    
    
    
