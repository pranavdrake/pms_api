from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import pandas as pd
from .models import *
from django.apps import apps

@api_view(['GET'])
def import_room_types(request):
    file  = 'mediafiles/import_data/all_room_types.csv'
    df = pd.read_csv(file)
    df = df.drop_duplicates(subset=['Type Name'])

    for index, row in df.iterrows():
        property = Property.objects.first()
        room_type, created = RoomType.objects.update_or_create(
            property=property,
            room_type=row['Type Name'],
            defaults={
                'max_adults': row['Number Of Adults'],
                'max_children': row['Number Of Child'],
                'total_number_of_rooms': row['Total Number of Rooms'],
            }
        )
    return Response({'room types imported':'room types imported'})

@api_view(['GET'])
def import_rooms(request):
    file  = 'mediafiles/import_data/all_rooms.csv'
    df = pd.read_csv(file)
    df = df.drop_duplicates(subset=['Room Number'])

    
    for index, row in df.iterrows():

        if Floor.objects.filter(property = Property.objects.first(), floor=int(row['Floor'])).exists():
            floor = Floor.objects.get(property = Property.objects.first(), floor=int(row['Floor']))
        else:
            Floor.objects.create(property = Property.objects.first(), floor=int(row['Floor']))
            floor = Floor.objects.get(property = Property.objects.first(), floor=int(row['Floor']))

        room_type = RoomType.objects.get(room_type=row['Room Type'])
        room, created = Room.objects.update_or_create(
            floor=floor,
            room_type=room_type,
            room_number=row['Room Number'],
            defaults={
                'room_status': row['Room Status'],
                'front_office_status': row['FO Status'],
                'reservation_status': row['Reservation Status'],
            }
        )

    return Response({'rooms imported':'rooms imported'})

@api_view(['GET'])
def import_market_groups(request):
    file  = 'mediafiles/import_data/all_market_groups.csv'
    df = pd.read_csv(file)
    df = df.drop_duplicates(subset=['Market Group'])
    for index, row in df.iterrows():
        if row['Status'].strip()=='Active':
            is_active = True

        market_group, created = MarketGroup.objects.update_or_create(market_group=row['Market Group'], defaults={'description': row['Description'], 'is_active': is_active})
    
    return Response({'market groups imported':'market groups imported'})

@api_view(['GET'])
def import_market_codes(request):
    file  = 'mediafiles/import_data/all_market_codes.csv'
    df = pd.read_csv(file)
    df = df.drop_duplicates(subset=['Market Code'])

    for index, row in df.iterrows():
        if row['Status'].strip()=='Active':
            is_active = True
        else:
            is_active = False

        market_group=MarketGroup.objects.get(market_group = row['Market Group'].strip())
        market_code, created = MarketCode.objects.update_or_create(market_group=market_group, market_code = row['Market Code'], defaults={'description': row['Description'], 'is_active': is_active})

    return Response({'market codes imported':'market codes imported'})


@api_view(['GET'])
def import_source_codes(request):
    file = 'mediafiles/import_data/all_sources.csv'
    df = pd.read_csv(file)
    df = df.drop_duplicates(subset=['Source Code'])

    for index, row in df.iterrows():
        if row['Status'].strip()=='Active':
            is_active = True
        else:
            is_active = False

        source_group = SourceGroup.objects.get(source_group = row['Source Group'].strip())
        source_code, created = Source.objects.update_or_create(source_group = source_group, source_code = row['Source Code'], defaults={'description': row['Description'],'is_active': is_active})

    return Response({'source codes imported':'source codes imported'})


@api_view(['GET'])
def import_rate_classes(request):
    file = 'mediafiles/import_data/all_rate_classes.csv'
    df = pd.read_csv(file)
    df = df.drop_duplicates(subset=['Rate Class'])

    for index, row in df.iterrows():
        if row['Status'].strip()=='Active':
            is_active = True
        else:
            is_active = False
        
        rate_class, created = RateClass.objects.update_or_create(rate_class = row['Rate Class'], defaults={'description': row['Description'],'is_active': is_active})

    return Response({'rate classes imported':'rate classes imported'})


@api_view(['GET'])
def import_rate_categories(request):
    file = 'mediafiles/import_data/all_rate_categories.csv'
    df = pd.read_csv(file)
    df = df.drop_duplicates(subset=['Rate Category'])

    for index, row in df.iterrows():
        if row['Status'].strip()=='Active':
            is_active = True
        else:
            is_active = False

        rate_class = RateClass.objects.get(rate_class = row['Rate Class'].strip())
        rate_category, created = RateCategory.objects.update_or_create(rate_class = rate_class, rate_category = row['Rate Category'], defaults={'description': row['Description'],'is_active': is_active})

    return Response({'rate categories imported':'rate categories imported'})


@api_view(['GET'])
def import_forexes(request):
    file = ''
    df = pd.read_csv(file)
    df = df.drop_duplicates(subset=[''])

    for index, row in df.iterrows():
        if str(row['Remarks']) == 'nan':
            remarks = ''
        else:
            remarks=row['Remarks']

        room = Room.objects.get(room_number = row['Room No'].strip())
        #reservation = Reservation.objects.get(reservation = row['Booking ID'].strip())
        #guest = GuestProfile.obejects.get(first_name = row['First Name'].strip(), last_name = row['Last Name'])
        forex, created = Forex.objects.update_or_create(
            room = room,  #certificate No.
            reservation = reservation,
            guest = guest,
            
            defaults={
                'currency' : row['Currency'],
                'amount' : row['Amount(FC)'],
                'rate_for_the_day' : row['Rate For The Day'],
                'equivalent_amount' : row['Eqvt Amount'],
                'cgst' : row['CGST'],
                'sgst' : row['SGST'],
                'total' : row['Total'],
                'remarks': remarks
            }
        )
    return Response({'forex imported':'forex imported'})
