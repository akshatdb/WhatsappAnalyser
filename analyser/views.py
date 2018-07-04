# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from analysis.engine import create
from forms import UploadFileForm
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import random

def index(request):
  return render(request, "analyser/index.html", {"msg":"what"})
# Create your views here.
@api_view(['POST'])
@authentication_classes((TokenAuthentication, ))
@permission_classes((AllowAny, ))
def analyse(request):
    if request.method == 'POST':
      form = UploadFileForm(request.POST, request.FILES)
      if form.is_valid():
        msg = create(request.FILES['msgfile'].read())
        return JsonResponse({"response":msg})
      return JsonResponse({"response":form.errors})
    else:
		return JsonResponse({"response":"Invalid Method"})