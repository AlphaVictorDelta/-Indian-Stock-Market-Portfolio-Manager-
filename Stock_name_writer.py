from nsetools import Nse
from pprint import pprint
import sqlite3
nse = Nse()
print(nse)

conn3 = sqlite3.connect('STOCKS.sqlite')
cur3 = conn3.cursor()

cur3.executescript('''
CREATE TABLE IF NOT EXISTS "STOCKS" (
	"Symbol"  TEXT NOT NULL,
	"Name"  TEXT NOT NULL
);
''')

all_stock_codes = nse.get_stock_codes()
all_stock_codes.pop('SYMBOL')

for i,j in all_stock_codes.items():
	name = j
	symbol = i

	cur3.execute('''INSERT INTO "STOCKS" (Symbol,Name) VALUES (?,?)''',(symbol,name) )
conn3.commit()
