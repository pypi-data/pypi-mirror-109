"""
@author  : MG
@Time    : 2021/4/15 15:55
@File    : signals.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""
from typing import Optional

from vnpy.trader.constant import Interval
from vnpy.trader.object import BarData
from vnpy_extra.backtest.cta_strategy.template import TargetPosAndPriceTemplate
from vnpy_extra.utils.enhancement import CtaSignal, BarGenerator

from vnpy_extra_tb.ams import TBArrayManager


class TBCtaSignal(CtaSignal):
    def __init__(self, array_size: int, strategy_obj, generate_daily=False, strict=False, **kwargs):
        super().__init__(array_size=array_size, strict=strict, **kwargs)
        self.am = TBArrayManager(size=array_size)
        self._generate_daily = generate_daily
        self.bg_daily: Optional[BarGenerator] = BarGenerator(
            window=1,
            on_bar=lambda _: _,
            on_window_bar=lambda bar: self.am_daily.update_bar(bar),
            interval=Interval.DAILY,
            strict=strict
        ) if generate_daily else None
        self.am_daily = TBArrayManager(size=array_size)
        self._strategy_obj: TargetPosAndPriceTemplate = strategy_obj
        # 对应 TB 中用于记录上一次进场到现在的数量
        self.bar_count_since_entry = 0
        # 对应 TB 中用于记录上一次出场到现在的数量
        self.bar_count_since_exit = 0
        # 一跳价格单位
        self.price_scale = self._strategy_obj.vt_symbol_price_tick
        # 记录上一状态时的 market_position
        self._market_position_at_last_window_bar = 0
        # 增加 信号价格
        self.signal_price = 0
        # 开仓价格，等于pos!=0时的 self.signal_price
        self.target_open_price = 0
        # 平仓价格，等于pos==0时的 self.signal_price
        self.target_close_price = 0

    @property
    def current_bar(self):
        return self.bg.last_finished_bar if self.bg.window_bar is None else self.bg.window_bar

    @property
    def current_bar_daily(self):
        return self.bg_daily.last_finished_bar if self.bg_daily.window_bar is None else self.bg_daily.window_bar

    @property
    def generate_daily(self) -> bool:
        return self._generate_daily

    def on_bar(self, bar: BarData):
        super().on_bar(bar)
        if self.bg_daily is not None:
            self.bg_daily.update_bar(bar)

    @property
    def market_position(self):
        return self._strategy_obj.pos

    def on_window(self, bar: BarData):
        super().on_window(bar)
        market_position = self.market_position
        if self._market_position_at_last_window_bar == 0 and market_position != 0:
            self.bar_count_since_entry = self.win_bar_count
        elif self._market_position_at_last_window_bar != 0 and market_position == 0:
            self.bar_count_since_exit = self.win_bar_count

        self._market_position_at_last_window_bar = market_position

    @property
    def bars_since_entry(self):
        if self.bar_count_since_entry == 0:
            return 0
        else:
            return self.win_bar_count - self.bar_count_since_entry

    @property
    def bars_since_exit(self):
        return self.win_bar_count - self.bar_count_since_exit if self.bar_count_since_exit != 0 else 0

    @property
    def entry_price(self):
        return self._strategy_obj.entry_price

    @property
    def exit_price(self):
        return self._strategy_obj.exit_price

    @property
    def open_daily_current(self) -> float:
        """当天的日级别信号(当前bar还未完成)"""
        if not self._generate_daily:
            raise AttributeError(f'generate_daily={self._generate_daily} 需要设置为 True')
        return self.current_bar_daily.open_price

    @property
    def high_daily_current(self) -> float:
        """当天的日级别信号(当前bar还未完成)"""
        if not self._generate_daily:
            raise AttributeError(f'generate_daily={self._generate_daily} 需要设置为 True')
        return self.current_bar_daily.high_price

    @property
    def low_daily_current(self) -> float:
        """当天的日级别信号(当前bar还未完成)"""
        if not self._generate_daily:
            raise AttributeError(f'generate_daily={self._generate_daily} 需要设置为 True')
        return self.current_bar_daily.low_price

    @property
    def close_daily_current(self) -> float:
        """当天的日级别信号(当前bar还未完成)"""
        if not self._generate_daily:
            raise AttributeError(f'generate_daily={self._generate_daily} 需要设置为 True')
        return self.current_bar_daily.close_price

    @property
    def volume_daily_current(self) -> float:
        """当天的日级别信号(当前bar还未完成)"""
        if not self._generate_daily:
            raise AttributeError(f'generate_daily={self._generate_daily} 需要设置为 True')
        return self.current_bar_daily.volume

    @property
    def open_daily_array(self):
        return self.am_daily.open_array

    @property
    def high_daily_array(self):
        return self.am_daily.high_array

    @property
    def low_daily_array(self):
        return self.am_daily.low_array

    @property
    def close_daily_array(self):
        return self.am_daily.close_array

    @property
    def volume_daily_array(self):
        return self.am_daily.volume_array

    @property
    def open_current(self):
        return self.current_bar.open_price

    @property
    def high_current(self):
        return self.current_bar.high_price

    @property
    def low_current(self):
        return self.current_bar.low_price

    @property
    def close_current(self):
        return self.current_bar.close_price

    @property
    def volume_current(self):
        return self.current_bar.volume

    @property
    def open(self):
        return self.am.open_array[-1]

    @property
    def high(self):
        return self.am.high_array[-1]

    @property
    def low(self):
        return self.am.low_array[-1]

    @property
    def close(self):
        return self.am.close_array[-1]

    @property
    def volume(self):
        return self.am.volume_array[-1]

    @property
    def open_array(self):
        return self.am.open_array

    @property
    def high_array(self):
        return self.am.high_array

    @property
    def low_array(self):
        return self.am.low_array

    @property
    def close_array(self):
        return self.am.close_array

    @property
    def volume_array(self):
        return self.am.volume_array

    def get_signal_pos(self):
        return super().get_signal_pos(), self.signal_price

    def set_signal_pos(self, pos, price=None):
        super().set_signal_pos(pos)
        self.signal_price = self.win_bar.close_price if price is None else price
        if pos == 0:
            self.target_close_price = self.signal_price
        else:
            self.target_open_price = self.signal_price
