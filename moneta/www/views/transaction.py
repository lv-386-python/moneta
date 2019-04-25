"""
This module provides views for transaction

"""
from django.http import HttpResponse

from src.python.db.transaction_manager import transaction as t
# from django.shortcuts import render


def transaction(request):
     if request.method == 'POST':
        post_data = { key: val[0] for key, val in request.POST.lists()}
        print(post_data)
        HttpResponse(200)

     return HttpResponse(404)