"""
Seed data script for development
Run with: python -m app.utils.seed_data
"""
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models import Base, Tenant, User, Booking, FAQItem
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_seed_data():
    """Create seed data for development"""
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_tenant = db.query(Tenant).first()
        if existing_tenant:
            logger.info("Seed data already exists. Skipping...")
            return
        
        # Create tenant 1
        tenant1 = Tenant(
            name="Café Le Québécois",
            slug="cafe-le-quebecois",
            email="contact@cafe-quebecois.ca",
            phone="+15141234567",
            settings={
                "business_hours": "8:00-18:00",
                "timezone": "America/Montreal"
            }
        )
        db.add(tenant1)
        db.flush()
        
        # Create tenant 2
        tenant2 = Tenant(
            name="Clinique Santé Plus",
            slug="clinique-sante-plus",
            email="info@sante-plus.ca",
            phone="+15149876543",
            settings={
                "business_hours": "9:00-17:00",
                "timezone": "America/Montreal"
            }
        )
        db.add(tenant2)
        db.flush()
        
        # Create users for tenant 1
        user1 = User(
            tenant_id=tenant1.id,
            email="admin@cafe-quebecois.ca",
            full_name="Marie Tremblay",
            phone="+15141234567",
            is_admin=True,
            language="fr"
        )
        db.add(user1)
        
        user2 = User(
            tenant_id=tenant1.id,
            email="manager@cafe-quebecois.ca",
            full_name="Jean Dupont",
            phone="+15141234568",
            is_admin=False,
            language="fr"
        )
        db.add(user2)
        
        # Create users for tenant 2
        user3 = User(
            tenant_id=tenant2.id,
            email="admin@sante-plus.ca",
            full_name="Dr. Sophie Martin",
            phone="+15149876543",
            is_admin=True,
            language="fr"
        )
        db.add(user3)
        
        user4 = User(
            tenant_id=tenant2.id,
            email="receptionist@sante-plus.ca",
            full_name="Alex Johnson",
            phone="+15149876544",
            is_admin=False,
            language="en"
        )
        db.add(user4)
        
        # Create sample bookings for tenant 1
        booking1 = Booking(
            tenant_id=tenant1.id,
            customer_name="Pierre Lavoie",
            customer_email="pierre.lavoie@example.com",
            customer_phone="+15145551234",
            service_type="Table Reservation",
            appointment_date=datetime.utcnow() + timedelta(days=2),
            status="confirmed",
            notes="Table for 4 people",
            source="whatsapp"
        )
        db.add(booking1)
        
        booking2 = Booking(
            tenant_id=tenant1.id,
            customer_name="Anne Côté",
            customer_email="anne.cote@example.com",
            customer_phone="+15145555678",
            service_type="Catering Order",
            appointment_date=datetime.utcnow() + timedelta(days=5),
            status="pending",
            notes="Corporate event - 20 people",
            source="web"
        )
        db.add(booking2)
        
        # Create sample bookings for tenant 2
        booking3 = Booking(
            tenant_id=tenant2.id,
            customer_name="Michel Gagnon",
            customer_email="michel.gagnon@example.com",
            customer_phone="+15145559876",
            service_type="Medical Consultation",
            appointment_date=datetime.utcnow() + timedelta(days=1),
            status="confirmed",
            notes="Annual checkup",
            source="sms"
        )
        db.add(booking3)
        
        # Create FAQ items for tenant 1
        faq1 = FAQItem(
            tenant_id=tenant1.id,
            question_en="What are your opening hours?",
            question_fr="Quelles sont vos heures d'ouverture?",
            answer_en="We are open Monday to Friday from 8:00 AM to 6:00 PM.",
            answer_fr="Nous sommes ouverts du lundi au vendredi de 8h00 à 18h00.",
            keywords=["hours", "heures", "open", "ouvert"],
            order=1
        )
        db.add(faq1)
        
        faq2 = FAQItem(
            tenant_id=tenant1.id,
            question_en="Do you offer catering services?",
            question_fr="Offrez-vous des services de traiteur?",
            answer_en="Yes! We offer catering for events of all sizes. Contact us for a quote.",
            answer_fr="Oui! Nous offrons des services de traiteur pour événements de toutes tailles. Contactez-nous pour un devis.",
            keywords=["catering", "traiteur", "event", "événement"],
            order=2
        )
        db.add(faq2)
        
        faq3 = FAQItem(
            tenant_id=tenant1.id,
            question_en="Do you have vegetarian options?",
            question_fr="Avez-vous des options végétariennes?",
            answer_en="Absolutely! We have a variety of vegetarian and vegan options on our menu.",
            answer_fr="Absolument! Nous avons une variété d'options végétariennes et véganes sur notre menu.",
            keywords=["vegetarian", "végétarien", "vegan", "végan", "menu"],
            order=3
        )
        db.add(faq3)
        
        # Create FAQ items for tenant 2
        faq4 = FAQItem(
            tenant_id=tenant2.id,
            question_en="How do I book an appointment?",
            question_fr="Comment puis-je prendre rendez-vous?",
            answer_en="You can book online through our website or call us at +1-514-987-6543.",
            answer_fr="Vous pouvez réserver en ligne sur notre site web ou nous appeler au +1-514-987-6543.",
            keywords=["appointment", "rendez-vous", "book", "réserver"],
            order=1
        )
        db.add(faq4)
        
        faq5 = FAQItem(
            tenant_id=tenant2.id,
            question_en="Do you accept insurance?",
            question_fr="Acceptez-vous les assurances?",
            answer_en="Yes, we accept most major insurance plans. Please bring your insurance card.",
            answer_fr="Oui, nous acceptons la plupart des principales assurances. Veuillez apporter votre carte d'assurance.",
            keywords=["insurance", "assurance", "payment", "paiement"],
            order=2
        )
        db.add(faq5)
        
        db.commit()
        logger.info("✅ Seed data created successfully!")
        logger.info("\nTest Users:")
        logger.info("  Tenant 1 (Café Le Québécois):")
        logger.info("    - admin@cafe-quebecois.ca (Admin)")
        logger.info("    - manager@cafe-quebecois.ca (Manager)")
        logger.info("  Tenant 2 (Clinique Santé Plus):")
        logger.info("    - admin@sante-plus.ca (Admin)")
        logger.info("    - receptionist@sante-plus.ca (Receptionist)")
        
    except Exception as e:
        logger.error(f"Error creating seed data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_seed_data()
