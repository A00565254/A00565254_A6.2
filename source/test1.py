from reservation_system import HotelManager

manager = HotelManager()

# 1. Probar Hoteles
manager.create_hotel("H1", "Gran Hotel", "CDMX", 100)
manager.modify_hotel("H1", location="Cancún")
manager.display_hotel("H1")

# 2. Probar Clientes
manager.create_customer("C1", "Ana Garcia", "ana@mail.com")
manager.display_customer("C1")
manager.modify_customer("C1", name="Ana G. Lopez")

# 3. Probar Reservaciones
manager.create_reservation("R1", "C1", "H1")
print("Reservación creada.")

# 3.5. Probar Reservaciones
manager.create_reservation("R2", "C2", "H1")
print("Reservación creada.")


# 4. Cancelar
manager.cancel_reservation("R1")
print("Reservación cancelada.")


