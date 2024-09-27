from dataclasses import dataclass, field
from typing import List


TURNS_PER_DAY = 8
INTEREST_RATE = 0.05


@dataclass
class Investment:
    amount: int
    days_left: int

    def accrue(self):
        self.amount += int(self.amount * INTEREST_RATE)
        self.days_left -= 1


def fmt_amount(amount: int) -> str:
    postfix = None
    power_vs_postfix = {
        9: "B",
        6: "M",
        3: "K",
    }
    for power, postfix in power_vs_postfix.items():
        threshold = 10**power
        if amount >= threshold:
            return f"{round(amount / threshold, 1)}{postfix}"
    return str(amount)


@dataclass
class Bank:
    investments: List[Investment] = field(default_factory=list)

    def add_investment(self, amount: int | float):
        if isinstance(amount, float):
            amount = int(amount)
        self.investments.append(Investment(amount, 2))

    def withdraw_daily(self) -> int:
        returns = self._receive_returns()
        self._remove_completed()
        self._acrue_all()
        return returns

    def _receive_returns(self) -> int:
        returns: int = 0
        for investment in self.investments:
            if investment.days_left == 0:
                returns += investment.amount
        return returns

    def _remove_completed(self):
        self.investments = [inv for inv in self.investments if inv.days_left != 0]

    def _acrue_all(self):
        for investment in self.investments:
            investment.accrue()


PROFIT_PER_TURN = 5_000_000
ASSUMED_PROFIT_PER_TURN_GROWTH = 0.05
NUMBER_OF_DAYS = 60
PER_TURN_INVESTMENT_PORTION = 0.5
REINVESTMENT_PORTION = 0.7


if __name__ == "__main__":
    bank = Bank()
    total_invested: int = 0
    total_returns: int = 0
    for day_index in range(NUMBER_OF_DAYS):
        PROFIT_PER_TURN += PROFIT_PER_TURN * ASSUMED_PROFIT_PER_TURN_GROWTH
        daily_returns = bank.withdraw_daily()

        reinvestment = int(daily_returns * REINVESTMENT_PORTION)
        bank.add_investment(reinvestment)
        investment_profit = daily_returns - reinvestment
        total_returns += investment_profit

        for _ in range(TURNS_PER_DAY):
            cash_to_invest = int(PROFIT_PER_TURN * PER_TURN_INVESTMENT_PORTION)
            total_invested += cash_to_invest
            bank.add_investment(cash_to_invest)

        if day_index == 0:
            continue
        print(
            f"""\
### DAY {day_index} ###
Profit from investments: {fmt_amount(investment_profit)}
reinvestment:            {fmt_amount(reinvestment)}
principal invested:      {fmt_amount(total_invested)}
total returns:           {fmt_amount(total_returns)}
"""
        )
