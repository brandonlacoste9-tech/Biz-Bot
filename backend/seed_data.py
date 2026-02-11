"""
Seed data script for development and testing
"""
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.models import Tenant, User, Booking, FAQ, LanguageEnum
from datetime import datetime, timedelta


def seed_data():
    db: Session = SessionLocal()
    
    try:
        # Check if data already exists
        existing_tenant = db.query(Tenant).first()
        if existing_tenant:
            print("Database already has data. Skipping seed.")
            return
        
        # Create demo tenants
        tenant1 = Tenant(
            name="Café Québécois",
            slug="cafe-quebecois",
            is_active=True
        )
        tenant2 = Tenant(
            name="Tech Solutions MTL",
            slug="tech-solutions-mtl",
            is_active=True
        )
        
        db.add(tenant1)
        db.add(tenant2)
        db.commit()
        db.refresh(tenant1)
        db.refresh(tenant2)
        
        print(f"Created tenants: {tenant1.name}, {tenant2.name}")
        
        # Create demo users
        user1 = User(
            tenant_id=tenant1.id,
            email="admin@cafe-quebecois.ca",
            full_name="Marie Tremblay",
            is_active=True,
            is_admin=True,
            preferred_language=LanguageEnum.FR_CA
        )
        user2 = User(
            tenant_id=tenant2.id,
            email="admin@techsolutions.ca",
            full_name="John Smith",
            is_active=True,
            is_admin=True,
            preferred_language=LanguageEnum.EN
        )
        user3 = User(
            tenant_id=tenant1.id,
            email="staff@cafe-quebecois.ca",
            full_name="Jean Dupont",
            is_active=True,
            is_admin=False,
            preferred_language=LanguageEnum.FR_CA
        )
        
        db.add_all([user1, user2, user3])
        db.commit()
        
        print(f"Created users: {user1.email}, {user2.email}, {user3.email}")
        
        # Create demo bookings
        booking1 = Booking(
            tenant_id=tenant1.id,
            customer_name="Sophie Martin",
            customer_email="sophie@example.com",
            customer_phone="+1-514-555-0100",
            service_type="Table Reservation",
            appointment_time=datetime.now() + timedelta(days=2, hours=18),
            status="confirmed",
            notes="Table for 4 people, near window"
        )
        booking2 = Booking(
            tenant_id=tenant2.id,
            customer_name="Robert Johnson",
            customer_email="robert@example.com",
            customer_phone="+1-514-555-0200",
            service_type="IT Consultation",
            appointment_time=datetime.now() + timedelta(days=3, hours=14),
            status="pending",
            notes="Initial consultation for cloud migration"
        )
        booking3 = Booking(
            tenant_id=tenant1.id,
            customer_name="Pierre Leblanc",
            customer_email="pierre@example.com",
            customer_phone="+1-514-555-0300",
            service_type="Private Event",
            appointment_time=datetime.now() + timedelta(days=7, hours=19),
            status="pending",
            notes="Birthday party for 10 people"
        )
        
        db.add_all([booking1, booking2, booking3])
        db.commit()
        
        print(f"Created {3} bookings")
        
        # Create demo FAQs
        faq1 = FAQ(
            tenant_id=tenant1.id,
            question_en="What are your opening hours?",
            answer_en="We are open Monday to Friday from 7 AM to 10 PM, and Saturday to Sunday from 8 AM to 11 PM.",
            question_fr="Quelles sont vos heures d'ouverture?",
            answer_fr="Nous sommes ouverts du lundi au vendredi de 7h à 22h, et le samedi et dimanche de 8h à 23h.",
            category="General",
            is_active=True
        )
        faq2 = FAQ(
            tenant_id=tenant1.id,
            question_en="Do you take reservations?",
            answer_en="Yes, we accept reservations for groups of 4 or more. You can book through our WhatsApp or call us.",
            question_fr="Acceptez-vous les réservations?",
            answer_fr="Oui, nous acceptons les réservations pour les groupes de 4 personnes ou plus. Vous pouvez réserver via WhatsApp ou nous appeler.",
            category="Reservations",
            is_active=True
        )
        faq3 = FAQ(
            tenant_id=tenant2.id,
            question_en="What services do you offer?",
            answer_en="We offer IT consulting, cloud migration, cybersecurity, and custom software development services.",
            question_fr="Quels services offrez-vous?",
            answer_fr="Nous offrons des services de consultation informatique, migration cloud, cybersécurité et développement de logiciels sur mesure.",
            category="Services",
            is_active=True
        )
        faq4 = FAQ(
            tenant_id=tenant2.id,
            question_en="How do I schedule a consultation?",
            answer_en="You can schedule a consultation by contacting us via WhatsApp or email. We typically respond within 24 hours.",
            question_fr="Comment puis-je planifier une consultation?",
            answer_fr="Vous pouvez planifier une consultation en nous contactant via WhatsApp ou par courriel. Nous répondons généralement dans les 24 heures.",
            category="General",
            is_active=True
        )
        
        db.add_all([faq1, faq2, faq3, faq4])
        db.commit()
        
        print(f"Created {4} FAQs")
        print("\nSeed data created successfully!")
        print("\nDemo credentials:")
        print("- Tenant 1 (Café Québécois): admin@cafe-quebecois.ca")
        print("- Tenant 2 (Tech Solutions MTL): admin@techsolutions.ca")
        print("\nUse the magic link authentication to login.")
        
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
