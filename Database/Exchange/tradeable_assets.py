import sqlite3


class TradeableAsset:
    def __init__(self):
        self.connection = sqlite3.connect('TradingBot.db')
        self.c = self.connection.cursor()

        self.c.execute('CREATE TABLE IF NOT EXISTS Assets(exchange TEXT, base_currency TEXT, target_currencies TEXT)')

        self.init_binance()

    def close(self):
        self.c.close()
        self.connection.close()
        print("Closed Assets TradingBot.db")

    def insert_asset(self, exchange, base_currency, target_currencies):
        self.c.execute('Select * FROM Assets WHERE exchange=? AND base_currency=?', (exchange,base_currency,))
        data = self.c.fetchall()
        if data.__len__() == 0:
            self.c.execute("INSERT INTO Assets (exchange, base_currency, target_currencies) VALUES (?, ?, ?)", (exchange, base_currency, target_currencies))
        else:
            self.c.execute("UPDATE Assets SET target_currencies=? WHERE exchange=? AND base_currency=?", (target_currencies, exchange, base_currency))

        self.connection.commit()

    def init_binance(self): #Add everyone when working
        self.insert_asset('binance', 'BNB', "ADA,ADX,AE,AGI,AION,AMB,APPC,ARDR,BAT,BCC,BCN,BCPT,BLZ,BRC,BTS,CMT,CND,CVC,DLT,ENJ,EOS,ETC,GNT,GTO,ICX,IOTA,LOOM,LSK,LTC,MCO,MFT,NANO,NAS,NAV,NCASH,NEBL,NEO,NULS,NXS,ONT,OST,PIVX,POA,POLY,POWR,QLC,QSP,QTUM,RCN,RDN,REP,RLC,RPX,SC,SKY,STEEM,STORM,SYS,THETA,TRIG,TUSD,VET,VIA,WABI,WAN,WAVES,WTC,XEM,XLM,XRP,XZC,YOYO,ZEN,ZIL")
        self.insert_asset('binance', 'BTC', "ADA,ADX,AE,AGI,AION,AMB,APPC,ARDR,ARK,AST,BAT,BCC,BCD,BCN,BCPT,BLZ,BNB,BNT,BQX,BRD,BTQ,BTS,CDT,CHAT,CLOAK,CMT,CND,CVC,DASH,DATA,DENT,DGD,DLT,DNT,DOCK,EDO,ELF,ENG,ENJ,EOS,ETC,ETH,EVX,FUEL,FUN,GAS,GNT,GRS,GTO,GVT,GXS,HOT,HSR,ICN,ICX,INS,IOST,IOTA,IOTX,KEY,KMD,KNC,LEND,LINK,LOOM,LRC,LSK,LTC,LUN,MANA,MCO,MDA,MFT,MOD,MTH,MTL,NANO,NAS,NAV,NCASH,NEBL,NEO,NPXS,NULS,NXS,OAX,OMG,ONT,OST,PIVX,POA,POE,POLY,POWR,PPT,QKC,QLC,QSP,QTUM,RCN,RDN,REP,REQ,RLC,RPX,SALT,SC,SKY,SNGL,SNM,SNT,STEEM,STORJ,STORM,STRAT,SUB,SYS,THETA,TNB,TNT,TRIG,TRX,TUSD,VET,VIA,VIB,VIBE,WABI,WAN,WAVES,,WINGS,WPR,WTC,XEM,XLM,XMR,XRP,XVG,XZC,YOYO,ZEC,ZEN,ZIL,ZRX")
        self.insert_asset('binance', 'ETH', "ADA,ADX,AE,AGI,AION,AMB,ARDR,ARK,ARN,AST,BAT,BCC,BCD,BCN,BCPT,BLZ,BNB,BQX,BRD,BTG,BTS,CDT,CHAT,CLOAK,CMT,CND,CVC,DASH,DATA,DENT,DGD,DLT,DNT,DOCK,EDO,ELF,ENG,ENJ,EOS,ETC,EVC,FUEL,FUN,GNT,GRS,GTO,GVT,GXS,HOT,HSR,ICN,ICX,INS,IOST,IOTA,IOTX,KEY,KMD,KNC,LEND,LINK,LOOM,LRC,LSK,LTC,LUN,MANA,MCO,MDA,MFT,MOD,MTH,MTL,NANO,NAS,NAV,NCASH,NEBL,NEO,NPXS,NULS,NXS,OAX,OMG,ONT,OST,PIVX,POA,POE,POWR,PPT,QKC,QLC,QSP,QTUM,RCN,RDN,REP,REQ,RLC,RPX,SALT,SC,SKY,SNGLS,SNM,STEEM,STORJ,STORM,STRAT,SUB,SYS,THETA,TNB,TNT,TRIG,TRX,TUSD,VET,VIA,VIBE,VIB,WABI,WAN,WAVES,WINGS,WPR,WTC,XEM,XLM,XMR,XRP,XVG,XZC,YOYO,ZEC,ZEN,ZIL,ZRX")
        self.insert_asset('binance', 'USDT', "ADA,BCC,BNB,BTC,EOS,ETC,ETH,ICX,IOTA,LTC,NEO,NULS,ONT,QTUM,TRX,TUSD,VET,XLM,XRP")

    def fetch(self, exchange):
        data = {}
        self.c.execute("Select * From Assets WHERE exchange=?", (exchange,))
        for row in self.c.fetchall():
            base = row[1]
            targets = row[2].split(",")
            data[base] = targets

        return data
