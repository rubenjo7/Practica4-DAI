import unittest
import os
import p4
from flask_testing import TestCase
import tempfile

class ejercicioTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, p4.app.config['DATABASE'] = tempfile.mkstemp()
        p4.app.config['TESTING'] = True
        self.app = p4.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(p4.app.config['DATABASE'])

    def test_home_status_code(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_name_status_code1(self):
        result = self.app.get('/comida')
        self.assertEqual(result.status_code, 200)

    def test_name_status_code2(self):
        result = self.app.get('/contacto')
        self.assertEqual(result.status_code, 200)

    def test_name_status_code3(self):
        result = self.app.get('/registro')
        self.assertEqual(result.status_code, 200)

    def test_name_status_code4(self):
        result = self.app.get('/insert')
        self.assertEqual(result.status_code, 200)

    def test_name_status_code5(self):
        result = self.app.get('/mod')
        self.assertEqual(result.status_code, 200)

if __name__ == '__main__':
    unittest.main()
