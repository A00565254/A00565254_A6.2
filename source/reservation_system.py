"""
A00565254
Guillermo Contreras Pedroza
Sistema de Reservación de Hoteles.
"""

import json
import os


class Hotel:
    """Clase para representar un Hotel."""
    def __init__(self, hotel_id, name, location, rooms):
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.rooms = rooms

    def to_dict(self):
        """Convierte objeto a diccionario."""
        return self.__dict__

    def __str__(self):
        """Representación en cadena para evitar R0903."""
        return f"Hotel: {self.name}"


class Customer:
    """Clase para representar un Cliente."""
    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email

    def to_dict(self):
        """Convierte objeto a diccionario."""
        return self.__dict__

    def __str__(self):
        """Representación en cadena para evitar R0903."""
        return f"Customer: {self.name}"


class Reservation:
    """Clase para representar una Reservación."""
    def __init__(self, res_id, cust_id, hotel_id):
        self.res_id = res_id
        self.cust_id = cust_id
        self.hotel_id = hotel_id

    def to_dict(self):
        """Convierte objeto a diccionario."""
        return self.__dict__

    def __str__(self):
        """Representación en cadena para evitar R0903."""
        return f"Res: {self.res_id}"


class HotelManager:
    """Clase para gestionar la persistencia y lógica de negocio."""

    def __init__(self):
        self.h_file = "hotels.json"
        self.c_file = "customers.json"
        self.r_file = "reservations.json"

    def _load(self, filename):
        """Carga datos directamente desde el nombre del archivo."""
        if not os.path.exists(filename):
            return {}
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError) as err:
            print(f"Error detectado en {filename}: {err}. Continuando...")
            return {}

    def _save(self, filename, data):
        """Guarda datos en el archivo especificado."""
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
        except IOError as err:
            print(f"Error al guardar {filename}: {err}")

    # --- Métodos de Hotel ---
    def create_hotel(self, h_id, name, loc, rooms):
        """Crea un hotel y lo guarda."""
        hotels = self._load(self.h_file)
        hotels[h_id] = Hotel(h_id, name, loc, rooms).to_dict()
        self._save(self.h_file, hotels)

    def delete_hotel(self, h_id):
        """Elimina un hotel."""
        hotels = self._load(self.h_file)
        if hotels.pop(h_id, None):
            self._save(self.h_file, hotels)

    def display_hotel(self, h_id):
        """Muestra información del hotel."""
        hotels = self._load(self.h_file)
        print(hotels.get(h_id, "Hotel no encontrado."))

    def modify_hotel(self, h_id, **kwargs):
        """Modifica datos del hotel."""
        hotels = self._load(self.h_file)
        if h_id in hotels:
            hotels[h_id].update(kwargs)
            self._save(self.h_file, hotels)

    # --- Métodos de Cliente ---
    def create_customer(self, c_id, name, email):
        """Crea un cliente."""
        customers = self._load(self.c_file)
        customers[c_id] = Customer(c_id, name, email).to_dict()
        self._save(self.c_file, customers)

    def delete_customer(self, c_id):
        """Elimina un cliente."""
        customers = self._load(self.c_file)
        if customers.pop(c_id, None):
            self._save(self.c_file, customers)

    def display_customer(self, c_id):
        """Muestra información del cliente."""
        customers = self._load(self.c_file)
        print(customers.get(c_id, "Cliente no encontrado."))

    def modify_customer(self, c_id, **kwargs):
        """Modifica datos del cliente."""
        customers = self._load(self.c_file)
        if c_id in customers:
            customers[c_id].update(kwargs)
            self._save(self.c_file, customers)

    # --- Métodos de Reservación ---
    def create_reservation(self, r_id, c_id, h_id):
        """Crea una reservación vinculando cliente y hotel."""
        reservations = self._load(self.r_file)
        reservations[r_id] = Reservation(r_id, c_id, h_id).to_dict()
        self._save(self.r_file, reservations)

    def cancel_reservation(self, r_id):
        """Cancela una reservación."""
        reservations = self._load(self.r_file)
        if reservations.pop(r_id, None):
            self._save(self.r_file, reservations)
