"""
Unit tests for Hotel Management System.
Ensures >85% code coverage.
"""

import unittest
import os
import json
from reservation_system import HotelManager


class TestHotelManager(unittest.TestCase):
    """Test suite for HotelManager class."""

    def setUp(self):
        """Prepara el entorno de pruebas."""
        self.manager = HotelManager()
        # Nombres de archivos temporales para pruebas
        self.files = ['hotels.json', 'customers.json', 'reservations.json']
        self._cleanup()

    def tearDown(self):
        """Limpia los archivos después de las pruebas."""
        self._cleanup()

    def _cleanup(self):
        """Elimina archivos JSON si existen."""
        for file in self.files:
            if os.path.exists(file):
                os.remove(file)

    def test_create_and_display_hotel(self):
        """Prueba la creación y visualización de un hotel."""
        self.manager.create_hotel("H1", "Test Hotel", "City A", 10)
        # Capturamos la lógica de carga para verificar contenido
        data = self.manager._load("hotels.json")
        self.assertIn("H1", data)
        self.assertEqual(data["H1"]["name"], "Test Hotel")

    def test_modify_hotel(self):
        """Prueba la modificación de datos de un hotel."""
        self.manager.create_hotel("H1", "Old Name", "City A", 10)
        self.manager.modify_hotel("H1", name="New Name")
        data = self.manager._load("hotels.json")
        self.assertEqual(data["H1"]["name"], "New Name")

    def test_delete_hotel(self):
        """Prueba la eliminación de un hotel."""
        self.manager.create_hotel("H1", "Hotel", "City", 5)
        self.manager.delete_hotel("H1")
        data = self.manager._load("hotels.json")
        self.assertNotIn("H1", data)

    def test_customer_operations(self):
        """Prueba el ciclo de vida del cliente."""
        self.manager.create_customer("C1", "User", "user@test.com")
        self.manager.modify_customer("C1", name="Updated User")
        data = self.manager._load("customers.json")
        self.assertEqual(data["C1"]["name"], "Updated User")
        self.manager.delete_customer("C1")
        data = self.manager._load("customers.json")
        self.assertNotIn("C1", data)

    def test_reservation_lifecycle(self):
        """Prueba creación y cancelación de reservación."""
        self.manager.create_reservation("R1", "C1", "H1")
        res_data = self.manager._load("reservations.json")
        self.assertIn("R1", res_data)
        self.manager.cancel_reservation("R1")
        res_data = self.manager._load("reservations.json")
        self.assertNotIn("R1", res_data)

    def test_invalid_file_handling(self):
        """Manejo de archivos corruptos."""
        # Creamos un archivo con JSON inválido
        with open("hotels.json", "w", encoding="utf-8") as f:
            f.write("{ invalid json ...")
        
        # El sistema debe detectar el error, imprimirlo y devolver un dict vacío
        data = self.manager._load("hotels.json")
        self.assertEqual(data, {})


if __name__ == "__main__":
    unittest.main()