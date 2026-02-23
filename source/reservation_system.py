"""
A00565254
Guillermo Contreras Pedroza
Sistema de Gestión de Hoteles
Este módulo permite administrar Hoteles, Clientes y Reservaciones
con persistencia en archivos JSON. 
"""

import json
import os


class Hotel:
    """Representa un Hotel en el sistema."""

    def __init__(self, hotel_id, name, location, total_rooms):
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.total_rooms = total_rooms
        self.rooms_available = total_rooms

    def to_dict(self):
        """Convierte la instancia a diccionario para JSON."""
        return self.__dict__

    def __str__(self):
        """Representación en texto del hotel."""
        return f"Hotel {self.name} ({self.location})"

class Customer:
    """Representa un Cliente en el sistema."""

    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email

    def to_dict(self):
        """Convierte la instancia a diccionario para JSON."""
        return self.__dict__

    def __str__(self):
        """Representación en texto del Cliente o Customer."""
        return f"Customer {self.name} ({self.email})"

class Reservation:
    """Representa una Reservación vinculando Cliente y Hotel."""

    def __init__(self, reservation_id, customer_id, hotel_id):
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id

    def to_dict(self):
        """Convierte la instancia a diccionario para JSON."""
        return self.__dict__

    def __str__(self):
        """Representación en texto de la reservación"""
        return f"Reservación {self.reservation_id} ({self.customer_id, self.hotel_id})"


class HotelManager:
    """Clase encargada de la lógica de negocio y persistencia."""

    def __init__(self):
        self.files = {
            'hotels': 'hotels.json',
            'customers': 'customers.json',
            'reservations': 'reservations.json'
        }

    def _load_file(self, entity):
        """Carga datos desde el archivo correspondiente."""
        filename = self.files[entity]
        if not os.path.exists(filename):
            return {}
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError) as error:
            print(f"Error detectado en {filename}: {error}. Continuando...")
            return {}

    def _save_file(self, entity, data):
        """Guarda datos en el archivo correspondiente."""
        try:
            with open(self.files[entity], 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
        except IOError as error:
            print(f"Error al guardar {entity}: {error}")

    # --- Métodos de Hotel ---
    def create_hotel(self, h_id, name, loc, rooms):
        """Crea y almacena un nuevo hotel."""
        hotels = self._load_file('hotels')
        hotels[h_id] = Hotel(h_id, name, loc, rooms).to_dict()
        self._save_file('hotels', hotels)

    def delete_hotel(self, h_id):
        """Elimina un hotel por su ID."""
        hotels = self._load_file('hotels')
        if hotels.pop(h_id, None):
            self._save_file('hotels', hotels)
        else:
            print(f"Hotel {h_id} no encontrado.")

    def display_hotel(self, h_id):
        """Muestra información de un hotel."""
        hotels = self._load_file('hotels')
        print(hotels.get(h_id, "Hotel no encontrado."))

    def modify_hotel(self, h_id, **kwargs):
        """Modifica atributos específicos de un hotel."""
        hotels = self._load_file('hotels')
        if h_id in hotels:
            hotels[h_id].update(kwargs)
            self._save_file('hotels', hotels)

    # --- Métodos de Cliente ---
    def create_customer(self, c_id, name, email):
        """Crea y almacena un nuevo cliente."""
        customers = self._load_file('customers')
        customers[c_id] = Customer(c_id, name, email).to_dict()
        self._save_file('customers', customers)

    def delete_customer(self, c_id):
        """Elimina un cliente."""
        customers = self._load_file('customers')
        if customers.pop(c_id, None):
            self._save_file('customers', customers)

    def display_customer(self, customer_id):
        """
        Muestra la información de un cliente específico.
        Req 2.2.c: Display Customer Information.
        """
        customers = self._load_file('customers')
        customer = customers.get(customer_id)
        if customer:
            print(f"ID: {customer['customer_id']}")
            print(f"Nombre: {customer['name']}")
            print(f"Email: {customer['email']}")
        else:
            print(f"Error: El cliente con ID {customer_id} no existe.")

    def modify_customer(self, customer_id, **kwargs):
        """
        Modifica la información de un cliente existente.
        Req 2.2.d: Modify Customer Information.
        """
        customers = self._load_file('customers')
        if customer_id in customers:
            # Actualizamos solo los campos proporcionados en kwargs
            for key, value in kwargs.items():
                if key in customers[customer_id]:
                    customers[customer_id][key] = value

            self._save_file('customers', customers)
            print(f"Cliente {customer_id} actualizado exitosamente.")
        else:
            print(f"Error: No se pudo modificar. Cliente {customer_id} no encontrado.")

    # --- Métodos de Reservación ---
    def create_reservation(self, r_id, c_id, h_id):
        """Crea una reservación si hay disponibilidad."""
        hotels = self._load_file('hotels')
        customers = self._load_file('customers')
        reservations = self._load_file('reservations')

        if h_id in hotels and c_id in customers:
            if hotels[h_id]['rooms_available'] > 0:
                hotels[h_id]['rooms_available'] -= 1
                res = Reservation(r_id, c_id, h_id)
                reservations[r_id] = res.to_dict()
                self._save_file('hotels', hotels)
                self._save_file('reservations', reservations)
            else:
                print("No hay habitaciones disponibles.")
        else:
            print("ID de Cliente o Hotel inválido.")

    def cancel_reservation(self, r_id):
        """Cancela una reservación y libera la habitación."""
        reservations = self._load_file('reservations')
        hotels = self._load_file('hotels')

        if r_id in reservations:
            h_id = reservations[r_id]['hotel_id']
            hotels[h_id]['rooms_available'] += 1
            del reservations[r_id]
            self._save_file('hotels', hotels)
            self._save_file('reservations', reservations)
