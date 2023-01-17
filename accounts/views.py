from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import pandas as pd
from .models import *
from django.apps import apps
from datetime import datetime
from django_countries import countries

# Create your views here.
@api_view(['GET'])
def import_accounts(request):
    file  = 'mediafiles/import_data/all_accounts.csv'
    df = pd.read_csv(file)

    # Account.objects.all().delete()    
    for index, row in df.iterrows():
        print(index)
        if str(row['Email'])=='nan':
            email  = ''
        else:
            email = row['Email']

        if str(row['GST ID'])=='nan':
            gst_id  = ''
        else:
            gst_id = row['GST ID']

        if str(row['Status'])=='nan':
            is_active = False
        elif row['Status']=='Active':
            is_active = True
        else:
            is_active = False
        
        if str(row['Account Type'])=='nan':
            account_type  = None
        else:
            account_type = row['Account Type']

        if str(row['Phone'])=='nan':
            phone_number  = ''
        else:
            phone_number = row['Phone']

        if str(row['IATA'])=='nan':
            iata  = ''
        else:
            iata = row['IATA']
        
        account_name, created = Account.objects.update_or_create(
        account_name=row['Account Name'],
        account_type = account_type,
        email =email,
        phone_number = phone_number,
        defaults={
        'address_line_1' : row['Address'],
        'iata':iata,
        'gst_id':gst_id,
        'is_btc_approved':row['Is BTC Approved'],
        'is_active': is_active}
        )
    
    return Response({'account imported':'account imported'})

@api_view(['GET'])
def import_guest_profiles(request):
    file  = 'mediafiles/import_data/all_guests_test.csv'
    df = pd.read_csv(file)

    # GuestProfile.objects.all().delete()    
    for index, row in df.iterrows():
        print(index)  
        if str(row['Date Of Birth']) == 'nan':
            dob = None
        else:
            dob = datetime.strptime(str(row['Date Of Birth']), "%d-%b-%Y")
            print(row['Date Of Birth'])
            dob = dob

        if str(row['Phone']) == 'nan':
            phone_number = ''
        else:
            phone_number = row['Phone']
        
        if str(row['Status']) == 'nan':
            guest_status = ''
        else:
            guest_status = row['Status']
        
        if str(row['Nationality']) == 'nan':
            nationality = ''
        else:
            COUNTRY_DICT = dict(countries)

            if row['Nationality'] == 'United States':
                row['Nationality'] = 'United States of America'
            
            nationality = list(filter(lambda x: COUNTRY_DICT[x] == row['Nationality'], COUNTRY_DICT))[0]

        if str(row['GST']) == 'nan':
            gst_id = ''
        else:
            gst_id = row['GST']

        if str(row['Email']) == 'nan':
            email = ''
        else:
            email = row['Email']
        
        if str(row['Corporate']) == 'nan':
            company = None
        else:
            company = Account.objects.get(account_name = row['Corporate'])

        # print(row['Corporate'])
        all_guest, created = GuestProfile.objects.update_or_create(
        email = email ,
        phone_number = phone_number,
        last_name = row['Last Name'] ,
        salutation = row['Salutation'],

        defaults = 
        {
        'first_name' : row['First Name'] ,
        'guest_status' : guest_status,
        'address_line_1' : row['Address'],
        'gst_id':gst_id,
        'nationality':nationality,
        'dob' : dob,
        'company' : company,
        'guest_type':row['Source'],
        }
        )

    return Response({'guest imported':'guest imported'})

