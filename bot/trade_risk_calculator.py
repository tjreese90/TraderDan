from api.oanda_api import OandaApi
import constants.defs as defs
from instrumentCollection.instrument_collection import InstrumentCollection

def get_trade_units(api: OandaApi, pair, signal, loss, trade_risk, log_message):
    # Fetch prices
    prices = api.get_prices([pair])

    if not prices:
        log_message("get_trade_units() Price is none", pair)
        return False

    # Extract the correct price for the pair
    price = next((p for p in prices if p.instrument == pair), None)
    
    if not price:
        log_message("get_trade_units() price is none. Check prices", pair)
        return False

    log_message(f"get_trade_units() price {price}", pair)

    # Determine conversion based on signal
    if signal == defs.SELL:
        conv = price.sell_conv
    elif signal == defs.BUY:
        conv = price.buy_conv
    else:
        log_message(f"Unrecognized signal {signal}", pair)
        return False

    ic_instance = InstrumentCollection()

    # Safety check for the pair in the dictionary
    pipLocation = ic_instance.instruments_dict.get(pair, {}).get('pipLocation', None)
    
    if not pipLocation or loss == 0:
        log_message(f"Invalid values found. Check pipLocation or loss for pair {pair}.", pair)
        return False

    # Calculate units based on risk
    num_pips = loss / pipLocation
    per_pip_loss = trade_risk / num_pips
    units = per_pip_loss / (conv * pipLocation)

    log_message(f"{pipLocation} {num_pips} {per_pip_loss} {units:.1f}", pair)

    return units
