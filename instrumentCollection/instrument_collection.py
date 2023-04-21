import json
from models.instrument import Instrument
from DB.db import DataDB

class InstrumentCollection:
    FILENAME = "instruments.json"
    API_KEYS = ['name', 'type', 'displayName', 'pipLocation', 'displayPrecision', 'tradeUnitsPrecision','marginRate']
    
    def __init__ (self):
        self.instruments_dict = {}
        
    def LoadInstrumentsDB(self):
        self.instruments_dict = {}
        data = DataDB().query_single(DataDB.INSTRUMENTS_COLL)
        for k, v in data.items():
            self.instruments_dict[k] = Instrument.FromApiObject(v)
    
    def  CreateDB(self, data):
        if data is None:
            print("Instrument file creation failed")
            return
        
        instruments_dict = {}
        for i in data:
            key = (i['name'])
            instruments_dict[key] = {k: i[k] for k in self.API_KEYS}
        
        database = DataDB()
        database.delete_many(DataDB.INSTRUMENTS_COLL) #removes everything in collection
        database.add_one(DataDB.INSTRUMENTS_COLL, instruments_dict)
            
            
    def PrintInstruments(self):
        [print(k,v) for k,v in self.instruments_dict.items()]
        print(len(self.instruments_dict.keys()), "Instruments")
    
instrumentCollection = InstrumentCollection()