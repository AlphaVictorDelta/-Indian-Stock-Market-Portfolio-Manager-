from pprint import pprint
import sqlite3
from datetime import date
import getpass
from nsetools import Nse

nse = Nse()
print(nse)
all_stock_codes = nse.get_stock_codes()

conn1 = sqlite3.connect('Custom_select_stocks')
cur1 = conn1.cursor()

cur1.executescript('''
CREATE TABLE IF NOT EXISTS "Moms_Select_Stocks" (
	"ID"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"Nse_Code"  TEXT NOT NULL,
	"Stock_Name" TEXT ,
	"Curr_Price"  INTEGER NOT NULL
);
''')
cur1.execute('SELECT Nse_Code FROM Moms_Select_Stocks')
Existing_Codes_Bases = cur1.fetchall()
Existing_Codes = list()

for name_tuple in Existing_Codes_Bases:
	for (name_variable) in name_tuple:
		Existing_Codes.append(name_variable)


conn2 = sqlite3.connect('STOCKS.sqlite')
cur2 = conn2.cursor()

cur2.execute('SELECT Symbol FROM STOCKS')
Nse_Codes_list = cur2.fetchall()
Stock_Codes= list()

for name_tuple in Nse_Codes_list:
	for (name_variable) in name_tuple:
		Stock_Codes.append(name_variable)

def get_price(name):
	get_price = nse.get_quote(name)
	curr_price = get_price['sellPrice1']
	if curr_price == None:
		price_list = ['buyPrice1', 'sellPrice2', 'sellPrice3', 'buyPrice2', 'sellPrice4', 'buyPrice3', 'sellPrice5', 'buyPrice4', 'buyPrice5']
		for i in price_list:
			curr_price = get_price[i]
			if curr_price != None:
				break
	if curr_price == None:
		curr_price = 0 
		return curr_price
	else:
		return curr_price

def Enter_Stock():
	temp1 = True
	while temp1:
		Nse_Code = input('\nEnter Name of Stock:\t')
		Nse_Code = Nse_Code.upper()
		if Nse_Code in Existing_Codes:
			print('\nStock Already Exists in Database. Please Choose to Update or Try Another Stock')
			continue

		if Nse_Code in Stock_Codes:
			temp1 = False

	new_price = get_price(Nse_Code)
	stock_nse_name = all_stock_codes[Nse_Code]

	conn1 = sqlite3.connect('Custom_select_stocks')
	cur1 = conn1.cursor()

	cur1.execute('INSERT INTO "Moms_Select_Stocks" (Nse_Code, Curr_Price, Stock_Name) VALUES (?,?,?)',(Nse_Code, new_price, stock_nse_name))
	conn1.commit()




def Update_Database():

	conn1 = sqlite3.connect('Custom_select_stocks')
	cur1 = conn1.cursor()
	cur1.execute('SELECT Nse_Code FROM Moms_Select_Stocks')
	Existing_Codes_Bases = cur1.fetchall()
	Existing_Codes = list()

	for name_tuple in Existing_Codes_Bases:
		for (name_variable) in name_tuple:
			Existing_Codes.append(name_variable)


	for name in Existing_Codes:
		current_price = get_price(name)
		conn1 = sqlite3.connect('Custom_select_stocks')
		cur1 = conn1.cursor()
		cur1.execute('UPDATE Moms_Select_Stocks SET Curr_Price = ? WHERE Nse_Code = ?',(current_price, name))
		conn1.commit()


# Main Function
print('WELCOME')
temp2 = True
while temp2:
	print('Choose an Option!')
	print('1. Enter Stocks')
	print('2. Update and Exit')
	user_choice = input('\nEnter Your Choice!\n')
	try:
		user_choice = int(user_choice)
	except:
		print('\nChoice Must be a Number. Choose Again\n')
		continue

	if user_choice == 1:
		temp3 = True
		while temp3:
			print('\nDo you want to enter Stocks!? Y/N\n')
			stock_choice = input()
			stock_choice = stock_choice.upper()

			if stock_choice == 'Y':
				Enter_Stock()
				continue
			elif stock_choice == 'N':
				temp3 = False
				continue
			else:
				print('\nPlease Choose the right option')
				continue

	elif user_choice == 2:
		Update_Database()
		print('\n Updating and Exiting Application!')
		temp2 == False
		break

	else:
		print('Invalid Choice! ... Choose Again!')
		continue