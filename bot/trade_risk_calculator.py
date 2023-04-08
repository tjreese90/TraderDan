from api.oanda_api import OandaApi
import constants.defs as defs
from instrumentCollection.instrument_collection import instrumentCollection as ic

def get_trade_units(api: OandaApi, pair, signal, loss, trade_risk, log_message):
    """
    This function calculates the number of units to trade. It does this by calculating the number of pips
    to loss, then dividing the trade risk by that number to get the per-pip loss. It then divides the per-pip
    loss by the conversion factor to get the number of units. This conversion factor is the number of pips
    that the currency has to move in order to make the trade profitable.
    """
    prices = api.get_prices([pair])
    
    if prices is None or len(prices) == 0:
        log_message("get_trade_units() Price is none", pair)
        return False
    
    price = None
    for p in prices:
        if p.instrument == pair:
            price = p
            break
        
    if price is None:
        log_message("get_trade_units() price is none???? Bad Bad", pair)
        return False
    
    log_message(f"get_trade_units() price {price}", pair)
    
    conv = price.buy_conv
    if signal == defs.SELL:
        conv = price.sell_conv
        
    pipLocation = ic.instruments_dict[pair].pipLocation
    num_pips = loss / pipLocation
    per_pip_loss = trade_risk / num_pips
    units = per_pip_loss / (conv * pipLocation)
    
    log_message(f"{pipLocation} {num_pips} {per_pip_loss} {units:.1f}", pair)
    
    return units

def get_trade_units(api: OandaApi, pair, signal, loss, trade_risk, log_message):
    prices = api.get_prices([pair])
    
    if prices is None or len(prices) == 0:
        log_message("get_trade_units() Price is none", pair)
        return False
    
    price = None
    for p in prices:
        if p.instrument == pair:
            price = p
            break
        
    if price is None:
        log_message("get_trade_units() price is none???? Bad Bad", pair)
        return False
    
    log_message(f"get_trade_units() price {price}", pair)
    
    conv = price.buy_conv
    if signal == defs.SELL:
        conv = price.sell_conv
        
    pipLocation = ic.instruments_dict[pair].pipLocation
    num_pips = loss / pipLocation
    per_pip_loss = trade_risk / num_pips
    units = per_pip_loss / (conv * pipLocation)
    
    log_message(f"{pipLocation} {num_pips} {per_pip_loss} {units:.1f}", pair)
    
    return units