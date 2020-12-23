from nsetools import Nse
from pprint import pprint

nse = Nse()
print(nse)

all_stock_codes = nse.get_stock_codes()
get_price = nse.get_quote('CASTROLIND')
pprint(get_price)