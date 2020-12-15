from django.contrib.auth.decorators import login_required
from django.urls import path

from WebApp.parent_module import views

urlpatterns = (
    # urls for TodoTInfo
    path('', login_required(views.start), name='parent_home'),
)



