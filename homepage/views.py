from django.shortcuts import render, HttpResponseRedirect, reverse
from homepage.models import CustomUser, Ticket
from homepage.forms import LoginForm, CreateTicket
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get('username'), password=data.get('password'))
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('homepage'))
    form = LoginForm()
    return render(request, 'forms.html', {'form': form})

@login_required
def index(request):
    new_tickets = Ticket.objects.filter(status=Ticket.NEW)
    in_progress_tickets = Ticket.objects.filter(status=Ticket.INPROGRESS)
    done_tickets = Ticket.objects.filter(status=Ticket.DONE)
    invalid_tickets = Ticket.objects.filter(status=Ticket.INVALID)

    return render(request, 'index.html', {'new_tickets': new_tickets, 'in_progress': in_progress_tickets, 'done_tickets': done_tickets, 'invalid_tickets': invalid_tickets})

@login_required
def create_ticket_view(request):
    if request.method == 'POST':
        form = CreateTicket(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_ticket = Ticket.objects.create(
                title=data.get('title'),
                description=data.get('description'),
                created_at=datetime.now(),
                status= 'New',
                user_that_filed= request.user,
                user_assigned = None,
                completed_by= None,
            )
            if new_ticket:
                return HttpResponseRedirect(reverse('homepage'))
    form = CreateTicket()
    return render(request, 'forms.html', {'form': form})

def ticket_edit_view(request, post_id):
    ticket = Ticket.objects.get(id=post_id)
    if request.method == 'POST':
        form = CreateTicket(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            ticket.title = data['title']
            ticket.description = data['description']
            ticket.save()
        return HttpResponseRedirect(reverse('ticketdetail', args=[post_id]))

    data = {
        'title': ticket.title,
        'description': ticket.description
    }
    form = CreateTicket(initial=data)
    return render(request, 'forms.html', {'form': form})


def ticket_detail_view(request, post_id):
    ticket = Ticket.objects.get(id=post_id)
    return render(request, 'ticketdetail.html', {'ticket': ticket})


def assigned_tickets(request, post_id):
    ticket = Ticket.objects.get(id=post_id)
    ticket.status = Ticket.INPROGRESS
    ticket.user_assigned = request.user
    ticket.completed_by = None
    ticket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def completed_tickets(request, post_id):
    ticket = Ticket.objects.get(id=post_id)
    ticket.status = Ticket.DONE
    ticket.user_assigned = None
    ticket.completed_by = request.user
    ticket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def invalid_tickets(request, post_id):
    ticket = Ticket.objects.get(id=post_id)
    ticket.status = Ticket.INVALID
    ticket.user_assigned = None
    ticket.completed_by = None
    ticket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def user_page(request, username):
    user = CustomUser.objects.get(username=username)
    filed= Ticket.objects.filter(user_that_filed=user)
    assigned_to= Ticket.objects.filter(user_assigned=user)
    completed_by= Ticket.objects.filter(completed_by=user)
    return render(request, 'user.html', {'user': user, 'filed': filed, 'assigned_to': assigned_to, 'completed_by': completed_by})

    