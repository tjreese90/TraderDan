from api.oanda_api import OandaApi
from models.trade_decision import TradeDecision
from bot.trade_risk_calculator import get_trade_units

def trade_is_open(pair, api: OandaApi):
    open_trades = api.get_open_trades()
   
    for ot in open_trades:
        if ot.instrument == pair:
            return ot
    return None

def place_trade(trade_decision: TradeDecision, api: OandaApi, log_message, log_error, trade_risk):

    ot = trade_is_open(trade_decision.pair, api)

    if ot is not None:
        log_message(f"Failed to place trade {trade_decision}, already open: {ot}")
        return

    trade_units = get_trade_units(api, trade_decision.pair, trade_decision.signal,trade_decision.loss, trade_risk, log_message)

    if trade_units is None:
        log_error(f"Error calculating trade units for {trade_decision}")
        return

    trade_id = api.place_trade(
       trade_decision.pair,
       trade_units,
       trade_decision.signal,
       trade_decision.sl,
       trade_decision.tp,
    )

    if trade_id is None:
        log_error(f"Error placing {trade_decision}")
        return

    log_message(f"Placed trade_id:{trade_id} for {trade_decision}")
