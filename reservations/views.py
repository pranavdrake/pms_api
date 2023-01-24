from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import pandas as pd
from .models import *
from accounts.models import Account,GuestProfile, Booker
from django.apps import apps
from decimal import Decimal
from accounts.models import Account

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
    file = 'mediafiles/import_data/all_forex_report.csv'
    df = pd.read_csv(file)
    df = df.drop_duplicates(subset=[''])
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

@api_view(['GET'])
def import_group_reservations(request):
    file = 'mediafiles/import_data/all_group_reservations.csv'                             
    df = pd.read_csv(file)
    df = df.drop_duplicates(subset=['Block Code'])    #unique column name to subset ?...

    for index, row in df.iterrows():

        if str(row['Group Name'])=='nan':

            group_name = None
        else:
            group_name , created = Account.objects.update_or_create(account_name= row['Group Name'].strip(), account_type = 'Group')
            # group_name = Account.objects.first()

        if row['Payment']=='nan':
            payment_type=None
        else:
            payment_type , created = PaymentType.objects.get_or_create(payment_type_code= row['Payment'])
            # payment_type = PaymentType.objects.first()

        if str(row['Company'])=='nan':
            company=None
        else:
            company = Account.objects.get(account_name= row['Company'])
            # company = Account.objects.first()

        if str(row['Agent'])=='nan':
            travel_agent = None        
        else:
            travel_agent = Account.objects.get(account_name= row['Agent'])

        if str(row['Source'])=='nan':
            source=None                             
        else:
            source = Source.objects.get(source_code= row['Source'])
            # source = Source.objects.first()

        if str(row['Market']) == 'nan':         
            market = None                        
        else:
            market = MarketCode.objects.get(market_code = row['Market'])
            # market = MarketCode.objects.first()

        if str(row['Res Type'])=='nan':
            reservation_type = None    
        else:
            reservation_type , created= ReservationType.objects.get_or_create(reservation_type = row['Res Type'].strip())
            # reservation_type = ReservationType.objects.first()

        if str(row['Rate Code'])=='nan':
            rate_code=None
        else:
            rate_code = RateCode.objects.get(rate_code = row['Rate Code'] )
            # rate_code = RateCode.objects.first()

        if str(row['package'])=='nan':
            package = None                          
        else:
            package = Package.objects.get(package_code = row['package'])
            # package = Package.objects.first()

        if str(row['Total Rooms'])=='nan':
            total_rooms = 0                          
        else:
            total_rooms = row['Total Rooms']

        if str(row['Cut-off Date']) !='nan':
            cut_off_date =datetime.strptime(str(row['Cut-off Date']),"%d-%b-%Y %H:%M:%S") 
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


@api_view(['GET'])
def import_reservations(request):
    file  = 'mediafiles/import_data/all_reservations.csv'
    df = pd.read_csv(file)
    df = df.drop_duplicates(subset=['Confirmation Code'])
    df = df.head(10)

    # Reservation.objects.all().delete()
    # return Response({'reservations imported':'reservations imported'})

    for index, row in df.iterrows():
        
        if str(row['Email'])!='nan':
            guest = GuestProfile.objects.get(email = row['Email'])
        else:
            guest = GuestProfile.objects.get(last_name  = row['Contact Name'])
        # guest = GuestProfile.objects.first()

        arrival_date  =  datetime.strptime(row['Arrival'],"%d-%b-%Y")
        departure_date  =  datetime.strptime(row['Departure'],"%d-%b-%Y")
        room_type  =  RoomType.objects.get(room_type = row['Room Type'])
        
        if str(row['Selected Room'])!= 'nan':
            selected_room  =  Room.objects.get(room_number = row['Selected Room'])
        else:
            selected_room = None

        if str(row['Rate code'])!= 'nan':
            rate_code  =  RateCode.objects.get(rate_code = row['Rate code'])

        if str(row['RTC'])!= 'nan':
            room_type_to_charge  =  RoomType.objects.get(room_type = str(row['RTC']))

        if str(row['Package'])!= 'nan':
            package  =  Package.objects.get(package_code = str(row['Package']))

        if str(df['Extra Code'][index]) != 'nan':
            extra_ids = []
            for extra in df['Extra Code'][index].split(","):
                extra = extra.strip()
                extra_ids.append(Extra.objects.get(extra_code = extra).id)
            extras  = Extra.objects.filter(pk__in = extra_ids)
        else:
            extras = []

        if str(row['Block Code'])!= 'nan':
            block_code  =  GroupReservation.objects.get(block_code = str(row['Block Code']))
            # block_code  =  GroupReservation.objects.first()
        else:
            block_code = None

        if str(row['ETA'])!= 'nan':
            eta  = datetime.strptime(row['ETA'], '%H:%M').time()

        if str(row['ETD'])!= 'nan':
            etd  = datetime.strptime(row['ETD'], '%H:%M').time()

        if str(row['Res Type'])!= 'nan':
            reservation_type,created = ReservationType.objects.get_or_create(
                reservation_type = row['Res Type'])
            
        if str(row['Market'])!= 'nan':
           market_code = row['Market'].split("-")[0]
           market = MarketCode.objects.get(market_code = market_code.strip())
            
        if str(row['Source'])!= 'nan':
           source = Source.objects.get(source_code = row['Source'])
            
        if str(row['Payment'])!= 'nan':
            paymemt_type,created = PaymentType.objects.get_or_create(
                payment_type_code = row['Payment'])


        if str(row['Company/Agent'])!= 'nan':
            company = None
            agent = None
            if(row['Company/Agent']=='Company'):
                company = Account.objects.get(account_name  = row['Account Name'])
                # company = Account.objects.first()
            if(row['Company/Agent']=='Agent'):
                agent = Account.objects.get(account_name  = row['Agent'])
            
            

        if str(row['Booker'])!= 'nan':
            booker = Booker.objects.get(name=row['Booker'])
        else:
            booker = None
        

        pick_up = None
        if row['Pickup Required']!= False:
            if str(row['Pickup Remarks'])!= 'nan':
                remarks = row['Pickup Remarks']
        
            pick_up, created =  PickupDropDetails.objects.get_or_create(
                type = 'Pickup',
                date = datetime.strptime(row['Pickup date'],"%d-%b-%Y"),
                time  = datetime.strptime(row['Pickup Time'], '%H:%M').time(),
                station_code  = row['Pickup Station Code'],
                carrier_code  = row['Pickup Carrier Code'],
                transport_type  = row['Pickup Transport Type'],
                defaults={
                'remarks'  : remarks
                }
            )
        
        drop = None
        if row['Drop Required']!= False:
            if str(row['Drop Remarks'])!= 'nan':
                remarks = row['Drop Remarks']
        
            drop, created =  PickupDropDetails.objects.get_or_create(
                type = 'Drop',
                date = datetime.strptime(row['Drop Date'],"%d-%b-%Y"),
                time  = datetime.strptime(row['Drop Time'], '%H:%M').time(),
                station_code  = row['Drop Station Code'],
                carrier_code  = row['Drop Carrier Code'],
                transport_type  = row['Drop Transport Type'],
                defaults={
                'remarks'  : remarks
                }
            )
                
        if str(row['Total Discount'])!= 'nan':
            total_discount = row['Total Discount']
        else:
            total_discount = 0

        if str(row['Total'])!= 'nan':
            total_base_amount = row['Total']
        else:
            total_base_amount = 0

        if str(row['Total Tax'])!= 'nan':
            total_tax = Decimal(row['Total Tax']).quantize(Decimal('0.00'))
        else:
            total_tax = 0

        if str(row['Total Extra Charge'])!= 'nan':
            total_extra_charge = Decimal(row['Total Extra Charge']).quantize(Decimal('0.00'))
        else:
            total_extra_charge = 0
        
        if str(row['Total Payment'])!= 'nan':
            total_payment = Decimal(row['Total Payment']).quantize(Decimal('0.00'))
        else:
            total_payment = 0

        if str(row['Stay Total'])!= 'nan':
            stay_total = Decimal(row['Stay Total']).quantize(Decimal('0.00'))
        else:
            stay_total = 0

        if str(row['TA Commision'])!= 'nan':
            travel_agent_commission = Decimal(row['TA Commision']).quantize(Decimal('0.00'))
        else:
            travel_agent_commission = 0
            
        if str(row['Total Cost Of stay'])!= 'nan':
            total_cost_of_stay = Decimal(row['Total Cost Of stay']).quantize(Decimal('0.00'))
        else:
            total_cost_of_stay = 0
        
        reservation, created = Reservation.objects.update_or_create(
                booking_id = row['Confirmation Code'],
                defaults = {
                'guest'  : guest,
                'arrival_date'  : arrival_date,
                'departure_date'  : departure_date,
                'adults': row['Adults'],
                'children': row['Children'],
                'number_of_rooms': row['No. of Rooms'],
                'room_type'  : room_type,
                'selected_room'  : selected_room,
                'rate_code'  : rate_code,
                'rate'  : row['Rate'],
                'room_type_to_charge': room_type_to_charge,
                'package': package,
                'block_code': block_code,
                'eta': eta,
                'etd': etd,
                'reservation_type': reservation_type,
                'market': market,
                'source': source,
                'origin': row['Origin'],
                'payment_type': paymemt_type,
                'balance': row['Balance'],
                'company':company,
                'agent':agent,
                'booker':booker,
                'print_rate':row['Print Rate'],
                'reservation_status':row['Status'],
                'total_discount':total_discount,
                'total_base_amount':total_base_amount,
                'total_extra_charge':total_extra_charge,
                'total_tax':total_tax,
                'total_payment':total_payment,
                'stay_total':stay_total,
                'travel_agent_commission':travel_agent_commission,
                'total_cost_of_stay':total_cost_of_stay,
                'pick_up': pick_up,
                'drop': drop,
                'comments': row['Comments'],
                'billing_instruction': row['Billing Instruction'],
                'unique_id': row['Unique ID'],
                'sub_booking_id': str(row['Sub Booking ID']),
                'transaction_id': str(row['Transaction Id']),
                'voucher_number': str(row['Voucher No']),
                }
        )
        
        reservation.extras.set(extras)
        reservation.save()

    
    return Response({'reservations imported':'reservations imported'})

@api_view(['GET'])
def import_folios(request):
    file ='mediafiles/import_data/all_guest_folio.csv'
    df = pd.read_csv(file)
    for index, row in df.iterrows():
        print(index)
        print(str(row['Booking ID']))
        # reservation = Reservation.objects.get(reservation = row['Booking ID'].strip())
        reservation = Reservation.objects.first()
        if str(row['Room']) == 'nan':
            None
        else:
            room = Room.objects.get(room_number = row['Room'])

        split_string = row['Guest'].split('.')
        salutation = split_string[0].strip()
        name = '.'.join(split_string[1:]).strip()
        if GuestProfile.objects.filter(last_name = name).count()> 1:
            guest = GuestProfile.objects.filter(last_name = name)[0]
        else:
            guest, created = GuestProfile.objects.get_or_create(last_name  = name, salutation = salutation)
        # guest = GuestProfile.objects.get(last_name = row['Last Name'].strip())

        if row['Company/Agent']=='Company':
            company_agent  =  Account.objects.get(account_name = row['Company'])
            # company_agent = Account.objects.first()
        else:
            company_agent  =  Account.objects.get(account_name = row['Agent'])
            # company_agent = Account.objects.first()

        if str(row['Company'])=='nan' and str(row['Agent'])=='nan':
            company_agent = None

        folio, cretaed = Folio.objects.update_or_create(
            folio_number = row['Folio'],
            room = room,
            reservation = reservation,
            guest = guest,
            defaults={
                'balance' : Decimal(row['Balance']).quantize(Decimal('0.00')),
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
            # reservation = Reservation.objects.get(booking_id = row['Bookings'])
            reservation = Reservation.objects.first()    

        if str(row['Room Type'])=='nan':
            room_type=None
        else:
            room_type = RoomType.objects.get(room_type = row['Room Type'])

        if row['Rate Code']=='nan':
            rate_code=None
        else:
            rate_code = RateCode.objects.get(rate_code = row['Rate Code'] )

        if row['Room'] == 'nan' :
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
            reservation = reservation,

            defaults={
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
def import_transactions(request):
    file  = 'mediafiles/import_data/transactions_test.csv'
    df = pd.read_csv(file, on_bad_lines='skip')
    df = df.drop_duplicates(subset=['ID'])
    df = df.head(80)
    Transaction.objects.all().delete()

    for index, row in df.iterrows():
    #     print(str(row['ID']))
    # return Response({'test': ' test'})

        print(index)
        # print(str(row['Is Cancelled']))
        # print(type(row['Is Cancelled']))
        # print(str(row['Company']))
        if row['Is Deposit']=='NaN':
            is_deposit = ''
        elif row['Is Deposit']==True:
            is_deposit = True
        else:
            is_deposit = False

        if row['Is Deposit']=='NaN':
            is_service_charge_cancelled = ''
        elif row['Is Serv Cancelled']==True:
            is_service_charge_cancelled = True
        else:
            is_service_charge_cancelled = False

        # if str(row['Is Cancelled'])=='True':
        #     is_cancelled = True
        # else:
        #     is_cancelled = False  

        if row['Is Cancelled']==True:
            is_cancelled = True
        else:
            is_cancelled = False  

        if row['Is Moved']==True:
            is_moved = True
        else:
            is_moved = False   

        if row['Is Duplicate']==True:
            is_duplicate = True
        else:
            is_duplicate = False    
        
        if str(row['Company'])=='nan' :
            company = None
        else:
            company = Account.objects.get(account_name = str(row['Company']))
            # company = company   

        if str(row['Agent'])=='nan' :
            agent = None
        else:
            agent = Account.objects.get(account_name = str(row['Agent']))
            # agent = agent

        if str(row['Disc Amount'])=='NaN' :
            discount_amount = 0
        else:
            discount_amount = row['Disc Amount']


        if str(row['Tax Percent'])== 'nan' :
            tax_percentage = 0
        else:
            tax_percentage = row['Tax Percent']

        if str(row['Amount'])== 'NaN' :
            base_amount = 0
        else:
            base_amount = row['Amount']

        if str(row['CGST'])== 'nan' :
            cgst = 0
        else:
            cgst = row['CGST']

        if str(row['SGST'])== 'nan' :
            sgst = 0
        else:
            sgst = row['SGST']

        
        if str(row['Total'])== 'nan' :
            total = 0
        else:
            total = row['Total']

        if str(row['Service Charge'])== 'nan' :
            service_charge_commission = 0
        else:
            service_charge_commission = row['Service Charge']

        if str(row['Ser Tax Percent'])== 'nan' :
            service_charge_commission_tax_percentage = 0
        else:
            service_charge_commission_tax_percentage = row['Ser Tax Percent']

        if str(row['Ser CGST'])== 'nan' :
            service_charge_commission_cgst = 0
        else:
            service_charge_commission_cgst = row['Ser CGST']

        if str(row['Ser SGST'])== 'nan' :
            service_charge_commission_sgst = 0
        else:
            service_charge_commission_sgst = row['Ser SGST']

        if str(row['Total With Service Charge'])== 'nan' :
            total_with_service_charge_commission = 0
        else:
            total_with_service_charge_commission = row['Total With Service Charge']

        if str(row['Date-Time'])== 'NaN' :
            transaction_date_time = ''
        else:
            transaction_date_time = datetime.strptime(str(row['Date-Time']),"%d-%b-%Y %H:%M:%S")
            transaction_date_time = transaction_date_time
      
        if str(row['Bill Date'])== 'nan':
            bill_date = None
        else:
            bill_date = datetime.strptime(str(row['Bill Date']),"%d-%b-%Y %H:%M:%S")

        if str(row['POS Bill Number'])== 'nan' :
            pos_bill_number = ''
        else:
            pos_bill_number = row['POS Bill Number']

        if str(row['POS Session'])== 'nan' :
            pos_session = ''
        else:
            pos_session = row['POS Session']

        if str(row['Type'])== 'nan' :
            transaction_type = ''
        else:
            transaction_type = row['Type']

        if str(row['Disc percentage'])== 'nan' :
            discount_percentage = 0
        else:
            discount_percentage = row['Disc percentage']

        if str(row['Disc Amount'])== 'nan' :
            discount_amount = 0
        else:
            discount_amount = row['Disc Amount']

        if str(row['Remarks'])== 'nan' :
            remarks = ''
        else:
            remarks = row['Remarks']

        if str(row['Supplement'])== 'nan' :
            supplement = ''
        else:
            supplement = row['Supplement']

        if str(row['Room Number'])== 'nan' :
            room = None
        else:
            room = Room.objects.get(room_number = row['Room Number'])
            room = room

        if str(row['Package'])== 'nan':
            package = None
        else:
            package = Package.objects.get(package_code = row['Package'])

        if str(row['Rate code'])== 'nan':
            rate_code = None
        else:
            rate_code = RateCode.objects.get(rate_code = row['Rate code'])

        if(str(row['Guest Name']))=='nan':
                guest = None
        else:
            split_string = row['Guest Name'].split('.')  
            salutation = split_string[0].strip()
            name = '.'.join(split_string[1:]).strip()
            if GuestProfile.objects.filter(last_name = name).count()> 1:
                guest = GuestProfile.objects.filter(last_name = name)[0]
                print(guest)
            else:
                guest, created  = GuestProfile.objects.get_or_create(last_name  = name)
               
        # folio = Folio.objects.get(folio = row['Folio No'])
        folio = Folio.objects.first()
        transaction_code=TransactionCode.objects.get(transaction_code = str(row['Transaction Code']))
        # reservation = Reservation.objects.get(reservation = row['Booking ID'].strip())
        reservation = Reservation.objects.first()
        # passer_by = PasserBy.objects.get(passer_by = row[' '])
        transaction, created = Transaction.objects.update_or_create(
            internal_id = row['ID'],
            defaults={
                        'transaction_code' : transaction_code,
                        'folio' : folio,
                        'transaction_date_time' : transaction_date_time,
                        'bill_date' : bill_date,
                        'reservation' : reservation,
                        'guest':guest,
                        'rate_code' : rate_code,
                        'room' : room,
                        'package' : package,
                        'company' : company,
                        'agent' : agent,
                        'base_amount' : base_amount,
                        'remarks' : remarks,
                        # # 'quantity' : row[''],
                        'supplement' : supplement,
                        # # 'description' : row[''],
                        'discount_amount': discount_amount,
                        'discount_percentage' : discount_percentage,
                        'transaction_type' : transaction_type,
                        'is_deposit' : is_deposit,
                        'tax_percentage' : tax_percentage,
                        'cgst': cgst,
                        'sgst': sgst,
                        'total': total,
                        # 'service_charge_commission_percentage' : row[''],
                        'service_charge_commission' : service_charge_commission,
                        'service_charge_commission_tax_percentage':service_charge_commission_tax_percentage,
                        'service_charge_commission_cgst': service_charge_commission_cgst,
                        'service_charge_commission_sgst' : service_charge_commission_sgst,
                        'total_with_service_charge_commission' : total_with_service_charge_commission,
                        'is_service_charge_cancelled' : is_service_charge_cancelled,
                        'is_cancelled' : is_cancelled,
                        'is_moved':is_moved,
                        'is_duplicate': is_duplicate,
                        'pos_bill_number' : pos_bill_number,
                        'pos_session' : pos_session,
                        # 'allowance_transaction' : allowance_transaction,
                        # invoice :row[''],
                        # card : row[''],

                        # 'commission_service_charge_percentage' : row[''],
                        
                    })
        
    return Response({'transactions imported':'transactions imported'})


# @api_view(['GET'])
# def import_transactions(request):
#     file  = 'mediafiles/import_data/transactions_test.csv'
#     df = pd.read_csv(file)

#     Transaction.objects.all().delete()

#     return Response({'transactions deleted':'transactions deleted'})


