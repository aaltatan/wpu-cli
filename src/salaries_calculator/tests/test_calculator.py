import pytest
from unittest import TestCase

from ..controllers import Salary, select_variant


class TestCalculator(TestCase):
    def test_layers_tax(self):
        salary = Salary(amount=300_000)
        self.assertEqual(salary.tax, 1_500)
        self.assertEqual(salary.net_salary, 298_500)

        salary = Salary(amount=500_000)
        self.assertEqual(salary.tax, 16_500)
        self.assertEqual(salary.net_salary, 483_500)

        salary = Salary(amount=1_500_000)
        self.assertEqual(salary.tax, 144_500)
        self.assertEqual(salary.net_salary, 1_355_500)

        salary = Salary(amount=3_500_000)
        self.assertEqual(salary.tax, 444_500)
        self.assertEqual(salary.net_salary, 3_055_500)

        salary = Salary(amount=500_000)
        self.assertEqual(salary.tax, 16_500)
        self.assertEqual(salary.net_salary, 483_500)

    def test_social_security_below_minimum(self):
        with pytest.raises(ValueError):
            salary = Salary(
                amount=1_000_000, social_security=True, social_security_salary=100_000
            )
            self.assertEqual(salary.social_security_deduction, 10_000)

    def test_tax_layers_with_social_security(self):
        salary = Salary(
            amount=1_000_000, social_security=True, social_security_salary=279_000
        )
        self.assertEqual(salary.social_security_deduction, 19_531)
        self.assertEqual(salary.fixed_tax, 0)
        self.assertEqual(salary.compensations, 0)
        self.assertEqual(salary.tax, 69_000)
        self.assertEqual(salary.net_salary, 1_000_000 - 69_000 - 19_531)

        salary = Salary(
            amount=1_000_000,
            social_security=True,
            social_security_salary=279_000,
            as_net=True,
            compensations_rate=0.25,
        )
        self.assertEqual(salary.gross_salary, 796_100)
        self.assertEqual(salary.compensations, 263_200)
        self.assertEqual(salary.social_security_deduction, 19_531)
        self.assertEqual(salary.fixed_tax, 13_200)
        self.assertEqual(salary.tax, 43_900)
        self.assertEqual(
            salary.net_salary, 796_100 + 277_800 - 19_531 - 27_800 - 43_900
        )

    def test_gross_salary(self):
        salary = Salary(amount=1_000_000, as_net=True)
        self.assertEqual(salary.gross_salary, 1_082_200)
        self.assertEqual(salary.tax, 82_200)
        self.assertEqual(salary.net_salary, 1_000_000)

        salary = Salary(amount=555_000, as_net=True)
        self.assertEqual(salary.gross_salary, 578_600)
        self.assertEqual(salary.tax, 23_600)
        self.assertEqual(salary.net_salary, 555_000)

        salary = Salary(amount=1_555_000, as_net=True)
        self.assertEqual(salary.gross_salary, 1_734_700)
        self.assertEqual(salary.tax, 179_700)
        self.assertEqual(salary.net_salary, 1_555_000)

    def test_gross_salary_with_compensations(self):
        salary = Salary(amount=1_000_000, as_net=True, compensations_rate=0.25)
        self.assertEqual(salary.gross_salary, 796_100)
        self.assertEqual(salary.compensations, 263_200)
        self.assertEqual(salary.tax, 46_100)
        self.assertEqual(salary.fixed_tax, 13_200)

        salary = Salary(amount=2_000_000, as_net=True, compensations_rate=0.5)
        self.assertEqual(salary.gross_salary, 1_082_200)
        self.assertEqual(salary.compensations, 1_052_700)
        self.assertEqual(salary.tax, 82_200)
        self.assertEqual(salary.fixed_tax, 52_700)

        salary = Salary(amount=2_000_000, as_net=True)
        self.assertEqual(salary.gross_salary, 2_258_300)
        self.assertEqual(salary.compensations, 0)
        self.assertEqual(salary.tax, 258_300)
        self.assertEqual(salary.fixed_tax, 0)

    def test_select_variant(self):
        salary = select_variant(amount=9_000_000, compensations_rate=0.25, accuracy=100)
        self.assertEqual(salary.gross_salary, 7_634_700)
        self.assertEqual(salary.compensations, 2_557_900)
        self.assertEqual(salary.net_salary, 9_000_000)
