import json
import os


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class TaxRate(object):
    up_to: float
    rate: float

    def __init__(
            self,
            up_to: float,
            rate: float,
    ):
        self.up_to = up_to
        self.rate = rate


class TaxCalculator(object):
    _tax_rates: list[TaxRate]

    def __init__(
            self,
            file: str,
    ):
        self._tax_rates = []
        with open(file, 'r') as f:
            tax_file: dict[str, list[dict[str, float]]] = json.load(f)
            tax_rates = tax_file["tax_rates"]
            for tax_rate in tax_rates:
                self._tax_rates.append(TaxRate(
                    rate=float(tax_rate["percent"]/100.0),
                    up_to=tax_rate["up_to"],
                ))

    def calculate(self, income: float) -> float:
        total_tax = 0
        prev_up_to = 0
        for tax_rate in self._tax_rates:
            to_tax = min(income, tax_rate.up_to) - prev_up_to
            total_tax += to_tax * tax_rate.rate
            prev_up_to = tax_rate.up_to
            if min(income, tax_rate.up_to) == income:
                break
        return total_tax


class TotalTaxCalculator(object):
    _state_tax_calculator = TaxCalculator(os.path.join(ROOT_DIR, "resources", "ca-tax-rate.json"))
    _federal_tax_calculator = TaxCalculator(os.path.join(ROOT_DIR, "resources", "federal-tax-rate.json"))
    _medicare_tax_calculator = TaxCalculator(os.path.join(ROOT_DIR, "resources", "medicare-tax-rate.json"))
    _social_sec_tax_calculator = TaxCalculator(os.path.join(ROOT_DIR, "resources", "social-security-tax-rate.json"))

    def calculate(self, income: float) -> float:
        state_tax = self._state_tax_calculator.calculate(income)
        federal_tax = self._federal_tax_calculator.calculate(income)
        medicare_tax = self._medicare_tax_calculator.calculate(income)
        social_sec_tax = self._social_sec_tax_calculator.calculate(income)

        return state_tax + federal_tax + medicare_tax + social_sec_tax
