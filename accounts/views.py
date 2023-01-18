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
    df = df.drop_duplicates(subset=['Account Name'])
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

        if str(row['Rate setup - Rate code'])=='nan':
            rate_code  = None
        else:
            rate_code = RateCode.objects.get(rate_code= row['Rate setup - Rate code'])

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
        'rate_code':rate_code,
        'is_active': is_active}
        )

    return Response({'account imported':'account imported'})

@api_view(['GET'])
def import_bookers(request):
    file = 'mediafiles/import_data/all_bookers.csv'
    df = pd.read_csv(file)
    df = df.drop_duplicates(subset=['Company'])


    for index, row in df.iterrows():
        print(row['Company'])
        account = Account.objects.get(account_name = row['Company'])
        # account = Account.objects.first()

        booker, created = Booker.objects.update_or_create(
            account = account,
            name = row['Name'],
            email = row['Email'],
            phone_number = row['Phone'],
        )

    return Response({'bookers imported':'bookers imported'})

@api_view(['GET'])
def import_guests(request):
    file  = 'mediafiles/import_data/all_guests.csv'
    df = pd.read_csv(file)

    for index, row in df.iterrows():
        if str(row['Date Of Birth']) == 'nan':
            dob = None
        else:
            dob = datetime.strptime(str(row['Date Of Birth']), "%d-%b-%Y")
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

            if row['Nationality'] == 'Russian Federation':
                row['Nationality'] = 'Russia'

            if row['Nationality'] == 'Ireland {Republic}':
                row['Nationality'] = 'Ireland'

            if row['Nationality'] == 'Korea South':
                row['Nationality'] = 'South Korea'

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

        guest, created = GuestProfile.objects.update_or_create(
        first_name = row['First Name'] ,
        last_name = row['Last Name'] ,
        salutation = row['Salutation'],
        email = email,
        phone_number = phone_number,
        defaults = 
        {
        'guest_status' : guest_status,
        'address_line_1' : row['Address'],
        'gst_id':gst_id,
        'nationality':nationality,
        'dob' : dob,
        'company' : company,
        'guest_type':row['Source'],
        }
        )

    return Response({'guests imported':'guests imported'})