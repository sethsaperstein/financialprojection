from TaxCalculator import TotalTaxCalculator


class NetWorthCalculator(object):
    _initial_investments: float
    _initial_savings: float
    _initial_income: float
    _yearly_costs: float
    _rate_of_return: float
    _rate_of_comp_growth: float
    _initial_age: int

    _tax_calculator = TotalTaxCalculator()

    def __init__(
            self,
            initial_investments: float,
            initial_savings: float,
            initial_income: float,
            yearly_costs: float,
            rate_of_return: float,
            rate_of_comp_growth: float,
            initial_age: int,
    ):
        self._initial_investments = initial_investments
        self._initial_savings = initial_savings
        self._initial_income = initial_income
        self._yearly_costs = yearly_costs
        self._rate_of_return = rate_of_return
        self._rate_of_comp_growth = rate_of_comp_growth
        self._initial_age = initial_age

    def calculate_net_worth(self, end_age=90) -> tuple[list[int], list[float]]:
        age: list[int] = [t for t in range(self._initial_age, end_age)]
        net_worth: list[float] = [self._initial_investments + self._initial_savings]
        investments: list[float] = [self._initial_investments]
        income: list[float] = [self._initial_income]
        years_to_calculate: int = end_age - self._initial_age

        for t in range(1, years_to_calculate):
            gross_income_t = income[t - 1] * (1+self._rate_of_comp_growth)
            net_income_t = gross_income_t - self._tax_calculator.calculate(income=gross_income_t)
            investments_t = net_income_t \
                            - self._yearly_costs \
                            + (investments[t - 1] * (1 + self._rate_of_return))
            net_worth_t = investments_t + self._initial_savings

            income.append(gross_income_t)
            investments.append(investments_t)
            net_worth.append(net_worth_t)

        return age, net_worth
