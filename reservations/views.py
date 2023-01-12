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
def import_groups(request):
    file  = 'mediafiles/import_data/all_groups.csv'
    df = pd.read_csv(file)
    df = df.drop_duplicates(subset=['Group Code'])
    for index, row in df.iterrows():
        if row['Status'].strip()=='Active':
            is_active = True
        else:
            is_active = False

        if str(row['Description']) == 'nan':
            description = ''
        else:
            description = row['Description']
        if str(row['Cost Center Type']) == 'nan':
            cost_center = ''
        else:
            cost_center = row['Cost Center Type']

        group, created = Group.objects.update_or_create(group_code=row['Group Code'], defaults={'description': description, 'cost_center': cost_center})

    return Response({'groups imported':'groups imported'})

@api_view(['GET'])
def import_sub_groups(request):
    file  = 'mediafiles/import_data/all_sub_groups.csv'
    df = pd.read_csv(file)
    for index, row in df.iterrows():
        if str(row['Description']) == 'nan':
            description = ''
        else:
            description = row['Description']

        # group=Group.objects.get(group = row['Group'])  
        sub_group, created = SubGroup.objects.update_or_create(
        # group=group,
        sub_group_code = row['Sub Group Code'],

        defaults={
        'description': description,
        })

    return Response({'sub group imported':'sub group imported'})

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
            # reservation = reservation,
            # guest = guest,

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
        begin_sell_date = datetime.strptime(row['Begin Sell Date'],"%d-%b-%Y")
        end_sell_date= datetime.strptime(row['End Sell Date'],"%d-%b-%Y")

        if row['status'] == 'Active':
            is_active = True
        else:
            is_active = False

        # package_group = PackageGroup.objects.get(package_group = row['Package Group'])
        package_group = PackageGroup.objects.first()
        
        transaction_code = TransactionCode.objects.get(transaction_code = row['Transaction Code'])
        # transaction_code  = TransactionCode.objects.first()

        package, created = Package.objects.update_or_create( 
            package_group = package_group,
            package_code = row['Package Code'],
            defaults={'description': row['Description'],
            'transaction_code' : transaction_code, 
            'begin_sell_date' : begin_sell_date,
            'end_sell_date' : end_sell_date,
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

@api_view(['GET'])
def import_transaction_codes(request):
    file  = 'mediafiles/import_data/all_transaction_codes.csv'
    df = pd.read_csv(file)
    df = df.drop_duplicates(subset=['Transaction Code '])
    revoke_df = df[df['Revoke Group'].notnull()] 
    df = df[df['Revoke Group'].isnull()] 

    for index, row in revoke_df.iterrows():
        if row['Discount Allowed']=='true':
            discount_allowed = True
        else:
            discount_allowed = False

        if str(row['Rate'])=='nan':
            base_rate = 0
        else:
            base_rate = row['Rate']

        if str(row['Commission Percent'])=='nan':
            commission_service_charge_percentage = 0
        else:
            commission_service_charge_percentage = row['Commission Percent']

        if str(row['Tax Percentage'])=='nan':
            tax_percentage = 0
        else:
            tax_percentage = row['Tax Percentage']

        is_allowance  = True 
        group  = Group.objects.get(group_code = row['Revoke Group'].strip())
        sub_group  = SubGroup.objects.get(sub_group_code = row['Sub Group'].strip())
        # group  = Group.objects.first()
        # sub_group  = SubGroup.objects.first()

        transaction_code, created = TransactionCode.objects.update_or_create(transaction_code=row['Transaction Code '], group = group, sub_group = sub_group ,defaults={'description': row['Description'], 'base_rate': base_rate,'tax_percentage': tax_percentage,'commission_service_charge_percentage': commission_service_charge_percentage, 'discount_allowed': discount_allowed, 'is_allowance': is_allowance})

    for index, row in df.iterrows():
        if row['Discount Allowed']=='true':
            discount_allowed = True
        else:
            discount_allowed = False

        is_allowance  = False 

        if(TransactionCode.objects.filter(transaction_code =  '8' + str(row['Transaction Code '])).exists()):
            allowance_code  = TransactionCode.objects.get(transaction_code =  '8' + str(row['Transaction Code ']))
        else:
            allowance_code = None

        if str(row['Rate'])=='nan':
            base_rate = 0
        else:
            base_rate = row['Rate']

        if str(row['Commission Percent'])=='nan':
            commission_service_charge_percentage = 0
        else:
            commission_service_charge_percentage = row['Commission Percent']

        if str(row['Tax Percentage'])=='nan':
            tax_percentage = 0
        else:
            tax_percentage = row['Tax Percentage']

        group  = Group.objects.get(group_code = row['Group'].strip())
        sub_group  = SubGroup.objects.get(sub_group_code = row['Sub Group'].strip())
        # group  = Group.objects.first()
        # sub_group  = SubGroup.objects.first()
        transaction_code, created = TransactionCode.objects.update_or_create(transaction_code=row['Transaction Code '],
          defaults={'description': row['Description'],
           'base_rate': base_rate,
           'tax_percentage': tax_percentage,
           'commission_service_charge_percentage': commission_service_charge_percentage, 
           'discount_allowed': discount_allowed, 
            'group' : group,
            'sub_group' : sub_group ,
            'allowance_code' :allowance_code,
           'is_allowance': is_allowance})

    return Response({'transaction codes imported':'transaction codes imported'})

@api_view(['GET'])
def import_rate_codes(request):
    # rc= RateCode.objects.first()
    # print(rc.days_applicable)
    # rc.days_applicable.clear()
    # rc.days_applicable  = ['Monday'] 
    # print(rc.days_applicable)
    # rc.save()
    # print(RateCode.objects.first().days_applicable)
    file  = 'mediafiles/import_data/all_rate_codes.csv'
    df = pd.read_csv(file)
    df = df.drop_duplicates(subset=['Rate code'])

    for index, row in df.iterrows():

        
        begin_sell_date = datetime.strptime(row['Begin_date'], "%d-%b-%Y")
        end_sell_date = datetime.strptime(row['End _sell_Date'], "%d-%b-%Y")
        rate_category = RateCategory.objects.get(rate_category = row['Rate Category'].strip())
        # rate_category = RateCategory.objects.first()
        if(MarketCode.objects.filter(market_code = str(row['Market Code']).strip()).exists()):
            market=MarketCode.objects.get(market_code = str(row['Market Code']).strip())
        else:
            market = None
        
        if str(row['Source'])=='nan':
            source = None
        else:
            source=Source.objects.get(source_code = row['Source'])
        # source=Source.objects.first()

        room_type_ids = []
        for room_type in df['Room Type'][index].split(","):
            room_type = room_type.strip()
            room_type_ids.append(RoomType.objects.get(room_type = room_type).id)
        room_types  = RoomType.objects.filter(pk__in=room_type_ids)

        if str(df['Extras'][index]) != 'nan':
            extra_ids = []
            for extra in df['Extras'][index].split(","):
                extra = extra.strip()
                
                extra_ids.append(Extra.objects.get(extra_code = extra).id)
            extras  = Extra.objects.filter(pk__in = extra_ids)
        else:
            extras = []

        days_applicable  = []
        if(str(df['Days'][index])!='nan'):
            for day in df['Days'][index].split(","):
                days_applicable.append(day)
        print(row['package'])
        if str(row['package'])=='nan':
            package = None
        else:
            package = Package.objects.get(package_code = row['package'])
        # package = Package.objects.first()
        
        if str(row['Pkg Transaction Code'])=='nan':
            package_transaction_code = None
        else:
            package_transaction_code = TransactionCode.objects.get(transaction_code = str(int(row['Pkg Transaction Code'])))
            
        transaction_code=TransactionCode.objects.get(transaction_code = str(row['Transaction Code']))

        rate_code, created = RateCode.objects.update_or_create(
            rate_category=rate_category,
            rate_code = row['Rate code'],
            defaults={
                        'description': row['Description'],
                        'market' : market,
                        'source' : source,
                        'begin_sell_date' : begin_sell_date,
                        'end_sell_date' : end_sell_date,
                        'package' : package,
                        # 'extras' : extras,
                        'transaction_code' : transaction_code,
                        'package_transaction_code' : package_transaction_code,
                        # 'room_types' : room_types,
                        # 'days_applicable' : days_applicable,
                        'print_rate' : row['Print Rate'],
                        'day_use' : row['Day Use'],
                        'discount' : row['Discount'],
                        'complementary' : row['Complementary'],
                        'house_use' : row['House Use'],
                    })
        
        rate_code.room_types.set(room_types)
        rate_code.extras.set(extras)
        rate_code.days_applicable = days_applicable
        rate_code.save()

    return Response({'rate codes imported':'rate codes imported'})