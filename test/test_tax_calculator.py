from TaxCalculator import TaxCalculator, TotalTaxCalculator


def test_tax_calculator() -> None:
    file = "./resources/sample-tax-rate.json"
    calculator = TaxCalculator(file=file)
    total_tax = calculator.calculate(200000)
    assert total_tax == 31000.0


def test_total_tax_calculator() -> None:
    total_tax_calculator = TotalTaxCalculator()
    tax = total_tax_calculator.calculate(income=216333)
    assert tax == 78502.99100000001
