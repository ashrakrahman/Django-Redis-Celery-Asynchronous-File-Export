
import time
import csv
from celery import task
from django.http import HttpResponse
from django.contrib.auth.models import User
import xlsxwriter
from django.http import (HttpResponseRedirect, HttpResponse)
from django.shortcuts import redirect


@task()
def aysc_func():
    # Let us assume, our Export takes 10 sec to execute
    time.sleep(10)
    #print ("okkkk")
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('Expenses01.xlsx')
    worksheet = workbook.add_worksheet()

    # Some data we want to write to the worksheet.
    expenses = (
        ['Rent', 1500],
        ['Gas', 100],
        ['Food', 300],
        ['Gym', 50],
    )

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0
    # Iterate over the data and write it out row by row.
    for item, cost in (expenses):
        worksheet.write(row, col, item)
        worksheet.write(row, col + 1, cost)
        row += 1
    # Write a total using a formula.
    worksheet.write(row, 0, 'Total')
    worksheet.write(row, 1, '=SUM(B1:B4)')
    workbook.close()
    print("okkkk")
    return 1


def export_users_csv():
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'
    writer = csv.writer(response)
    writer.writerow(['Username', 'First name', 'Last name', 'Email address'])
    users = User.objects.all().values_list(
        'username', 'first_name', 'last_name', 'email')
    for user in users:
        writer.writerow(user)

    return response
