import unittest

from src.models import CartItem
from src.pricing import PricingService, PricingError


class TestPricingService(unittest.TestCase):

    def setUp(self):
        self.pricing = PricingService()

    def test_subtotal_1(self):
        items = [
            CartItem("prod1", 1200, 2),
            CartItem("prod2", 800, 1)
        ]

        total = self.pricing.subtotal_cents(items)

        self.assertEqual(total, 3200)

    def test_cantidad_invalida(self):
        items = [CartItem("prod1", 1000, 0)]

        with self.assertRaises(PricingError):
            self.pricing.subtotal_cents(items)

    def test_precio_negativo(self):
        items = [CartItem("prod1", -500, 1)]

        with self.assertRaises(PricingError):
            self.pricing.subtotal_cents(items)

    def test_aplicar_cupon1(self):
        resultado = self.pricing.apply_coupon(10000, "SAVE10")

        self.assertEqual(resultado, 9000)

    def test_aplicar_cupon2(self):
        resultado = self.pricing.apply_coupon(7000, "CLP2000")

        self.assertEqual(resultado, 5000)

    def test_aplicar_cupon3(self):
        with self.assertRaises(PricingError):
            self.pricing.apply_coupon(5000, "DESCUENTO")

    def test_impuesto1(self):
        tax = self.pricing.tax_cents(10000, "CL")

        self.assertEqual(tax, 1900)

    def test_impuesto2(self):
        tax = self.pricing.tax_cents(10000, "US")

        self.assertEqual(tax, 0)

    def test_impuesto3(self):
        tax = self.pricing.tax_cents(10000, "EU")

        self.assertEqual(tax, 2100)

    def test_impuesto4(self):
        with self.assertRaises(PricingError):
            self.pricing.tax_cents(10000, "AR")

    def test_envio1(self):
        envio = self.pricing.shipping_cents(10000, "CL")

        self.assertEqual(envio, 2500)

    def test_envio2(self):
        envio = self.pricing.shipping_cents(20000, "CL")

        self.assertEqual(envio, 0)

    def test_envio3(self):
        envio = self.pricing.shipping_cents(10000, "US")

        self.assertEqual(envio, 5000)

    def test_envio4(self):
        with self.assertRaises(PricingError):
            self.pricing.shipping_cents(10000, "BR")
                                          
