
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.db.models import Count, Q
from django.http import (HttpResponseRedirect,
                         HttpResponse, HttpResponseForbidden)
from django.shortcuts import render_to_response, get_object_or_404, render
from django.forms.formsets import formset_factory
from django.db.models import ProtectedError
from django.db import connection

from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
import smtplib
from datetime import datetime as dt
import time
import os.path
from datetime import date, timedelta, datetime
import json
from django.views.decorators.csrf import csrf_exempt
from .tasks import aysc_func
from celery.result import AsyncResult

# TO run celery
# Run vnev , for this project jp3
# Go to the project directory
# celery -A ct worker -l info

# Redis
# Check Redis-Server Status:
# sudo service redis-server status


def get_celery(request):
    async_result = aysc_func.delay()
    print(async_result)
    message = "Your Download will be completed in a moment. Please Wait..."
    task_id = async_result
    print('###########')
    print(task_id)
    task = AsyncResult(str(task_id))
    data = task.result or task.state
    return render(request, "celery_test.html", {
        'message': message,
        'data': data,
        'task_id': task
    })


@csrf_exempt
def check_status(request):
    filename = "Expenses01.xlsx"
    if request.is_ajax():
        task_id = request.POST.get('celery_id')
        data = AsyncResult(str(task_id))
        status = data.result or data.state
        context = {}
        if str(status) == '1':
            context['status'] = "SUCCESS"
            context['file'] = "Expenses01.xlsx"
        else:
            context['status'] = "PENDING"
            context['file'] = "None"
        return HttpResponse(json.dumps(context))

    f = open(filename, 'r')
    response = HttpResponse(f, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Expenses01.xlsx'
    return response


# def task_state(request):
#     data = 'Fail'
#     if request.is_ajax():
#         if 'task_id' in request.POST.keys() and request.POST['task_id']:
#             task_id = request.POST['task_id']
#             task = AsyncResult(task_id)
#             data = task.result or task.state
#         else:
#             data = 'No task_id in the request'
#     else:
#         data = 'This is not an ajax request'
#
#     json_data = json.dumps(data)
#     return HttpResponse(json_data, content_type='application/json')

def download_test(request):
    filename = "Expenses01.xlsx"
    f = open(filename, 'rb')
    response = HttpResponse(f, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Expenses01.xlsx'
    return response
