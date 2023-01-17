from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import pandas as pd
from .models import *
from accounts.models import Account
from django.apps import apps
from decimal import Decimal

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
    file = 'mediafiles/import_data/all_forex_report.csv'
    df = pd.read_csv(file)
    df = df.drop_duplicates(subset=['Booking ID'])

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
    return Response({'forexes imported':'forexes imported'})



@api_view(['GET'])
def import_folios(request):
    file ='mediafiles/import_data/all_guest_folio.csv'
    df = pd.read_csv(file)
    df = df.drop_duplicates(subset=['Booking ID'])

    for index, row in df.iterrows():

        #reservation = Reservation.objects.get(reservation = row['Booking ID'].strip())
        room = Room.objects.get(room_number = row['Room'])
        #guest = GuestProfile.obejects.get(first_name = row['First Name'].strip(), last_name = row['Last Name'].strip())
        #company_agent = Account.objects.get(company_agent = row['Company/Agent'].strip())
        if row['Company/Agent']=='Company':
            company_agent  =  Account.objects.get(account_name = row['Company'])
        else:
            company_agent  =  Account.objects.get(account_name = row['Agent'])
        
        if str(row['Company'])=='nan' and str(row['Agent'])=='nan':
            company_agent = None

        folio, cretaed = Folio.objects.update_or_create(
            folio_number = row['Folio'],
            room = room,
            reservation = reservation,
            guest = guest,
            defaults={
                'balance' : row['Balance'],
                'company_agent' : company_agent,
                'is_settled': row['Is Settled'],
                'is_cancelled':row['Is_Cancelled'],
            }

        )
    
    return Response({'folios imported':'folios imported'})

@api_view(['GET'])
def import_daily_details(request):
    file = 'mediafiles/import_data/all_daily_details.csv'
    df = pd.read_csv(file)
    # df = df.drop_duplicates(subset=['Bookings']) #unique columns?.........

    for index, row in df.iterrows():
        
        if row['Disc Amt'] =='nan':
            discount_amount = 0
        else:
            discount_amount = row['Disc Amt']

        if str(row['Market']) == 'nan':         
            market_code = None
        else:
            market_code = MarketCode.objects.get(market_code = row['Market'].split('-')[0].strip())

        if row['Bookings']=='nan':
            reservation= None
        else:
            reservation = Reservation.objects.get(booking_id = row['Bookings'])  

        if str(row['Room Type'])=='nan':
            room_type=None
        else:
            room_type = RoomType.objects.get(room_type = row['Room Type'])

        if row['Rate Code']=='nan':
            rate_code=None
        else:
            rate_code = RateCode.objects.get(rate_code = row['Rate Code'] )

        if row['Room'] == 'nan':
            room = None
        else:
            room = Room.objects.get(room_number = row['Room'])            

        if row['package']=='nan':
            package = None
        else:
            package = Package.objects.get(package_code = row['package'])            

        if str(row['Source'])=='nan':
            source=None
        else:
            source = Source.objects.get(source_code= row['Source'])

        daily_detail ,created = DailyDetail.objects.update_or_create(

            date = datetime.strptime(row['Date'],"%d-%b-%Y"),
            
            defaults={
                'reservation':reservation,
                'source':source,
                'package':package,
                'room':room,
                'rate_code':rate_code,
                'room_type' : room_type,
                'market_code':market_code,
                'total_rate' : row['Rate Amount'],
                'adults' : row['Adults'],
                'children' : row['Child'],
                'discount_amount' : discount_amount,
                # 'room_rate' : row[''],                
                # 'package_rate' : row[''],             
            }
        )

    return Response({'daily details imported' : 'daily details imported'})


@api_view(['GET'])
def import_group_reservations(request):
    file = 'mediafiles/import_data/all_group_reservations.csv'                             
    df = pd.read_csv(file)
    df = df.drop_duplicates(subset=['Block Code'])    #unique column name to subset ?...

    for index, row in df.iterrows():
        print(row['Rate'])
        
        if str(row['Group Name'])=='nan':

            group_name = None
        else:
            #group_name , created = Account.objects.get_or_create(account_name= row['Group Name'].strip(), account_type = 'group')
            group_name = Account.objects.first()

        if row['Payment']=='nan':
            payment_type=None
        else:
            #payment_type , created = PaymentType.objects.get_or_create(account_name= row['Payment'])
            payment_type = PaymentType.objects.first()

        if str(row['Company'])=='nan':
            company=None
        else:
            # company = Account.objects.get(account_name= row['Company'])
            company = Account.objects.first()

        if str(row['Agent'])=='nan':
            travel_agent = None        
        else:
            travel_agent = Account.objects.get(account_name= row['Agent'].strip())

        if str(row['Source'])=='nan':
            source=None                             
        else:
            #source = Source.objects.get(source_code= row['Source'])
            source = Source.objects.first()

        if str(row['Market']) == 'nan':         
            market = None                        
        else:
            #market = MarketCode.objects.get(market = row['Market'])
            market = MarketCode.objects.first()

        if str(row['Res Type'])=='nan':
            reservation_type = None    
        else:
            #reservation_type = ReservationType.objects.get(reservation_type = row['Res Type'].strip())
            reservation_type = ReservationType.objects.first()

        if row['Rate Code']=='nan':
            rate_code=None
        else:
            #rate_code = RateCode.objects.get(rate_code = row['Rate Code'] )
            rate_code = RateCode.objects.first()

        if row['package']=='nan':
            package = None                          
        else:
            #package = Package.objects.get(package = row['package'])
            package = Package.objects.first()

        if str(row['Total Rooms'])=='nan':
            total_rooms = 0                          
        else:
            #package = Package.objects.get(package = row['package'])
            total_rooms = row['Total Rooms']

        if str(row['Cut-off Date']) !='nan':
            print(row['Cut-off Date'])
            cut_off_date =datetime.strptime(str(row['Cut-off Date']),"%d-%b-%Y %H:%M:%S")  #'%d-%b-%Y %H:%M:%S' ?...
        else:
            cut_off_date = None   

        group_reservations, created = GroupReservation.objects.update_or_create(

            block_code = row['Block Code'],                    
            
            defaults={
                'group_name': group_name,
                'payment_type':payment_type,
                'company' : company,
                'travel_agent':travel_agent,
                'source' : source,
                'market' :market,
                'reservation_type':reservation_type,
                'rate_code': rate_code,
                'package' :package,
                'arrival_date' : datetime.strptime(str(row['Arrival Date']),"%d-%b-%Y"),
                'departure_date' : datetime.strptime(str(row['Departure Date']),"%d-%b-%Y"),
                'nights' : row['Nights'],
                'status' : row['Status'],
                'origin' : row['Origin'],  
                'rate' :Decimal(row['Rate']).quantize(Decimal("0.00")),      
                'pax' : row['Pax'],        
                'cut_off_date' : cut_off_date,
                'total_rooms' :total_rooms,   
            }
        )

    return Response({'group reservstions imported' : 'group reservstions imported'})
    