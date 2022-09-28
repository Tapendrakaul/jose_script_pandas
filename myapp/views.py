import os
from django.conf import settings
import pandas as pd
from django.shortcuts import render
import csv
from collections import Counter
from django.http import HttpResponse
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from sqlalchemy import create_engine
from django.core.files.storage import FileSystemStorage
from django.views import View
from django.contrib import messages

from helpers import sanitise_column

from .forms import LoginForm, SignupForm
from.forms import LoginForm, SignupForm
from django.contrib.auth.models import User
import numpy as np 


# Create your views here.
# data_file_name = 'data_file'
# folder_path = 'Jose_Galeras/upload_files'
# if not os.path.exists(folder_path):
#     os.mkdir(folder_path)


# Create your views here.
data_file_name = 'data_file'
folder_path = 'upload_files'
if not os.path.exists(folder_path):
    os.mkdir(f'{folder_path}')


def signupView(request):
    """ Signup view """
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save()
			    # login(request, user)
                messages.success(request, "Thanks for registering. You are now logged in.")
                # login(request, user)
                return redirect('/login')
        else:
            form = SignupForm()
        return render(request, 'signup.html', {'form': form})


def loginView(request):
    """ Login view """
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            form = LoginForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('/')
        else:
            form = LoginForm()
        return render(request, 'login.html', {'form': form})



@login_required(login_url="/login")
def user_logout(request):
    """ Logout view"""
    logout(request)
    return redirect('/login')



@login_required(login_url="/login")
def index(request):

    if request.method == 'POST' and request.FILES.get('filename'):
        file_name = request.FILES.get('filename')
        
        data_filename = data_file_name+get_extention(file_name.name)
        # remove exists file
        removeExistsFile(data_filename)
        fs = FileSystemStorage(location=folder_path)
        filename = fs.save(data_filename, file_name)
        # file_url = fs.url(filename)
        return redirect('/')

    return render(request, 'index.html')


def uploadExcel(request):
    if request.method == 'POST':
        file_name = request.files.get('filename')

        con = con.connect()
        dfs = pd.read_excel(file_name, sheet_name=None)
        
        for table, df in dfs.items():
            df.columns = sanitise_column(df.columns)

        response = {
                'status': 1,
                'message': "Successfully uploaded."
            }
        return response




def removeExistsFile(filename):
    if os.path.exists(folder_path+'/'+filename):
        os.remove(folder_path+'/'+filename)

    return True


def get_extention(file):
    file_ext = os.path.splitext(file)[1]
    return file_ext



def exportCSV(request, num):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{num}.csv"'
    city_list = []
    file_name = f'{folder_path}/{data_file_name}.xlsx'

    files = os.listdir(folder_path)
    if len(files) == 0:
        return
    user_count = num
    for f in files:
        fullname = f'{folder_path}/{f}'
        if os.path.isfile(fullname):
            df_sampless = pd.read_excel(file_name, engine='openpyxl')
            aa = df_sampless['reviews'] = df_sampless['reviews'].fillna(0).astype(np.int64)

            df_samples = df_sampless['city'].tolist()
            coun = dict(Counter(df_samples))

            for k,v in coun.items():
                if v == user_count:
                    city_list.append(k)

            # for header code 
            HeaderList = list(df_sampless.columns.values)
            columns = HeaderList*user_count
            UniqueValues = set(columns)
            for x in UniqueValues:
                number = 0
                for i in range(0,len(columns)):
                    if columns[i] == x:
                        number += 1
                        if number >= 1:
                            columns[i] += str(number)

    # loop for city list and code responsible for creating csv
    count = 0
    for city in city_list:
        count = count +1
        print("THe city name is :",city)

        df_new = df_sampless[df_sampless['city'] == (city)]
        df = df_new.values.reshape(1, -1)

        df = pd.DataFrame(df)
        if count == 1:
            df.to_csv(path_or_buf=response, index=False, header=columns, encoding='utf8')
        else:
             df.to_csv(path_or_buf=response, mode="a", index=False, header=False, encoding='utf8')
        
    return response


