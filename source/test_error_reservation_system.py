"""
Pruebas de error para el Sistema de Reservaciones.
Enfocado en casos de borde y datos inválidos.
"""

import unittest
import os
import json
from reservation_system import HotelManager


class TestReservationErrors(unittest.TestCase):
    """Pruebas para validar el manejo de errores y datos inexistentes."""

    def setUp(self):
        """Prepara el entorno limpiando archivos previos."""
        self.manager = HotelManager()
        self.files = ["hotels.json", "customers.json", "reservations.json"]
        for file in self.files:
            if os.path.exists(file):
                os.remove(file)

    def test_modify_non_existent_hotel(self):
        """Intenta modificar un hotel que no existe."""
        # No debería lanzar excepción, solo imprimir mensaje en consola
        self.manager.modify_hotel("999", name="Hotel Fantasma")
        data = self.manager._load("hotels.json")
        self.assertEqual(data, {})

    def test_delete_non_existent_customer(self):
        """Intenta eliminar un cliente que no existe."""
        # El sistema debe manejarlo sin interrumpir la ejecución
        self.manager.delete_customer("C-MISSING")
        data = self.manager._load("customers.json")
        self.assertEqual(data, {})

    def test_cancel_non_existent_reservation(self):
        """Intenta cancelar una reservación que no existe."""
        self.manager.cancel_reservation("R-NONE")
        data = self.manager._load("reservations.json")
        self.assertEqual(data, {})

    def test_corrupt_json_file(self):
        """Simula un archivo corrupto para probar el Req 3."""
        filename = "hotels.json"
        with open(filename, "w", encoding="utf-8") as file:
            file.write("Esto no es un JSON { {")
        
        # _load debe atrapar el error y retornar dict vacío
        data = self.manager._load(filename)
        self.assertEqual(data, {})

    def test_read_permission_error(self):
        """Simula un error de IO (archivo bloqueado o sin permisos)."""
        filename = "customers.json"
        # Creamos un directorio con el mismo nombre para forzar error de lectura
        os.mkdir(filename)
        
        try:
            data = self.manager._load(filename)
            self.assertEqual(data, {})
        finally:
            # Limpieza para no afectar otros tests
            os.rmdir(filename)

    def test_display_non_existent_entities(self):
        """Prueba la visualización de datos cuando los IDs no existen."""
        # Estos métodos imprimen "No encontrado", no deben fallar
        self.manager.display_hotel("H-NULL")
        self.manager.display_customer("C-NULL")

    def test_reservation_with_empty_ids(self):
        """Prueba la creación de reservación con strings vacíos."""
        self.manager.create_reservation("", "", "")
        data = self.manager._load("reservations.json")
        self.assertIn("", data)


if __name__ == "__main__":
    unittest.main()