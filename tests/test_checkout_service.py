import unittest
from unittest.mock import Mock

from src.models import CartItem
from src.checkout import CheckoutService, ChargeResult


class TestCheckoutService(unittest.TestCase):

    def setUp(self):

        self.pagos = Mock()
        self.email = Mock()
        self.fraud = Mock()
        self.repo = Mock()

        self.checkout = CheckoutService(
            payments=self.pagos,
            email=self.email,
            fraud=self.fraud,
            repo=self.repo
        )

    def test_checkout1_usuario_invalido(self):
        items = [CartItem("prod1", 1500, 1)]

        resultado = self.checkout.checkout(
            user_id="   ",
            items=items,
            payment_token="token123",
            country="CL"
        )

        self.assertEqual(resultado, "INVALID_USER")

    def test_checkout2_fraude(self):
        items = [CartItem("prod1", 1500, 1)]

        self.fraud.score.return_value = 85

        resultado = self.checkout.checkout(
            user_id="usuario1",
            items=items,
            payment_token="tok",
            country="CL"
        )

        self.assertEqual(resultado, "REJECTED_FRAUD")

    def test_checkout3_ok(self):
        items = [CartItem("prod1", 2000, 1)]

        self.fraud.score.return_value = 10
        self.pagos.charge.return_value = ChargeResult(True, "abc123")

        resultado = self.checkout.checkout(
            user_id="usuario1",
            items=items,
            payment_token="tok",
            country="CL"
        )

        self.assertTrue(resultado.startswith("OK:"))

    def test_pago1_fallido(self):
        items = [CartItem("prod1", 2000, 1)]

        self.fraud.score.return_value = 5
        self.pagos.charge.return_value = ChargeResult(False, reason="sin_fondos")

        resultado = self.checkout.checkout(
            user_id="usuario1",
            items=items,
            payment_token="tok",
            country="CL"
        )

        self.assertEqual(resultado, "PAYMENT_FAILED:sin_fondos")

    def test_pago2_charge_none(self):
        items = [CartItem("prod1", 2000, 1)]

        self.fraud.score.return_value = 5
        self.pagos.charge.return_value = ChargeResult(True, None)

        resultado = self.checkout.checkout(
            user_id="usuario1",
            items=items,
            payment_token="tok",
            country="CL"
        )

        self.assertTrue(resultado.startswith("OK:"))

    def test_checkout4_carrito_invalido(self):
        items = [CartItem("prod1", -100, 1)]

        resultado = self.checkout.checkout(
            user_id="usuario1",
            items=items,
            payment_token="tok",
            country="CL"
        )

        self.assertTrue(resultado.startswith("INVALID_CART"))