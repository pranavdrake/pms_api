from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import pandas as pd
from .models import *
from django.apps import apps




@api_view(['GET'])
def import_bookers(request):
    file = 'mediafiles/import_data/all_bookers.csv'
    df = pd.read_csv(file)
    df = df.drop_duplicates(subset=['Company'])
    

    for index, row in df.iterrows():
        # account = Account.objects.get(account_name = row['Company'])
        account = Account.objects.first()

        booker, created = Booker.objects.update_or_create(
            account = account,
            name = row['Name'],
            email = row['Email'],
            phone_number = row['Phone'],
        )

    return Response({'bookers imported':'bookers imported'})