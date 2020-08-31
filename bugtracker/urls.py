"""bugtracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from homepage.views import login_view, index, create_ticket_view, ticket_detail_view, ticket_edit_view, completed_tickets, assigned_tickets, invalid_tickets, user_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('index/', index, name='homepage'),
    path('addticket/', create_ticket_view, name='addticket'),
    path('<str:username>/', user_page),
    path('ticket/<int:post_id>/edit', ticket_edit_view),
    path('ticket/<int:post_id>/assignedtickets/', assigned_tickets),
    path('ticket/<int:post_id>/completedtickets/', completed_tickets),
    path('ticket/<int:post_id>/invalidtickets/', invalid_tickets),
    path('ticket/<int:post_id>', ticket_detail_view, name='ticketdetail'),
    
]
