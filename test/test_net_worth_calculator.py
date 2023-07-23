from src.NetWorthCalculator import NetWorthCalculator


def test_net_worth_calculator() -> None:
    calculator = NetWorthCalculator(
        initial_investments=237000.0,
        initial_savings=20000.0,
        initial_income=314000.0,
        yearly_costs=53000.0,
        rate_of_return=0.07,
        rate_of_comp_growth=0.05,
        initial_age=25,
    )
    age, net_worth = calculator.calculate_net_worth()
    assert len(age) == len(net_worth)
    assert net_worth[0] == 257000.0
    assert net_worth[1] == 550290.0
    assert net_worth[2] == 880595.3

