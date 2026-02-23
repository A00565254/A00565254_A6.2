"""
Script de pruebas intensivas para el Sistema de Hoteles.
Explora casos con manejo de errores.
"""

from reservation_system import HotelManager
import os

def run_stress_tests():
    """Ejecuta una serie de pruebas de estrés y validación."""
    manager = HotelManager()
    print("--- INICIANDO STRESS TEST ---")

    # 1. Prueba de Resiliencia: Archivo Corrupto (Req 3)
    print("\n[1] Probando archivo corrupto...")
    with open("hotels.json", "w", encoding="utf-8") as f:
        f.write("ESTO NO ES UN JSON VALIDO {,,}")
    
    # El programa debe mostrar el error en consola pero NO detenerse
    manager.display_hotel("H-999")
    manager.create_hotel("H2", "Hotel Resiliente", "Narnia", 5)
    print("Resultado: Sistema continuó operando tras error de archivo.")

    # 2. Prueba de Modificación Masiva
    print("\n[2] Modificando múltiples atributos a la vez...")
    manager.create_customer("C2", "Carlos", "carlos@test.com")
    manager.modify_customer(
        "C2", 
        name="Carlos Slim", 
        email="carlos.slim@newmail.com", 
        phone="555-1234" # Atributo nuevo no definido en __init__
    )
    manager.display_customer("C2")

    # 3. Prueba de Eliminación de Inexistentes
    print("\n[3] Eliminando IDs que no existen...")
    manager.delete_hotel("ID_FANTASMA")
    manager.delete_customer("C_FANTASMA")
    manager.cancel_reservation("R_FANTASMA")

    # 4. Prueba de Flujo Completo
    print("\n[4] Flujo de reservación completo...")
    manager.create_hotel("H3", "Hotel Playa", "Cancún", 50)
    manager.create_customer("C3", "Beatriz", "bea@test.com")
    manager.create_reservation("R3", "C3", "H3")
    
    print("\nDatos actuales en archivos:")
    manager.display_hotel("H3")
    manager.display_customer("C3")

    # 5. Limpieza Final (Opcional)
    print("\n--- PRUEBAS COMPLETADAS ---")

if __name__ == "__main__":
    run_stress_tests()