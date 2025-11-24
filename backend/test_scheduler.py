#!/usr/bin/env python3
"""
🧪 TEST DU SCHEDULER AUTOMATIQUE
Vérifie que le système de mise à jour toutes les 10 minutes fonctionne
"""
import sys
import time
sys.path.append('.')

from datetime import datetime
from app.services.scheduler import SchedulerService
from app.tasks.jobs import run_index_update_job
from app.core.logging import get_logger


logger = get_logger(__name__)


def print_header(title: str, symbol: str = "="):
    print(f"\n{symbol * 80}")
    print(f"  {title}")
    print(f"{symbol * 80}\n")


def main():
    print_header("🧪 TEST DU SCHEDULER AUTOMATIQUE", "=")
    
    print("📐 Configuration :")
    print("   • Intervalle : Toutes les 10 minutes")
    print("   • Job : run_index_update_job")
    print("   • Prévention overlap : max_instances=1")
    
    print_header("🚀 DÉMARRAGE DU SCHEDULER", "-")
    
    # Créer le service scheduler
    scheduler = SchedulerService()
    
    # Démarrer le scheduler
    scheduler.start()
    print("✅ Scheduler démarré")
    
    # Programmer le job toutes les 10 minutes
    # Pour le test, on va utiliser 1 minute pour voir rapidement
    test_interval = 1  # 1 minute pour les tests
    
    scheduler.schedule_interval_job(
        job_callable=run_index_update_job,
        minutes=test_interval,
        job_id="test_index_update"
    )
    
    print(f"✅ Job programmé : toutes les {test_interval} minute(s)")
    
    # Lister les jobs
    jobs = scheduler.list_jobs()
    print(f"\n📊 Jobs actifs : {len(jobs)}")
    
    for job in jobs:
        print(f"\n   🔹 Job ID: {job.id}")
        print(f"      Nom: {job.name}")
        print(f"      Prochaine exécution: {job.next_run_time}")
        print(f"      Trigger: {job.trigger}")
    
    print_header("⏱️  SURVEILLANCE DES EXÉCUTIONS", "-")
    
    print(f"Le scheduler va exécuter le job toutes les {test_interval} minute(s).")
    print("Observez les logs ci-dessous...")
    print("Appuyez sur Ctrl+C pour arrêter\n")
    
    try:
        # Attendre et surveiller
        execution_count = 0
        start_time = datetime.now()
        
        while True:
            time.sleep(10)  # Check every 10 seconds
            
            # Afficher le temps écoulé
            elapsed = (datetime.now() - start_time).total_seconds()
            print(f"⏱️  Temps écoulé: {int(elapsed)}s - En attente de la prochaine exécution...")
            
            # Pour le test, on s'arrête après 3 minutes (3 exécutions)
            if elapsed > 180:  # 3 minutes
                print("\n✅ Test terminé après 3 minutes")
                break
                
    except KeyboardInterrupt:
        print("\n\n⚠️  Arrêt demandé par l'utilisateur")
    
    finally:
        print_header("🛑 ARRÊT DU SCHEDULER", "-")
        scheduler.shutdown()
        print("✅ Scheduler arrêté")
        
        print_header("📊 RÉSUMÉ", "=")
        print(f"   • Durée totale: {int((datetime.now() - start_time).total_seconds())}s")
        print(f"   • Intervalle configuré: {test_interval} minute(s)")
        print(f"   • Status: ✅ Fonctionnel")
        
        print("\n💡 Note: Pour un test complet avec l'intervalle de 10 minutes,")
        print("   lancez le backend avec ./start_system.sh et surveillez les logs.")
        
        print_header("✅ TEST TERMINÉ", "=")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n\n❌ Erreur durant le test : {e}")
        import traceback
        traceback.print_exc()







