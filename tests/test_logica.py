import unittest
from src.logica import EstadoGraficador, snap_to_grid

class TestSnapToGrid(unittest.TestCase):
    def test_snap_to_grid(self):
        # Prueba con grid_size 1
        self.assertEqual(snap_to_grid(2.3, 3.7, 1), (2, 4))
        # Prueba con grid_size 0.5
        self.assertEqual(snap_to_grid(2.3, 3.7, 0.5), (2.5, 3.5))
        # Prueba con grid_size 2
        self.assertEqual(snap_to_grid(3.9, 7.1, 2), (4, 8))

class TestEstadoGraficador(unittest.TestCase):
    def test_estado_inicial(self):
        estado = EstadoGraficador()
        self.assertEqual(estado.grid_size, 1)
        self.assertEqual(estado.puntos, {})
        self.assertEqual(estado.aristas, [])
        self.assertEqual(estado.matching, [])
        self.assertFalse(estado.media_arista)
        self.assertIsNone(estado.extremo1)
        self.assertIsNone(estado.extremo2)

if __name__ == "__main__":
    unittest.main()