from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from logging import Logger
from typing import Any, Dict, List, Tuple

from ctlml_commons.entity.candle import Candle
from ctlml_commons.entity.focus.focus import Focus
from ctlml_commons.entity.lot import Lot
from ctlml_commons.entity.news import News
from ctlml_commons.entity.range_window import RangeWindow
from ctlml_commons.util.num_utils import float_to_percentage_str


@dataclass(frozen=True)
class PercentageFocus(Focus):
    """Percentage up/down based investment strategy."""

    """Percentage based per share to consider purchasing"""
    percentage_up: float

    """Percentage up per share total to decide to sell"""
    percentage_window: RangeWindow

    """If should sell at the end of day"""
    sell_at_end_of_day: bool

    def evaluate_buy(
            self, symbol: str, news: List[News], current_price: float, candles: Dict[str, Candle], logger: Logger
    ) -> Tuple[bool, str]:

        if not candles:
            return False, f"not enough data"

        open_price: float = candles[list(candles.keys())[-1]].open
        diff: float = (current_price - open_price) / open_price * 100
        message: str = f"buy per: {open_price} versus {current_price} = {float_to_percentage_str(diff)}"

        logger.debug(message)

        if (current_price - open_price) / open_price * 100 > self.percentage_up:
            return True, message

        return False, message

    def evaluate_sell(
            self, lot: Lot, news: List[News], current_price: float, candles: Dict[str, Candle], logger: Logger
    ) -> Tuple[bool, str]:
        threshold: float = (current_price - lot.purchase_price) / lot.purchase_price * 100

        if threshold > self.percentage_window.ceiling:
            message: str = f"""{lot.symbol} with purchase price {current_price} is {threshold} over {lot.purchase_price}.
                            Selling"""
            logger.debug(message)

            return True, message
        elif threshold < self.percentage_window.floor:
            message: str = f"""{lot.symbol} with purchase price {current_price} is {threshold} under {lot.purchase_price}.
                            Selling"""
            logger.debug(message)

            return True, message

        return False, f"Sell per: {lot.purchase_price} versus {current_price} = {float_to_percentage_str(threshold)}"

    def serialize(self) -> Dict[str, Any]:
        data = deepcopy(self.__dict__)
        data["percentage_window"] = self.percentage_window.serialize()
        data["focus_type"] = self.__class__.__name__
        return data

    @classmethod
    def deserialize(cls, input_data: Dict[str, Any]) -> PercentageFocus:
        data = deepcopy(input_data)

        del data["focus_type"]
        data["percentage_window"] = RangeWindow.deserialize(data["percentage_window"])

        return cls(**data)
