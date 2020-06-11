from pprint import pprint
import sqlite3
from datetime import date
import getpass
from nsetools import Nse
nse = Nse()
print(nse)



conn2 = sqlite3.connect('passwords.sqlite')
cur2 = conn2.cursor()

cur2.executescript('''
CREATE TABLE IF NOT EXISTS "Accounts" (
	"ID"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"Username"  TEXT NOT NULL,
	"Password"  TEXT NOT NULL,
	"AccBal"    INTEGER NOT NULL,
	"DatabaseName"  TEXT NOT NULL
);
''')

conn3 = sqlite3.connect('STOCKS.sqlite')
cur3 = conn3.cursor()

cur3.execute('SELECT Symbol FROM STOCKS')
stock_names_list = cur3.fetchall()
Stock_codes= list()

for name_tuple in stock_names_list:
	for (name_variable) in name_tuple:
		Stock_codes.append(name_variable)







def sell_trade(x):
	user_username = x
	flag12 = True
	while flag12 == True:
		try:
			stock_name = input('\n\tEnter the Name of the Stock : ')
			stock_action = 'SELL'
			cur1.execute('SELECT Quantity FROM Portfolio WHERE StockName = ?',(stock_name,))
			existing_quan = cur1.fetchone()[0]
			flag12 = False
			continue
		except:
			print('Hey! This stock does not exist, Try Again!')
			continue

	flag8 = True
	while flag8 == True:
		try:
			stock_sell_price = float(input('\n\tEnter the Selling Price : '))
			stock_sell_quan = int(input('\n\tEnter the Quantity : '))
		except:
			print('Please Enter digits only!')
			continue
		

		if stock_sell_quan > existing_quan :
			print('\nSelling a quantity that does not exist! Please Try Again!')
			continue 
		else:
			remaining_quan = existing_quan - stock_sell_quan
			Money_return = stock_sell_quan*stock_sell_price
			Money_return = Money_return - ((1/100)*Money_return)
			flag8 = False
			continue
	cur1.execute('SELECT Amount_Invested FROM Portfolio WHERE StockName = ?',(stock_name,))
	money_invested = cur1.fetchone()[0]
	ProfitLoss = Money_return -(-1 * money_invested)

	cur1.execute('UPDATE Portfolio SET Quantity = ? WHERE StockName = ?',(remaining_quan,stock_name))
	cur1.execute('UPDATE Portfolio SET Amount_Invested = ? WHERE StockName = ?',(ProfitLoss,stock_name))
	conn1.commit()

	cur1.execute('INSERT INTO "History" (Date,StockName,Action,Quantity,Price,Amount_Invested) VALUES (?,?,?,?,?,?)''',
	 (Date_,stock_name,stock_action,stock_sell_quan,stock_sell_price,Money_return))
	conn1.commit()

	cur1.execute('SELECT StockName FROM ProfitLoss')
	stock_names_list = cur1.fetchall()
	stock_name_record = list()
	count = 0
	for name_tuple in stock_names_list:
		for (name_variable) in name_tuple:
			stock_name_record.append(name_variable)


	for name_variable in stock_name_record:
		if stock_name == name_variable:
			cur1.execute('SELECT Profit_Loss FROM ProfitLoss WHERE StockName = ?',(stock_name,))
			previous_Profit = cur1.fetchone()[0]
			ProfitLoss = previous_Profit + ProfitLoss
			if ProfitLoss > 0:
				Result = 'PROFIT'
			else:
				Result = 'LOSS'
			cur1.execute('UPDATE ProfitLoss SET Profit_Loss = ? WHERE StockName = ?',(ProfitLoss,stock_name))
			cur1.execute('UPDATE ProfitLoss SET Result = ? WHERE StockName = ?',(Result,stock_name))
			count = count + 1
			conn1.commit()

	if count == 0:
		if ProfitLoss > 0:
			Result = 'PROFIT'
		else:
			Result = 'LOSS'

		cur1.execute('INSERT INTO "ProfitLoss" (Date,StockName,Profit_Loss,Result) VALUES (?,?,?,?)',(Date_,stock_name,ProfitLoss,Result))
		del_quan = 0
		cur1.execute('DELETE FROM Portfolio WHERE Quantity = ?',(del_quan,))

		conn2 = sqlite3.connect('passwords.sqlite')
		cur2 = conn2.cursor()
		cur2.execute('SELECT Accbal FROM Accounts WHERE Username = ?',(user_username,))
		cur_bal = cur2.fetchone()[0]

		cur_bal = cur_bal + Money_return

		cur2.execute('UPDATE Accounts SET AccBal = ? WHERE Username = ?',(cur_bal,user_username))
		conn2.commit()


		cur1.execute('INSERT INTO "EndOfDay_Balance" (Date,EndDayBalance) VALUES (?,?)',(Date_,cur_bal))
		conn1.commit()










def buy_trade(x):
	user_username = x
	flag13 = True
	while flag13 == True:
		stock_name = input('\n\tEnter the Symbol of the Stock as per STOCKS.sqlite : ')
		for name in Stock_codes:
			if stock_name == name:
				flag13 = False
				break
			


	stock_action = 'BUY'

	flag7 = True
	while flag7 == True:

		try:
			stock_buy_price = float(input('\n\tEnter the Price of the Stock : '))
			stock_buy_quan = int(input('\n\tEnter the Quantity : '))
			flag7 = False
			continue

		except:
			print('Please Enter only Digits :')
			continue

	stock_total = stock_buy_quan*stock_buy_price 
	stock_total = stock_total + ((1/100)*stock_total)

	Date_ = str(date.today())

	conn2 = sqlite3.connect('passwords.sqlite')
	cur2 = conn2.cursor()
	cur2.execute('SELECT Accbal FROM Accounts WHERE Username = ?',(user_username,))
	cur_bal = cur2.fetchone()[0]



	if stock_total > cur_bal:
		print('Insufficient Funds! Please try Again!')
		return None
	else:
		cur1.execute('''INSERT INTO "History" (Date,StockName,Action,Quantity,Price,Amount_Invested) VALUES (?,?,?,?,?,?)''',
		 (Date_,stock_name,stock_action,stock_buy_quan,stock_buy_price,stock_total) )
		conn1.commit()

	






	cur1.execute('''SELECT StockName FROM "Portfolio"''')
	stock_records = cur1.fetchall()
	stock_names_list = list()
	for name_tuple in stock_records:
		for (name_variable) in name_tuple:
			stock_names_list.append(name_variable)


	count = 0

	for name_variable_1 in stock_names_list:        
		if stock_name == name_variable_1:
			print('ENTER THE IF !')
			cur1.execute('SELECT * FROM Portfolio WHERE StockName = ?',(name_variable,))
			stock_record = cur1.fetchall()


			new_price = stock_buy_price
			new_quan = stock_record[0][4]
			new_quan = stock_buy_quan + new_quan
			new_total = stock_record[0][5] + (-1 * stock_total)

			cur1.execute('UPDATE Portfolio SET Price = ? WHERE StockName = ?',(new_price,stock_name))
			cur1.execute('UPDATE Portfolio SET Quantity = ? WHERE StockName = ?',(new_quan,stock_name))
			cur1.execute('UPDATE Portfolio SET Amount_Invested = ? WHERE StockName = ?',(new_total,stock_name))
			conn1.commit()
			count = count + 1
			break   
		   

			
			
	if count == 0 :
		cur1.execute('''INSERT INTO "Portfolio" (Date,StockName,Quantity,Price,Amount_Invested) VALUES (?,?,?,?,?)''',
		 (Date_,stock_name,stock_buy_quan,stock_buy_price,-1*stock_total) )
		conn1.commit()  


	conn2 = sqlite3.connect('passwords.sqlite')
	cur2 = conn2.cursor()
	cur2.execute('SELECT Accbal FROM Accounts WHERE Username = ?',(user_username,))
	cur_bal = cur2.fetchone()[0]

	cur_bal = cur_bal  - stock_total

	cur2.execute('UPDATE Accounts SET AccBal = ? WHERE Username = ?',(cur_bal,user_username))
	conn2.commit()


	cur1.execute('INSERT INTO "EndOfDay_Balance" (Date,EndDayBalance) VALUES (?,?)',(Date_,cur_bal))
	conn1.commit()








def update_portfolio():
	print('updating Portfolio...')
	cur1.execute('''SELECT StockName FROM "Portfolio"''')
	stock_records = cur1.fetchall()
	stock_names_list = list()
	for name_tuple in stock_records:
		for (name_variable) in name_tuple:
			stock_names_list.append(name_variable)





	for name in stock_names_list:

		cur1.execute('SELECT Quantity FROM "Portfolio" WHERE StockName = ?',(name,))
		hypo_quan = cur1.fetchone()[0]

		cur1.execute('SELECT Amount_Invested FROM "Portfolio" WHERE StockName = ?',(name,))
		actaul_price = cur1.fetchone()[0]
		actaul_price = -1 * actaul_price


		

		get_price = nse.get_quote(name)
		try:
			hypo_price = get_price['buyPrice1']
			hypo_money = hypo_price * hypo_quan
		except:
			hypo_price = get_price['sellPrice1']
			hypo_money = hypo_price * hypo_quan


		hypo_money = hypo_money - ((1/100)*hypo_money)
		hypo_profit = hypo_money - actaul_price

		cur1.execute('UPDATE Portfolio SET Current_live_Price = ? WHERE StockName = ?',(hypo_price,name))
		cur1.execute('UPDATE Portfolio SET Hypo_Profit = ? WHERE StockName = ?',(hypo_profit,name))
		conn1.commit()
		





def update_dailyhighlights():
	pass









def Delete_Record():
	pass










Date_ = str(date.today())
user_login = None


print('\t\tW E L C O M E\n')
print(f'\t\t Date : {Date_}')


flag1 = True
while flag1 == True:
	choice_acc = input('\nDo you have an account ? YES or NO : ')
	if choice_acc == 'YES' or choice_acc == 'yes':
		user_username = input ('Please Enter Your Registered Username : ')
		try:
			cur2.execute('SELECT Password FROM Accounts WHERE Username = ?',(user_username,))
			Password = cur2.fetchone()[0]
		except:
			print('Please enter proper credentials ! try again!')
			continue
		
		
		if len(user_username) > 1:
			cur2.execute('SELECT Password FROM Accounts WHERE Username = ?',(user_username,))
			Password = cur2.fetchone()[0]

			flag2 = True
			while flag2 == True:

				user_password = getpass.getpass('\nEnter Password : ')
				if user_password == Password:
					user_login = True
					cur2.execute('SELECT DatabaseName FROM Accounts WHERE Username = ?',(user_username,))
					user_database = cur2.fetchone()[0]
					conn1 = sqlite3.connect(user_database)
					cur1 = conn1.cursor()

					cur1.executescript('''
						CREATE TABLE IF NOT EXISTS "ProfitLoss" (
						"ID"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
						"Date"  TEXT NOT NULL,
						"StockName" TEXT NOT NULL,
						"Profit_Loss"   INTEGER NOT NULL,
						"Result"    TEXT NOT NULL
						);

						CREATE TABLE IF NOT EXISTS "EndOfDay_Balance" (
						"ID"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
						"Date"  TEXT NOT NULL,
						"EndDayBalance" INTEGER NOT NULL
						);

						CREATE TABLE IF NOT EXISTS "Portfolio" (
						"ID"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
						"Date"  TEXT NOT NULL,
						"StockName" TEXT NOT NULL,
						"Price" INTEGER NOT NULL,
						"Quantity"  INTEGER NOT NULL,
						"Amount_Invested"   INTEGER NOT NULL,
						"Current_live_Price" INTEGER ,
						"Hypo_Profit" INTEGER 
						);

						CREATE TABLE IF NOT EXISTS "History" (
						"ID"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
						"Date"  TEXT NOT NULL,
						"StockName" TEXT NOT NULL,
						"Action"    TEXT NOT NULL,
						"Quantity"  INTEGER NOT NULL,
						"Price" INTEGER NOT NULL,
						"Amount_Invested"   INTEGER NOT NULL
						);



						''')


					flag2 = False
					flag1 = False 
					break

				else:
					print('\nINCORRECT PASSWORD ! ')
					print('Retype the Password ')
					flag2 = True
		else:
			print ('\nThe Username Does Not exist ! Please try again !')

	elif choice_acc == 'no' or choice_acc == 'NO':

		choice_make_acc = input('Do You want to make an account ? YES or NO : ')
		if choice_make_acc == 'yes' or choice_make_acc == 'YES':

			flag3 = True
			while flag3 == True:

				new_username = input('\n\nEnter Username : ')
				cur2.execute('SELECT * FROM Accounts')
				username_records = cur2.fetchall()
				username_list = []
				for row in username_records:
					username_list.append(row[1])

				count = 0

				for name_variable in username_list:
					if name_variable == new_username:
						print('\nThis Username Has Already Been taken!')
						count = count+1
						continue
				if count == 0:
					print('Valid Username!')
					new_database = new_username+'.sqlite'
					print(f'Your Database Name is : {new_database}')
					print('\nPlease log into your account to create the database!')
					flag3 = False
					break
						

			flag4 = True
			while flag4 == True:

				new_password1 = getpass.getpass('\n\tEnter Password : ')
				new_password2 = getpass.getpass('\n\tReEnter Password : ')

				if new_password1 == new_password2:
					if len(new_password1) >= 6 :
						new_password = new_password1
						flag4 = False
					else:
						print('\nPlease Enter a Password with more than 6 characters')
						continue
				else:
					print('\nboth the passwords should match ')
					continue


			flag5 = True
			while flag5 == True:
				new_balance = input('\nEnter your Current DEMAT account balance : ')
				try:
					new_balance = float(new_balance)
					flag5 = False
					continue
				except:
					print('Enter in Digits only!')
					continue

			
			cur2.execute('''INSERT INTO "Accounts" (Username,Password,Accbal,DatabaseName) VALUES (?,?,?,?)''', (new_username,new_password,new_balance,new_database) )
			conn2.commit()

			flag1 = False 
			continue

		elif choice_make_acc == 'NO' or choice_make_acc == 'no' :
			print('\n\n\n\t\tThank You! Have A Good Day!')
			exit()

		else:
			print('Enter A Valid Input!')
			break

	else :
		print('\nPlease enter a Valid Answer ')
		flag1 = False 
		continue


if user_login == True:
	flag6 = True

	while flag6 == True:
		user_trade = input('''\n\nPlease pick a action :-
		1 : Register a Trade
		2 : Add/Remove Money
		3 : Exit and Update
		4 : Delete Record
		\n\n\t
		 ''')
		if user_trade == '1':
			trade_action = input('BUY or SELL : ')
			if trade_action == 'BUY' or trade_action == 'buy':
				buy_trade(user_username)
				continue
			elif trade_action == 'SELL' or trade_action == 'sell':
				sell_trade(user_username)
				continue
			else :
				print('\n\nPlease Enter a Valid Action! ' )
				continue
		elif user_trade == '2':
			
			flag9 = True
			while flag9 == True:
				try:
					others_name =input('\nplease confirm your username :')
					conn2 = sqlite3.connect('passwords.sqlite')
					cur2 = conn2.cursor()
					cur2.execute('SELECT Accbal FROM Accounts WHERE Username = ?',(others_name,))
					cur_bal = cur2.fetchone()[0]
					flag9 = False
					continue
				except:
					print('\n please enter a valid username!')
					continue

			user_others = input('\nEnter 1: for adding/removing money \nEnter 2: for deleting an Entry')
			if user_others == '1':
				flag11 = True
				while flag11 == True:
					addrem = input('\nEnter 1 for adding Money\nEnter 2 for Removing money')


					if addrem == '1':

						flag10 = True
						while flag10 == True :	
							try:
								add_money = float(input('\n how much money to add? '))
								cur_bal = cur_bal + add_money 
								flag10 = False
								flag11 = False
								continue
							except:
								print('Enter digits only!')
								continue


				cur2.execute('UPDATE Accounts SET AccBal = ? WHERE Username = ?',(cur_bal,user_username))
				conn2.commit() 
				db =others_name+'.sqlite'

				conn2 = sqlite3.connect(db)
				cur2 = conn2.cursor()
				cur1.execute('INSERT INTO "EndOfDay_Balance" (Date,EndDayBalance) VALUES (?,?)',(Date_,cur_bal))
				conn1.commit()

			elif user_others == '2':
				flag10 == True
				while flag10 == True :	
					try:
						remo_money = float(input('\n how much money to remove? '))
						cur_bal = cur_bal + remo_money 
						flag10 = False
						continue
					except:
						print('Enter digits only!')
						continue


				cur2.execute('UPDATE Accounts SET AccBal = ? WHERE Username = ?',(cur_bal,user_username))
				conn2.commit() 
				db =others_name+'.sqlite'

				conn2 = sqlite3.connect(db)
				cur2 = conn2.cursor()
				cur1.execute('INSERT INTO "EndOfDay_Balance" (Date,EndDayBalance) VALUES (?,?)',(Date_,cur_bal))
				conn1.commit()
		elif user_trade =='3':
			update_portfolio()
			update_dailyhighlights()
			print('\n\n\nGood Day!')
			print('\t\tSESSION TERMINATED!')
			exit()
		elif user_trade == '4':
			print('\n Deleting a Record is a Hectic Process ! Make sure to enter correct details next time')
		else:
			exit()













			










					
