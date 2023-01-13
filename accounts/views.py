import datetime
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import pandas as pd
from .models import *
from django.apps import apps

# Create your views here.
@api_view(['GET'])
def import_accounts(request):
    file  = 'mediafiles/import_data/all_accounts.csv'
    df = pd.read_csv(file)

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
    file  = 'mediafiles/import_data/all_guests.csv'
    df = pd.read_csv(file)
    
    for index, row in df.iterrows():
        print(index)
        # dob = datetime.strptime(row['Date Of Birth'], "%d-%b-%Y")
        
        if row['Phone'] == 'nan':
            phone_number = ''
        else:
            phone_number = row['Phone']

        if row['Nationality'] == 'nan':
            nationality = ''
        else:
            nationality = row['Nationality']

        if row['Email'] == 'nan':
            email = ''
        else:
            email = row['Email']
        
        # account = Account.objects.get(account_name = row['Account Name'])
        all_guest, created = GuestProfile.objects.update_or_create(
        email = email ,
        phone_number = phone_number,
        
        defaults = 
        {
        'last_name' :row['Name'] ,
        # 'guest_status' :row['Status'] ,
        'salutation' : row['Salutation'],
        'address_line_1' : row['Address'],
        'gst_id':row['GST'],
        'nationality':nationality,
        # 'dob' : dob,
        # 'guest_preferences':row['Guest Preferences'],
        'guest_type':row['Source'],
        }
        )
    
    return Response({'account imported':'account imported'})
