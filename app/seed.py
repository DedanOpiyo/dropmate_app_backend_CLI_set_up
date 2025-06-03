# app/seed.py
#!/usr/bin/env python3

# Script goes here!
from datetime import datetime, timedelta

from app.models import User, Location, RouteGroup, Route, ShippingCost, Shipment, Service, RouteLocation, ItemCategory, ShipmentItem, Border, RouteTag, DropLog
from app.models.user import ProfileType
from app.models.location import LocationType # Enum Location type. -for seeding locations.
from app.models.route import BorderTypeRt
from app.models.shipment import ShipmentStatus, ShipmentType
from app.models.border import BorderType, BorderStatus
from app.models.drop_log import DropLogStatus
from app.models.shipmentContactInfo import ShipmentContactInfo 

from faker import Faker
import random
# ProfileType.(choice([customer, company, admin])) # only company to add services -implement later

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

if __name__ == '__main__':
    engine = create_engine('sqlite:///app/dropmate.db')  # relative to project root- app
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(User).delete()
    session.query(Location).delete()
    session.query(RouteGroup).delete()
    session.query(Route).delete()
    session.query(ShippingCost).delete()
    session.query(Service).delete()
    session.query(Shipment).delete()
    session.query(RouteLocation).delete()
    session.query(ItemCategory).delete()
    session.query(ShipmentItem).delete()
    session.query(Border).delete()
    session.query(RouteTag).delete()
    session.query(DropLog).delete()

    fake = Faker()

    users = []
    for i in range(15):
        user = User(
            real_name=fake.name(),
            username=fake.unique.user_name(),
            email=fake.unique.email(),
            phone_number=random.randint(1000000000, 9999999999),
            password=fake.password(),
            role=random.choice(['admin', 'user', 'moderator']),
            profile_type=random.choice([ProfileType.customer, ProfileType.company, ProfileType.admin])
        )

        # add and commit individually to get IDs back
        session.add(user)
        session.commit()

        users.append(user)

    # Step 1: Seeding countries
    countries = []
    for i in range(3):  # Seeding 3 countries
        country = Location(
            name=fake.country(),
            type=LocationType.country,
            constituency=fake.state(),
            description=fake.text(max_nb_chars=50),
            latitude=fake.latitude(),
            longitude=fake.longitude(),
            is_border=False
        )
        session.add(country)
        session.commit()
        countries.append(country)


    # Step 2: Seeding counties for each country
    counties = []
    for country in countries:
        for _ in range(2):  # 2 counties per country
            county = Location(
                name=fake.city(),
                type=LocationType.county,
                constituency=fake.state(),
                description=fake.text(max_nb_chars=50),
                latitude=fake.latitude(),
                longitude=fake.longitude(),
                country_id=country.id,
                parent_id=country.id,  # hierarchy
                is_border=random.choice([True, False])
            )
            session.add(county)
            session.commit()
            counties.append(county)

    # Step 3: Seeding towns for each county
    towns = []
    for county in counties:
        for _ in range(2):  # 2 towns per county
            town = Location(
                name=fake.city(),
                type=LocationType.town,
                constituency=fake.state(),
                description=fake.text(max_nb_chars=50),
                latitude=fake.latitude(),
                longitude=fake.longitude(),
                country_id=county.country_id,
                parent_id=county.id,
                is_border=random.choice([True, False])
            )
            session.add(town)
            session.commit()
            towns.append(town)

    # Step 4: Optional - seeding villages or estates
    for town in towns:
        for _ in range(2):  # 2 estates per town
            estate = Location(
                name=fake.street_name(),
                type=LocationType.estate,
                constituency=fake.state(),
                description=fake.text(max_nb_chars=50),
                latitude=fake.latitude(),
                longitude=fake.longitude(),
                country_id=town.country_id,
                parent_id=town.id,
                is_border=False
            )
            session.add(estate)

    session.commit()


    # Getting 5 towns or counties to act as region centers for RouteGroups
    region_locations = session.query(Location).filter(
        Location.type.in_([LocationType.town, LocationType.county]) # still using location's enum
    ).limit(5).all()

    route_groups = []

    for loc in region_locations:
        rg = RouteGroup(
            name=f"{loc.name} {random.choice(['Express', 'Metro', 'Zone', 'Group'])}", # realistic RouteGroup names like: e.g. Eldoret Express
            description=fake.text(max_nb_chars=80),
            region_location_id=loc.id
        )
        session.add(rg)
        session.commit()
        route_groups.append(rg)

    print(f"Seeded {len(route_groups)} route groups.")


    # Get towns or estates to use as endpoints
    endpoints = session.query(Location).filter(
        Location.type.in_([LocationType.estate, LocationType.town])
    ).all()

    # Get existing route groups
    route_groups = session.query(RouteGroup).all()

    routes = []

    for _ in range(10):  # Seed 10 random routes
        origin = random.choice(endpoints)
        destination = random.choice(endpoints)

        # Skip same-location routes
        if origin.id == destination.id:
            continue

        # Pick a random route group (optional)
        route_group = random.choice(route_groups) if route_groups else None

        # Determine scope based on logic (customize as needed)
        if origin.country_id != destination.country_id:
            scope = BorderTypeRt.cross_country
        elif origin.parent_id != destination.parent_id:
            scope = BorderTypeRt.inter_county
        else:
            scope = random.choice(list(BorderTypeRt))  # fallback random

        route = Route(
            origin_location_id=origin.id,
            destination_location_id=destination.id,
            route_group_id=route_group.id if route_group else None,
            scope=scope
        )

        session.add(route)
        session.commit()
        routes.append(route)

    print(f"Seeded {len(routes)} routes.")


    # Get all routes that do not yet have a shipping cost
    routes = session.query(Route).filter(Route.shipping_cost == None).all() # after refactor, instead of == None, we use .is_(None)

    shipping_costs = []

    for route in routes:
        cost = random.randint(300, 2000)  # Assign random cost

        # Optionally use a time range (e.g. valid from today to +90 days)
        start_date = datetime.now()
        end_date = start_date + timedelta(days=random.choice([30, 60, 90]))

        shipping_cost = ShippingCost(
            route_id=route.id,
            cost_value=cost,
            start_date=start_date,
            end_date=end_date,
            active=True
        )

        session.add(shipping_cost)
        session.commit()
        shipping_costs.append(shipping_cost)

    print(f"Seeded shipping costs for {len(shipping_costs)} routes.")


    # shipping_cost_id was deleted...

    # # GOAL: Step : Update routes with the matching shipping_cost_id
    # # we can loop through the seeded ShippingCost records and update each corresponding Route:

    # shipping_costs = session.query(ShippingCost).all()

    # updated_count = 0
    # for sc in shipping_costs:
    #     route = session.query(Route).filter_by(id=sc.route_id).first()
    #     if route:
    #         route.shipping_cost_id = sc.id
    #         updated_count += 1

    # session.commit()
    # print(f"Updated {updated_count} routes with shipping_cost_id.")


    # Get a list of users (ensure users are in the DB)
    users = session.query(User).filter_by(profile_type=ProfileType.company).all() # filter where role/profile_type is company 

    services = []

    # Create 10 services randomly assigned to users
    for _ in range(10):
        user = random.choice(users)
        
        service = Service(
            user_id=user.id,
            company_name=fake.company(),
            service_name=random.choice([
                "Parcel Delivery", "Express Courier", "Freight", 
                "Logistics Management", "Same Day Delivery"
            ]),
            cost=random.randint(100, 5000),  # Random cost
            license=fake.uuid4(),  # Simulated license string
            image_url=fake.image_url()  # Optional
        )

        session.add(service)
        services.append(service)

    session.commit()

    print(f"Seeded {len(services)} services.")


    # Fetch required dependencies
    users = session.query(User).all()
    services = session.query(Service).all()
    routes = session.query(Route).all()
    locations = session.query(Location).all()

    shipments = []

    # Let's seed 15 shipments
    for _ in range(15):
        user = random.choice(users)
        service = random.choice(services)
        route = random.choice(routes)

        # Ensure valid origin and destination from the route
        origin = route.origin
        destination = route.destination

        shipment = Shipment(
            user_id=user.id,
            origin_location_id=origin.id,
            destination_location_id=destination.id,
            route_id=route.id,
            service_id=service.id,
            status=random.choice(list(ShipmentStatus)),
            shipment_type=random.choice(list(ShipmentType)),
            shipping_cost=random.randint(300, 10000)
        )

        session.add(shipment)
        shipments.append(shipment)

    session.commit()

    print(f"Seeded {len(shipments)} shipments.")



    # Seeding RouteLocation - Origin comes first, Destination Last.

    # Fetch existing routes and locations
    routes = session.query(Route).all()
    locations = session.query(Location).all()

    route_locations = []

    for route in routes:
        # Select 1 to 3 random intermediate locations excluding origin and destination
        intermediate_locations = random.sample(
            [loc for loc in locations if loc.id not in (route.origin_location_id, route.destination_location_id)],
            k=random.randint(1, 3)
        )

        # Add origin as sequence 0
        route_locations.append(
            RouteLocation(
                route_id=route.id,
                location_id=route.origin_location_id,
                sequence=0
            )
        )

        # Add intermediate locations with increasing sequence
        for idx, loc in enumerate(intermediate_locations, start=1):
            route_locations.append(
                RouteLocation(
                    route_id=route.id,
                    location_id=loc.id,
                    sequence=idx
                )
            )

        # Add destination as last
        route_locations.append(
            RouteLocation(
                route_id=route.id,
                location_id=route.destination_location_id,
                sequence=len(intermediate_locations) + 1
            )
        )

    # Bulk save
    session.bulk_save_objects(route_locations)
    session.commit()

    print(f"Seeded {len(route_locations)} route-locations for {len(routes)} routes.")


    # Item category. Can we use List Interpretation?

    categories = [
        ItemCategory(
            name="Electronics",
            base_rate=1.5,
            description="Fragile items like phones, laptops"
        ),
        ItemCategory(
            name="Furniture",
            base_rate=2.0,
            description="Bulky items like sofas, tables"
        ),
        ItemCategory(
            name="Perishables",
            base_rate=2.5,
            description="Time-sensitive food and medicines"
        ),
        ItemCategory(
            name="Documents",
            base_rate=1.0,
            description="Letters, legal or business papers"
        ),
        ItemCategory(
            name="Clothing",
            base_rate=1.2,
            description="Apparel and accessories"
        ),
        ItemCategory(
            name="Machinery",
            base_rate=3.0,
            description="Industrial equipment and tools"
        ),
    ]

    # Add and commit
    session.bulk_save_objects(categories)
    session.commit()

    print(f"Seeded {len(categories)} item categories.")


    # ShipmentItem seeding

    # Step 1: Get existing shipments and categories
    shipments = session.query(Shipment).limit(10).all()
    categories = session.query(ItemCategory).all()

    # Step 2: Create shipment items
    shipment_items = []

    for shipment in shipments:
        for _ in range(random.randint(1, 3)):  # 1 to 3 items per shipment
            category = random.choice(categories)
            item = ShipmentItem(
                shipment_id=shipment.id,
                item_name=fake.word().capitalize(),
                description=fake.sentence(),
                weight=round(random.uniform(0.5, 20.0), 2),  # in kg
                quantity=random.randint(1, 10),
                value=random.randint(100, 5000),
                category_id=category.id
            )
            shipment_items.append(item)

    # Step 3: Save to DB
    session.bulk_save_objects(shipment_items)
    session.commit()

    print(f"Seeded {len(shipment_items)} shipment items.")



    # Step 1: Border Seeding (If Location table doesn't yet have any is_border=True)
    # Randomly mark a few locations as border locations (if not already done)
    border_candidates = session.query(Location).filter(Location.type.in_(['county', 'city'])).limit(5).all()

    for loc in border_candidates:
        loc.is_border = True

    session.commit()

    # Step 2: Border Seeding (Our Location table have some is_border=True)
    # Step I: Get border-flagged locations
    border_locations = session.query(Location).filter_by(is_border=True).all()

    # Step II: Create border entries
    borders = []

    for loc in border_locations:
        border = Border(
            location_id=loc.id,
            border_type=random.choice(list(BorderType)),
            checkpoint_name=f"{loc.name} Checkpoint",
            status=random.choice(list(BorderStatus)),
            notes=fake.sentence()
        )
        borders.append(border)

    # Step III: Save to DB
    session.bulk_save_objects(borders)
    session.commit()

    print(f"Seeded {len(borders)} borders for is_border=True locations.")



    # RouteTag Seeding
    # Sample tags and associated price factors
    sample_tags = [
        ("priority", 1.5),
        ("fragile", 1.2),
        ("bulk", 0.9),
        ("overnight", 2.0),
        ("standard", 1.0)
    ]

    # Step 1: Get all routes (or a subset if needed)
    routes = session.query(Route).all()

    route_tags = []

    for route in routes:
        # Optionally assign 1–2 tags per route
        num_tags = random.randint(1, 2)
        chosen_tags = [random.choice(sample_tags) for _ in range(num_tags)]

        for tag_name, factor in chosen_tags:
            tag = RouteTag(
                route_id=route.id,
                tag=tag_name,
                price_factor=factor
            )
            route_tags.append(tag)

    # Step 2: Save all tags
    session.bulk_save_objects(route_tags)
    session.commit()

    print(f"Seeded {len(route_tags)} route tags for {len(routes)} routes.")



    # DropLog Seeding
    # Step 1: Get all existing shipments
    shipments = session.query(Shipment).all()

    # Step 2: Create drop logs for each shipment
    drop_logs = []

    for shipment in shipments:
        # Optionally assign 1–3 drop logs per shipment
        num_logs = random.randint(1, 3)
        current_time = datetime.now()

        for i in range(num_logs):
            status = random.choice(list(DropLogStatus))
            location = fake.city()
            created_at = current_time - timedelta(days=random.randint(1, 10))

            drop_log = DropLog(
                shipment_id=shipment.id,
                status=status,
                location=location,
                created_at=created_at,
                updated_at=created_at if status == DropLogStatus.scheduled else datetime.now()
            )
            drop_logs.append(drop_log)

    # Step 3: Save to DB
    session.bulk_save_objects(drop_logs)
    session.commit()

    print(f"Seeded {len(drop_logs)} drop logs for {len(shipments)} shipments.")


    # Contact info table

    # Step 1: Get all existing shipments and users
    shipments = session.query(Shipment).all()
    info_providers = session.query(User).all()

    # Step 2: Create contact info for each shipment
    contact_infos = []

    for shipment in shipments:
        sender_name = fake.name()
        sender_phone = fake.phone_number()
        sender_address = fake.address()

        receiver_name = fake.name()
        receiver_phone = fake.phone_number()
        receiver_address = fake.address()

        info_provider = random.choice(info_providers)

        contact_info = ShipmentContactInfo(
            shipment_id=shipment.id,
            sender_name=sender_name,
            sender_phone=sender_phone,
            sender_address=sender_address,
            receiver_name=receiver_name,
            receiver_phone=receiver_phone,
            receiver_address=receiver_address,
            info_provider_id=info_provider.id
        )
        contact_infos.append(contact_info)

    # Step 3: Save to DB
    session.bulk_save_objects(contact_infos)
    session.commit()

    print(f"Seeded {len(contact_infos)} shipment contact info records for {len(shipments)} shipments.")





    # # Get sample origin and destination locations
    # locations = session.query(Location).limit(10).all()
    # route_groups = session.query(RouteGroup).all() # We need Location, RouteGroup, and ShippingCost entries (they're foreign key dependencies in Route model).

    # if len(locations) < 2:
    #     raise ValueError("Not enough locations to seed routes!")

    # routes = []

    # for _ in range(5):  # create 5 sample routes
    #     origin, destination = random.sample(locations, 2)

    #     # Optional route group
    #     group = random.choice(route_groups) if route_groups else None

    #     # First create Route without shipping_cost FK (circular)
    #     new_route = Route(
    #         origin=origin,
    #         destination=destination,
    #         scope=random.choice(list(BorderType)),
    #         route_group=group
    #     )

    #     session.add(new_route)
    #     session.commit()  # get route.id before adding ShippingCost

    #     # Now create ShippingCost and assign to the route
    #     cost = ShippingCost(
    #         route_id=new_route.id,
    #         cost_value=random.randint(500, 5000),
    #         start_date=datetime.utcnow(),
    #         end_date=datetime.utcnow() + timedelta(days=90),
    #         active=True
    #     )
    #     session.add(cost)
    #     session.commit()

    #     routes.append(new_route)

    # print(f"Seeded {len(routes)} routes with associated shipping costs.")




    # print("Seeded Location hierarchy successfully!")



    # freebies = []
    # for company in companies:
    #     for i in range(random.randint(1,5)):
    #         dev = random.choice(devs)
    #         if company not in dev.companies:
    #             dev.companies.append(company)
    #             session.add(dev)
    #             session.commit()
            
    #         freebie = Freebie(
    #             item_name=fake.unique.word(),
    #             value=random.randint(40, 400),
    #             company_id=company.id,
    #             dev_id=dev.id
    #         )

    #         freebies.append(freebie)

    # session.bulk_save_objects(freebies)
    # session.commit()

    session.close() # close session
