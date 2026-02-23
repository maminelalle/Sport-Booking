"""
Script pour créer des réservations et paiements de test
"""
import os
import django
import sys
from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP
from django.utils import timezone

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sportsbooking.settings')
django.setup()

from apps.auth_app.models import CustomUser
from apps.courts.models import Court
from apps.reservations.models import Reservation
from apps.payments.models import Payment

def create_test_reservations():
    """Créer des réservations et paiements de test"""
    
    # Récupérer un utilisateur client
    try:
        client = CustomUser.objects.filter(email='client@sportbooking.com').first()
        if not client:
            # Créer un client si nécessaire
            from apps.auth_app.models import Role
            client_role = Role.objects.get(name='CLIENT')
            client = CustomUser.objects.create_user(
                email='client@sportbooking.com',
                username='client@sportbooking.com',
                password='client123456',
                first_name='Client',
                last_name='Test',
                phone='+22243567890',
                role=client_role
            )
            print("✓ Client créé")
    except Exception as e:
        print(f"Erreur lors de la récupération du client: {e}")
        return
    
    # Récupérer des terrains
    courts = Court.objects.all()[:5]
    
    if not courts:
        print("❌ Aucun terrain trouvé dans la base de données")
        return
    
    print(f"\n📊 Création de réservations pour: {client.email}")
    print(f"📍 Nombre de terrains disponibles: {courts.count()}\n")
    
    # Supprimer les anciennes réservations de test
    old_count = Reservation.objects.filter(user=client).count()
    if old_count > 0:
        Reservation.objects.filter(user=client).delete()
        print(f"🗑️  Supprimé {old_count} anciennes réservations\n")
    
    reservations_created = []
    today = timezone.now()
    
    # Scénario 1: Réservation à venir (demain)
    court1 = courts[0]
    start_time1 = today + timedelta(days=1)
    start_time1 = start_time1.replace(hour=10, minute=0, second=0, microsecond=0)
    end_time1 = start_time1 + timedelta(hours=2)
    duration1 = 2
    total1 = Decimal(court1.price_per_hour * duration1)
    
    reservation1 = Reservation.objects.create(
        user=client,
        court=court1,
        start_datetime=start_time1,
        end_datetime=end_time1,
        price_per_hour=court1.price_per_hour,
        total_amount=total1,
        status='CONFIRMED',
        notes='Réservation pour entraînement équipe'
    )
    
    payment1 = Payment.objects.create(
        reservation=reservation1,
        amount=total1 * Decimal('1.1'),  # + 10% frais de service
        method='CARD',
        status='SUCCESS',
        transaction_reference=f'TXN{reservation1.id}001',
        stripe_payment_intent_id=f'pi_test_{reservation1.id}_001'
    )
    
    reservations_created.append(reservation1)
    print(f"✓ Réservation 1: {court1.name} - Demain 10h-12h - CONFIRMED")
    print(f"  💳 Paiement: {payment1.amount} MRU - SUCCESS\n")
    
    # Scénario 2: Réservation à venir (dans 3 jours)
    if courts.count() > 1:
        court2 = courts[1]
        start_time2 = today + timedelta(days=3)
        start_time2 = start_time2.replace(hour=14, minute=0, second=0, microsecond=0)
        end_time2 = start_time2 + timedelta(hours=1)
        duration2 = 1
        total2 = Decimal(court2.price_per_hour * duration2)
        
        reservation2 = Reservation.objects.create(
            user=client,
            court=court2,
            start_datetime=start_time2,
            end_datetime=end_time2,
            price_per_hour=court2.price_per_hour,
            total_amount=total2,
            status='CONFIRMED',
            notes='Match amical'
        )
        
        payment2 = Payment.objects.create(
            reservation=reservation2,
            amount=total2 * Decimal('1.1'),
            method='CARD',
            status='SUCCESS',
            transaction_reference=f'TXN{reservation2.id}002',
            stripe_payment_intent_id=f'pi_test_{reservation2.id}_002'
        )
        
        reservations_created.append(reservation2)
        print(f"✓ Réservation 2: {court2.name} - Dans 3 jours 14h-15h - CONFIRMED")
        print(f"  💳 Paiement: {payment2.amount} MRU - SUCCESS\n")
    
    # Scénario 3: Réservation passée (il y a 5 jours)
    if courts.count() > 2:
        court3 = courts[2]
        start_time3 = today - timedelta(days=5)
        start_time3 = start_time3.replace(hour=16, minute=0, second=0, microsecond=0)
        end_time3 = start_time3 + timedelta(hours=2)
        duration3 = 2
        total3 = Decimal(court3.price_per_hour * duration3)
        
        reservation3 = Reservation.objects.create(
            user=client,
            court=court3,
            start_datetime=start_time3,
            end_datetime=end_time3,
            price_per_hour=court3.price_per_hour,
            total_amount=total3,
            status='COMPLETED',
            notes='Tournoi mensuel'
        )
        
        payment3 = Payment.objects.create(
            reservation=reservation3,
            amount=total3 * Decimal('1.1'),
            method='CARD',
            status='SUCCESS',
            transaction_reference=f'TXN{reservation3.id}003',
            stripe_payment_intent_id=f'pi_test_{reservation3.id}_003'
        )
        
        reservations_created.append(reservation3)
        print(f"✓ Réservation 3: {court3.name} - Il y a 5 jours 16h-18h - COMPLETED")
        print(f"  💳 Paiement: {payment3.amount} MRU - SUCCESS\n")
    
    # Scénario 4: Réservation passée (il y a 2 jours)
    if courts.count() > 3:
        court4 = courts[3]
        start_time4 = today - timedelta(days=2)
        start_time4 = start_time4.replace(hour=9, minute=0, second=0, microsecond=0)
        end_time4 = start_time4 + timedelta(hours=1)
        duration4 = 1
        total4 = Decimal(court4.price_per_hour * duration4)
        
        reservation4 = Reservation.objects.create(
            user=client,
            court=court4,
            start_datetime=start_time4,
            end_datetime=end_time4,
            price_per_hour=court4.price_per_hour,
            total_amount=total4,
            status='COMPLETED',
            notes='Session individuelle'
        )
        
        payment4 = Payment.objects.create(
            reservation=reservation4,
            amount=total4 * Decimal('1.1'),
            method='TRANSFER',
            status='SUCCESS',
            transaction_reference=f'TXN{reservation4.id}004',
            stripe_payment_intent_id=f'pi_test_{reservation4.id}_004'
        )
        
        reservations_created.append(reservation4)
        print(f"✓ Réservation 4: {court4.name} - Il y a 2 jours 9h-10h - COMPLETED")
        print(f"  💳 Paiement: {payment4.amount} MRU (TRANSFER) - SUCCESS\n")
    
    # Scénario 5: Réservation annulée (il y a 7 jours)
    if courts.count() > 4:
        court5 = courts[4]
        start_time5 = today - timedelta(days=7)
        start_time5 = start_time5.replace(hour=18, minute=0, second=0, microsecond=0)
        end_time5 = start_time5 + timedelta(hours=2)
        duration5 = 2
        total5 = Decimal(court5.price_per_hour * duration5)
        
        reservation5 = Reservation.objects.create(
            user=client,
            court=court5,
            start_datetime=start_time5,
            end_datetime=end_time5,
            price_per_hour=court5.price_per_hour,
            total_amount=total5,
            status='CANCELLED',
            notes='Annulé - Mauvais temps'
        )
        
        payment5 = Payment.objects.create(
            reservation=reservation5,
            amount=total5 * Decimal('1.1'),
            method='CARD',
            status='REFUNDED',
            transaction_reference=f'TXN{reservation5.id}005',
            stripe_payment_intent_id=f'pi_test_{reservation5.id}_005'
        )
        
        reservations_created.append(reservation5)
        print(f"✓ Réservation 5: {court5.name} - Il y a 7 jours 18h-20h - CANCELLED")
        print(f"  💳 Paiement: {payment5.amount} MRU - REFUNDED\n")
    
    # Scénario 6: Réservation en attente de paiement (dans 5 jours)
    if courts.count() > 0:
        court6 = courts[0]
        start_time6 = today + timedelta(days=5)
        start_time6 = start_time6.replace(hour=15, minute=0, second=0, microsecond=0)
        end_time6 = start_time6 + timedelta(hours=1, minutes=30)
        duration6 = Decimal('1.5')
        total6 = (court6.price_per_hour * duration6).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        reservation6 = Reservation.objects.create(
            user=client,
            court=court6,
            start_datetime=start_time6,
            end_datetime=end_time6,
            price_per_hour=court6.price_per_hour,
            total_amount=total6,
            status='PENDING',
            notes='En attente de confirmation paiement'
        )
        
        payment6 = Payment.objects.create(
            reservation=reservation6,
            amount=total6 * Decimal('1.1'),
            method='CARD',
            status='PENDING',
            transaction_reference=f'TXN{reservation6.id}006',
            stripe_payment_intent_id=f'pi_test_{reservation6.id}_006'
        )
        
        reservations_created.append(reservation6)
        print(f"✓ Réservation 6: {court6.name} - Dans 5 jours 15h-16h30 - PENDING")
        print(f"  💳 Paiement: {payment6.amount} MRU - PENDING\n")
    
    print(f"\n✅ {len(reservations_created)} réservations créées avec succès!")
    print(f"\n📋 RÉSUMÉ:")
    print(f"   • {Reservation.objects.filter(user=client, status='CONFIRMED').count()} réservations CONFIRMED")
    print(f"   • {Reservation.objects.filter(user=client, status='COMPLETED').count()} réservations COMPLETED")
    print(f"   • {Reservation.objects.filter(user=client, status='CANCELLED').count()} réservations CANCELLED")
    print(f"   • {Reservation.objects.filter(user=client, status='PENDING').count()} réservations PENDING")
    
    total_payments = Payment.objects.filter(reservation__user=client).count()
    total_amount = sum(p.amount for p in Payment.objects.filter(reservation__user=client, status='SUCCESS'))
    print(f"\n💰 PAIEMENTS:")
    print(f"   • {total_payments} paiements créés")
    print(f"   • {total_amount} MRU dépensés (completés)")
    
    print(f"\n🔐 COMPTE TEST:")
    print(f"   Email: {client.email}")
    print(f"   Password: client123456")
    print(f"\n🌐 ACCÈS:")
    print(f"   Frontend: http://localhost:3000")
    print(f"   Login: http://localhost:3000/login")
    print(f"   Réservations: http://localhost:3000/my-reservations")
    print(f"   Paiements: http://localhost:3000/payments")
    print(f"   Analytics: http://localhost:3000/analytics")

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  CRÉATION DE DONNÉES DE TEST - RÉSERVATIONS & PAIEMENTS")
    print("="*60 + "\n")
    
    create_test_reservations()
    
    print("\n" + "="*60)
    print("  ✨ DONNÉES DE TEST CRÉÉES AVEC SUCCÈS!")
    print("="*60 + "\n")
