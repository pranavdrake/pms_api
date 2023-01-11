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
def import_source_groups(request):
    file  = 'mediafiles/import_data/all_source_groups.csv'
    df = pd.read_csv(file)
    df = df.drop_duplicates(subset=['Source Group Code'])

    for index, row in df.iterrows():
        if row['Status'].strip()=='Active':
            is_active = True
        
        source_group, created = SourceGroup.objects.update_or_create(
            source_group=row['Source Group Code'], 
            defaults={'description': row['Description'], 'is_active': is_active})
    
    return Response({'source groups imported':'Source groups imported'})



@api_view(['GET'])
def import_extra(request):
    file  = 'mediafiles/import_data/all_extras.csv'
    df = pd.read_csv(file)
    df = df.drop_duplicates(subset=['Code'])

    for index, row in df.iterrows():
        # group = Group.objects.get(group=row['Department'].strip())
        # sub_group = SubGroup.objects.get(sub_group = row[''])
        extra, created = Extra.objects.update_or_create(
        # group = group,
        # sub_group=sub_group,
        extra_code=row['Code'],
            defaults={
                 'description': row['Description'],
                # 'type': row['Type'],
            }
        )
    return Response({'Extra Data imported':'extra data imported'})

@api_view(['GET'])
def import_package_group(request):
    file  = 'mediafiles/import_data/package_group.csv'
    df = pd.read_csv(file)
    df = df.drop_duplicates(subset=['Package Group'])

    for index, row in df.iterrows():
        package_group, created = PackageGroup.objects.update_or_create(
            package_group=row['Package Group'], 
            defaults={'description': row['Description'],})
    
    return Response({'package groups imported':'Package groups imported'})


@api_view(['GET'])
def import_package(request):
    file  = 'mediafiles/import_data/all_packages.csv'
    df = pd.read_csv(file)
    df = df.drop_duplicates(subset=['Package Code'])

    for index, row in df.iterrows():
        if row['status'].strip() == 'Active':
            is_active = True
        else:
            is_active = False

        # package_group = PackageGroup.objects.get(package_group = row['Package Group'])
        # transaction_code = TransactionCode.objects(transaction_code = row['Transaction Code'])
        package, created = Package.objects.update_or_create( 
            # package_group = package_group,
            # transaction_code = transaction_code, 
            package_code = row['Package Code'],
            defaults={'description': row['Description'],
            'begin_sell_date' : row['Begin Sell Date'],
            'end_sell_date' : row['End Sell Date'],
            'base_price' : row['Price'],
            'tax_percentage' : row['Tax Percentage'],
            # 'tax_amount' : row[''],
            # 'total_amount' : row[''],
            'calculation_rule' : row['calculation Rule '],
            'posting_rhythm' : row['Posting Rhythm'],
            'rate_inclusion' : row['Rate Inclusion'],
            'is_active' : is_active
            })
    
    return Response({'package imported':'Package imported'})

