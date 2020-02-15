#CONTACT ME FOR QUESTIONS AND SUGGESTIONS ON DISCORD Aevann#6346
import sys, os, datetime, pytz, hashlib, requests, json, re, time, gspread, sys, datetime, os, csv, math
from oauth2client.service_account import ServiceAccountCredentials
from gspread_formatting import *

devid = '' #INSERT YOUR API HIREZ DEV ID
authkey = '' #INSERT YOUR HIREZ API AUTH KEY
kbmgooglesheetid = '1g05xgJnAR0JQXzreEOqG-xV5cd0izx67ZvOTXMZe_Zg' #INSERT YOUR KEYBOARD & MOUSE GOOGLE SHEET ID (YOU'LL FIND IT IN ITS URL)
controllergooglesheetid = '12TrxqtZbp2G_7p0vJYPOZvpSbCxNHFIFL_d767BTF9g' #INSERT YOUR CONTROLLER GOOGLE SHEET ID (YOU'LL FIND IT IN ITS URL)
basedir1 = os.path.dirname(os.path.realpath(__file__))
sheetsapikey1 = f'{basedir1}/sheetsapikey1.json' #INSERT THE LOCATION OF YOUR FIRST GOOGLE SHEETS API KEY
sheetsapikey2 = f'{basedir1}/sheetsapikey2.json' #INSERT THE LOCATION OF YOUR SECOND GOOGLE SHEETS API KEY
sheetsapikey3 = f'{basedir1}/sheetsapikey3.json' #INSERT THE LOCATION OF YOUR THIRD GOOGLE SHEETS API KEY
hour = '-1'
rankindex = ['Qualifying', 'Bronze', 'Bronze', 'Bronze', 'Bronze', 'Bronze', 'Silver', 'Silver', 'Silver', 'Silver', 'Silver', 'Gold', 'Gold', 'Gold', 'Gold', 'Gold', 'Platinum', 'Platinum', 'Platinum', 'Platinum', 'Platinum', 'Diamond', 'Diamond', 'Diamond', 'Diamond', 'Diamond', 'Master', 'Master', 'All Ranks']
bancount = {}

def calcandpost():
	global bancount
	matchcount = json.loads(open(f'{basedir2}matchcount.json').read()[8:])
	wincount = json.loads(open(f'{basedir2}wincount.json').read())
	cardmatchcount = json.loads(open(f'{basedir2}cardmatchcount.json').read())
	cardwincount = json.loads(open(f'{basedir2}cardwincount.json').read())
	itemmatchcount = json.loads(open(f'{basedir2}itemmatchcount.json').read())
	itemwincount = json.loads(open(f'{basedir2}itemwincount.json').read())
	compmatchcount = json.loads(open(f'{basedir2}compmatchcount.json').read())
	compwincount = json.loads(open(f'{basedir2}compwincount.json').read())
	enemymatchcount = json.loads(open(f'{basedir2}enemymatchcount.json').read())
	enemywincount = json.loads(open(f'{basedir2}enemywincount.json').read())
	dps = json.loads(open(f'{basedir2}dps.json').read())
	hps = json.loads(open(f'{basedir2}hps.json').read())
	sps = json.loads(open(f'{basedir2}sps.json').read())
	avgmatchcount = json.loads(open(f'{basedir2}avgmatchcount.json').read())
	gcs = [gspread.authorize(ServiceAccountCredentials.from_json_keyfile_name(sheetsapikey1, ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])), gspread.authorize(ServiceAccountCredentials.from_json_keyfile_name(sheetsapikey2, ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])), gspread.authorize(ServiceAccountCredentials.from_json_keyfile_name(sheetsapikey3, ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']))]
	gcn = 0
	gc = gcs[gcn]

	avgdps = {}
	for k, v in dps.items(): avgdps[k] = v/avgmatchcount[k]
	avghps = {}
	for k, v in hps.items(): avghps[k] = v/avgmatchcount[k]
	avgs = []
	for k, v in sps.items():
		if k == 'Grohk,Maelstrom': cc = 'Damage'
		elif k == 'Pip,Catalyst': cc =  'Flank'
		elif k == 'Skye,Smoke and Dagger': cc =  'Support'
		else: cc= cclass[k.split(",")[0]]
		avgs.append((cc, k, avgdps[k], avghps[k], v/avgmatchcount[k], avgmatchcount[k]))
	
	avgs.sort(key=lambda x: (-x[2], -x[3], -x[4], -x[5]))
	open(f'{basedir2}avgs.csv', 'w').write(f'Class, Champion,Talent,Average DPS,Average HPS,Average SPS,Match Count\n' + str(avgs).replace('"', "'").replace("), ('" , '\n').replace("', '" , ",").replace("', " , ",")[3:-2])
	sheet = gc.open_by_key(googlesheetid)
	while True:
		try:
			sheet.values_update(
				'Average Damage/Healing/Shielding Per Second',
				params={'valueInputOption': 'USER_ENTERED'},
				body={'values': list(csv.reader(open(f'{basedir2}avgs.csv')))})
			format_cell_range(sheet.worksheet('Average Damage/Healing/Shielding Per Second'), 'A1:Z1', cellFormat(textFormat=textFormat(bold=True)))
		except Exception as e:
			if 'Quota exceeded for quota group' not in str(e):
				print(e)
				sys.exit()
			gcn += 1
			gc = gcs[gcn]
			sheet = gc.open_by_key(googlesheetid)
			continue
		break
	
	banrate = []
	for k, v in bancount.items():
		if k == None: continue
		br = str(v/ratematchcount*100).split('.')[0] + '%'
		if len(br) == 2: br = f'0{br}'
		pr = str(pickcount[k]/(ratematchcount-v)*100).split('.')[0] + '%'
		if len(pr) == 2: pr = f'0{pr}'
		wr = str(wincount[f'{k},All Ranks'] / matchcount[f'{k},All Ranks']*100).split('.')[0] + '%'
		banrate.append((k, br, pr, wr))
	banrate.sort(key=lambda x: (x[1], x[2]), reverse=True)
	open(f'{basedir2}banrate.csv', 'w').write(f'Champion,{day} Banrate,{day} Pickrate when not banned,v{patch} Winrate\n' + str(banrate).replace('"', "'").replace("'), ('" , '\n').replace("', '" , ",")[3:-3])
	sheet = gc.open_by_key(googlesheetid)
	while True:
		try:
			sheet.values_update(
				'Champion Banrates',
				params={'valueInputOption': 'USER_ENTERED'},
				body={'values': list(csv.reader(open(f'{basedir2}banrate.csv')))})
			format_cell_range(sheet.worksheet('Champion Banrates'), 'A1:Z1', cellFormat(textFormat=textFormat(bold=True)))
		except Exception as e:
			if 'Quota exceeded for quota group' not in str(e):
				print(e)
				sys.exit()
			gcn += 1
			gc = gcs[gcn]
			sheet = gc.open_by_key(googlesheetid)
			continue
		break

	cardWRs = []
	for champ, cards in cardmatchcount.items():
		for card, cardmatchcount in cards.items():
			D = cardwincount[champ][card] / cardmatchcount
			E = cardmatchcount
			H = D*E
			I = E-H
			J = 2.5758293035489
			C1 = max(D-J/(E+J**2)*math.sqrt(H*I/E+J**2/4),0)
			C2 = min(D+J/(E+J**2)*math.sqrt(H*I/E+J**2/4),1)
			D = str(D*100).split('.')[0] + '%'
			if len(D) == 2: D = f'0{D}'
			C1 = str(C1*100).split('.')[0] + '%'
			if len(C1) == 2: C1 = f'0{C1}'
			C2 = str(C2*100).split('.')[0] + '%'
			if len(C2) == 2: C2 = f'0{C2}'
			cardWRs.append((f'{champ},{card}', D, E, C1, C2))
	cardWRs.sort(key=lambda x:(x[0].split(',')[2], x[3], x[1], x[2]), reverse=True)
	cardWRs.sort(key=lambda x:(x[0].split(',')[0]))
	open(f'{basedir2}cardWRs.csv', 'w').write(f'Champion,Card,Card Level,v{patch} Winrate,v{patch} Match Count,Confidence Interval -,Confidence Interval +\n' + str(cardWRs).replace('"' , "'").replace("'), ('" , "\n").replace(", " , ",").replace("'," , ",").replace(",'" , ",")[3:-3])

	sheet = gc.open_by_key(googlesheetid)
	while True:
		try:
			sheet.values_update(
				'By Card',
				params={'valueInputOption': 'USER_ENTERED'},
				body={'values': list(csv.reader(open(f'{basedir2}cardWRs.csv')))})
		except Exception as e:
			if 'Quota exceeded for quota group' not in str(e):
				print(e)
				sys.exit()
			gcn += 1
			gc = gcs[gcn]
			sheet = gc.open_by_key(googlesheetid)
			continue
		break

	itemWRs = []
	for item, itemmatchcount in itemmatchcount.items():
		D = itemwincount[item] / itemmatchcount
		E = itemmatchcount
		H = D*E
		I = E-H
		J = 2.5758293035489
		C1 = max(D-J/(E+J**2)*math.sqrt(H*I/E+J**2/4),0)
		C2 = min(D+J/(E+J**2)*math.sqrt(H*I/E+J**2/4),1)
		D = str(D*100).split('.')[0] + '%'
		if len(D) == 2: D = f'0{D}'
		C1 = str(C1*100).split('.')[0] + '%'
		if len(C1) == 2: C1 = f'0{C1}'
		C2 = str(C2*100).split('.')[0] + '%'
		if len(C2) == 2: C2 = f'0{C2}'
		itemWRs.append((item, D, E, C1, C2))

	itemWRs.sort(key=lambda x:(x[3], x[1], x[2]), reverse=True)
	itemWRs.sort(key=lambda x:(x[0].split(',')[0]))
	open(f'{basedir2}itemWRs.csv', 'w').write(f'Champion,Item,v{patch} Winrate,v{patch} Match Count,Confidence Interval -,Confidence Interval +\n' + str(itemWRs).replace('"' , "'").replace("'), ('" , "\n").replace(", " , ",").replace("'," , ",").replace(",'" , ",")[3:-3])

	sheet = gc.open_by_key(googlesheetid)
	while True:
		try:
			sheet.values_update(
				'By Item',
				params={'valueInputOption': 'USER_ENTERED'},
				body={'values': list(csv.reader(open(f'{basedir2}itemWRs.csv')))})
		except Exception as e:
			if 'Quota exceeded for quota group' not in str(e):
				print(e)
				sys.exit()
			gcn += 1
			gc = gcs[gcn]
			sheet = gc.open_by_key(googlesheetid)
			continue
		break

	compWRs = []
	for comp, compmatchcount in compmatchcount.items():
		D = compwincount[comp] / compmatchcount
		E = compmatchcount
		H = D*E
		I = E-H
		J = 2.5758293035489
		C1 = max(D-J/(E+J**2)*math.sqrt(H*I/E+J**2/4),0)
		C2 = min(D+J/(E+J**2)*math.sqrt(H*I/E+J**2/4),1)
		D = str(D*100).split('.')[0] + '%'
		if len(D) == 2: D = f'0{D}'
		C1 = str(C1*100).split('.')[0] + '%'
		if len(C1) == 2: C1 = f'0{C1}'
		C2 = str(C2*100).split('.')[0] + '%'
		if len(C2) == 2: C2 = f'0{C2}'
		compWRs.append((comp, D, E, C1, C2))
		
	compWRs.sort(key=lambda x:(x[3], x[1], x[2]), reverse=True)
	open(f'{basedir2}compWRs.csv', 'w').write(f'Composition,v{patch} Winrate,v{patch} Match Count,Confidence Interval -,Confidence Interval +\n' + str(compWRs).replace('"' , "'").replace("'), ('" , "\n").replace(", " , ",").replace("'," , ",").replace(",'" , ",")[3:-3])
				
	sheet = gc.open_by_key(googlesheetid)
	while True:
		try:
			sheet.values_update(
				'By Composition',
				params={'valueInputOption': 'USER_ENTERED'},
				body={'values': list(csv.reader(open(f'{basedir2}compWRs.csv')))})
		except Exception as e:
			if 'Quota exceeded for quota group' not in str(e):
				print(e)
				sys.exit()
			gcn += 1
			gc = gcs[gcn]
			sheet = gc.open_by_key(googlesheetid)
			continue
		break

	enemyWRs = []
	for item, enemymatchcount in enemymatchcount.items():
		D = (enemymatchcount - enemywincount[item]) / enemymatchcount
		E = enemymatchcount
		H = D*E
		I = E-H
		J = 2.5758293035489
		C1 = max(D-J/(E+J**2)*math.sqrt(H*I/E+J**2/4),0)
		C2 = min(D+J/(E+J**2)*math.sqrt(H*I/E+J**2/4),1)
		D = str(D*100).split('.')[0] + '%'
		if len(D) == 2: D = f'0{D}'
		C1 = str(C1*100).split('.')[0] + '%'
		if len(C1) == 2: C1 = f'0{C1}'
		C2 = str(C2*100).split('.')[0] + '%'
		if len(C2) == 2: C2 = f'0{C2}'
		enemyWRs.append((item, D, E, C1, C2))

	enemyWRs.sort(key=lambda x:(x[3], x[1], x[2]), reverse=True)
	enemyWRs.sort(key=lambda x:(x[0].split(',')[0]))
	open(f'{basedir2}enemyWRs.csv', 'w').write(f'1st Champion,2nd Champion,v{patch} 2nd Champion Winrate,v{patch} Match Count,Confidence Interval -,Confidence Interval +\n' + str(enemyWRs).replace('"' , "'").replace("'), ('" , "\n").replace(", " , ",").replace("'," , ",").replace(",'" , ",")[3:-3])

	sheet = gc.open_by_key(googlesheetid)
	while True:
		try:
			sheet.values_update(
				'By Enemy Champion',
				params={'valueInputOption': 'USER_ENTERED'},
				body={'values': list(csv.reader(open(f'{basedir2}enemyWRs.csv')))})
		except Exception as e:
			if 'Quota exceeded for quota group' not in str(e):
				print(e)
				sys.exit()
			gcn += 1
			gc = gcs[gcn]
			sheet = gc.open_by_key(googlesheetid)
			continue
		break
		
	WRs = []
	for i1, i2 in matchcount.items():
		winrate = str(wincount[i1] / i2)[:4]
		WRs.append((i1, float(winrate), i2))
	talentwinrates = []
	diamondpustalentwinrates = []
	rankwinrates = []
	mapwinrates = []
	skinwinrates = []
	avgrankwinrates = {}

	for i in WRs:
		D = i[1]
		E = i[2]
		H = D*E
		I = E-H
		J = 2.5758293035489
		C1 = max(D-J/(E+J**2)*math.sqrt(H*I/E+J**2/4),0)
		C2 = min(D+J/(E+J**2)*math.sqrt(H*I/E+J**2/4),1)
		D = str(i[1]*100).split('.')[0] + '%'
		C1 = str(C1*100).split('.')[0] + '%'
		C2 = str(C2*100).split('.')[0] + '%'
		if '#' in i[0]: skinwinrates.append((i[0].replace('#', ''), D, E, C1, C2))
		elif 'Ranked' in i[0]: mapwinrates.append((cclass[i[0].split(',')[0]] + f',{i[0]}'.replace('Ranked ',''), D, E, C1, C2)) 
		elif any(f',{r}' in i[0] for r in rankindex): rankwinrates.append((cclass[i[0].split(',')[0]] + f',{i[0]}', D, E, C1, C2))
		elif any(r == i[0] for r in rankindex): avgrankwinrates[i[0]] = str(i[1]*100).split('.')[0] + '%'
		elif i[0].startswith('Diamond+,'):
			i0 = i[0].replace('Diamond+,', '')
			if i0 == 'Grohk,Maelstrom': cc = 'Damage'
			elif i0 == 'Pip,Catalyst': cc =  'Flank'
			elif i0 == 'Skye,Smoke and Dagger': cc =  'Support'
			else: cc= cclass[i0.split(",")[0]]
			diamondpustalentwinrates.append((cc, i0, D, E, C1, C2))
		else:
			if i[0] == 'Grohk,Maelstrom': cc = 'Damage'
			elif i[0] == 'Pip,Catalyst': cc =  'Flank'
			elif i[0] == 'Skye,Smoke and Dagger': cc =  'Support'
			else: cc= cclass[i[0].split(",")[0]]
			talentwinrates.append((cc, i[0], D, E, C1, C2))

	skinwinrates.sort(key=lambda x:(x[3], x[1], x[2]), reverse=True)
	skinwinrates.sort(key=lambda x: x[0].split(',')[0])
	mapwinrates.sort(key=lambda x:(x[3], x[1], x[2]), reverse=True)
	mapwinrates.sort(key=lambda x: x[0].split(',')[0] + x[0].split(',')[1])
	rankwinrates.sort(key=lambda x:(x[3], x[1], x[2]), reverse=True)
	rankwinrates.sort(key=lambda x: x[0].split(',')[0] + x[0].split(',')[1])
	talentwinrates.sort(key=lambda x:(x[4], x[2], x[3]), reverse=True)
	talentwinrates.sort(key=lambda x: x[0])
	diamondpustalentwinrates.sort(key=lambda x:(x[4], x[2], x[3]), reverse=True)
	diamondpustalentwinrates.sort(key=lambda x: x[0])

	open(f'{basedir2}skinWRs.csv', 'w').write(f'Champion,Skin,v{patch} Winrate,v{patch} Match Count,Confidence Interval -,Confidence Interval +\n' + str(skinwinrates).replace('"' , "'").replace("'), ('" , "\n").replace(", " , ",").replace("'," , ",").replace(",'" , ",")[3:-3])

	sheet = gc.open_by_key(googlesheetid)
	while True:
		try:
			sheet.values_update(
				'By Skin',
				params={'valueInputOption': 'USER_ENTERED'},
				body={'values': list(csv.reader(open(f'{basedir2}skinWRs.csv')))})
		except Exception as e:
			if 'Quota exceeded for quota group' not in str(e):
				print(e)
				sys.exit()
			gcn += 1
			gc = gcs[gcn]
			sheet = gc.open_by_key(googlesheetid)
			continue
		break

	open(f'{basedir2}mapWRs.csv', 'w').write(f'Class,Champion,Map,v{patch} Winrate,v{patch} Match Count,Confidence Interval -,Confidence Interval +\n' + str(mapwinrates).replace('"' , "'").replace("'), ('" , "\n").replace(", " , ",").replace("'," , ",").replace(",'" , ",")[3:-3])

	sheet = gc.open_by_key(googlesheetid)
	while True:
		try:
			sheet.values_update(
				'By Map',
				params={'valueInputOption': 'USER_ENTERED'},
				body={'values': list(csv.reader(open(f'{basedir2}mapWRs.csv')))})
		except Exception as e:
			if 'Quota exceeded for quota group' not in str(e):
				print(e)
				sys.exit()
			gcn += 1
			gc = gcs[gcn]
			sheet = gc.open_by_key(googlesheetid)
			continue
		break

	rankwinrates = str(rankwinrates).replace('"' , "'").replace("'), ('" , "\n").replace(", " , ",").replace("'," , ",").replace(",'" , ",")[3:-3]
	for r in ['Qualifying', 'Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond', 'Master', 'All Ranks']: rankwinrates = rankwinrates.replace(r, f'{r}: {avgrankwinrates[r]}')
	open(f'{basedir2}rankWRs.csv', 'w').write(f'Class,Champion,Player Rank: its average winrate,v{patch} Champion Winrate,v{patch} Match Count,Confidence Interval -,Confidence Interval +\n' + rankwinrates)

	sheet = gc.open_by_key(googlesheetid)
	while True:
		try:
			sheet.values_update(
			'By Player Rank',
			params={'valueInputOption': 'USER_ENTERED'},
			body={'values': list(csv.reader(open(f'{basedir2}rankWRs.csv')))})
		except Exception as e:
			if 'Quota exceeded for quota group' not in str(e):
				print(e)
				sys.exit()
			gcn += 1
			gc = gcs[gcn]
			sheet = gc.open_by_key(googlesheetid)
			continue
		break

	open(f'{basedir2}talentWRs.csv', 'w').write(f'{otherversion}\nSource Code: github.com/Aevann1/PaladinsWinrates\nClass,Champion,Talent,v{patch} Winrate,v{patch} Match Count,Confidence Interval -,Confidence Interval +\n' + str(talentwinrates).replace('"' , "'").replace("'), ('" , "\n").replace(", " , ",").replace("'," , ",").replace(",'" , ",")[3:-3])

	sheet = gc.open_by_key(googlesheetid)
	while True:
		try:
			sheet.values_update(
				'Champion Winrates By Talent (All Ranks)',
				params={'valueInputOption': 'USER_ENTERED'},
				body={'values': list(csv.reader(open(f'{basedir2}talentWRs.csv')))})
		except Exception as e:
			if 'Quota exceeded for quota group' not in str(e): print(e)
			gcn += 1
			gc = gcs[gcn]
			sheet = gc.open_by_key(googlesheetid)
			continue
		break

	sheet = gc.open_by_key(googlesheetid).worksheet('Champion Winrates By Talent (All Ranks)')
	while True:
		try:
			format_cell_range(sheet, 'A1:Z3', cellFormat(textFormat=textFormat(bold=True)))
			format_cell_range(sheet, f'B4:B{sheet.row_count}', cellFormat(textFormat=textFormat(bold=False)))
		except Exception as e:
			if 'Quota exceeded for quota group' not in str(e):
				print(e)
				sys.exit()
			gcn += 1
			gc = gcs[gcn]
			sheet = gc.open_by_key(googlesheetid).worksheet('Champion Winrates By Talent (All Ranks)')
			continue
		break


	sheet = gc.open_by_key(googlesheetid).worksheet('Champion Winrates By Talent (All Ranks)')
	n = 1
	cnames = ''
	for val in gc.open_by_key(googlesheetid).worksheet('Champion Winrates By Talent (All Ranks)').col_values(2):
		while True:
			try:
				if val in 'GrohkPipSkye': val = sheet.acell(f'A{n}').value + val
				if val not in cnames:
					format_cell_range(sheet, f'B{n}:B{n}', cellFormat(textFormat=textFormat(bold=True)))
					cnames += f'{val},'
			except Exception as e:
				if 'Quota exceeded for quota group' not in str(e):
					print(e)
					sys.exit()
				gcn += 1
				gc = gcs[gcn]
				sheet = gc.open_by_key(googlesheetid).worksheet('Champion Winrates By Talent (All Ranks)')
				continue
			n += 1
			break

	diawr = (wincount['Diamond'] + wincount['Master']) / (matchcount['Diamond'] + matchcount['Master'])
	diawr = str(diawr*100).split('.')[0] + '%'
	open(f'{basedir2}diamondplustalentWRs.csv', 'w').write(f'Average Diamond+ winrate for all champions and talents: {diawr}\nClass,Champion,Talent,v{patch} Winrate,v{patch} Match Count,Confidence Interval -,Confidence Interval +\n' + str(diamondpustalentwinrates).replace('"' , "'").replace("'), ('" , "\n").replace(", " , ",").replace("'," , ",").replace(",'" , ",")[3:-3])

	sheet = gc.open_by_key(googlesheetid)
	while True:
		try:
			sheet.values_update(
			'By Talent (Diamond+)',
			params={'valueInputOption': 'USER_ENTERED'},
			body={'values': list(csv.reader(open(f'{basedir2}diamondplustalentWRs.csv')))})
		except Exception as e:
			if 'Quota exceeded for quota group' not in str(e): print(e)
			gcn += 1
			gc = gcs[gcn]
			sheet = gc.open_by_key(googlesheetid)
			continue
		break

	sheet = gc.open_by_key(googlesheetid).worksheet('By Talent (Diamond+)')
	while True:
		try:
			format_cell_range(sheet, 'A1:Z2', cellFormat(textFormat=textFormat(bold=True)))
			format_cell_range(sheet, f'B3:B{sheet.row_count}', cellFormat(textFormat=textFormat(bold=False)))
		except Exception as e:
			if 'Quota exceeded for quota group' not in str(e):
				print(e)
				sys.exit()
			gcn += 1
			gc = gcs[gcn]
			sheet = gc.open_by_key(googlesheetid).worksheet('By Talent (Diamond+)')
			continue
		break

	sheet = gc.open_by_key(googlesheetid).worksheet('By Talent (Diamond+)')
	n = 1
	cnames = ''
	for val in gc.open_by_key(googlesheetid).worksheet('By Talent (Diamond+)').col_values(2):
		while True:
			try:
				if val in 'GrohkPipSkye': val = sheet.acell(f'A{n}').value + val
				if val not in cnames:
					format_cell_range(sheet, f'B{n}:B{n}', cellFormat(textFormat=textFormat(bold=True)))
					cnames += f'{val},'
			except Exception as e:			
				if 'Quota exceeded for quota group' not in str(e):
					print(e)
					sys.exit()
				gcn += 1
				gc = gcs[gcn]
				sheet = gc.open_by_key(googlesheetid).worksheet('By Talent (Diamond+)')
				continue
			n += 1
			break

while True:
	t = str(datetime.datetime.now(pytz.timezone('UTC')).strftime('%Y%m%d%H%M%S'))
	while True:
		try:
			s = json.loads(requests.get(f'http://api.paladins.com/paladinsapi.svc/createsessionJson/{devid}/' + hashlib.md5((f'{devid}createsession{authkey}{t}').encode('utf-8')).hexdigest() + f'/{t}', timeout=10).content)['session_id']
			patch = json.loads(requests.get(f'http://api.paladins.com/paladinsapi.svc/getpatchinfoJson/{devid}/' + hashlib.md5((f'{devid}getpatchinfo{authkey}{t}').encode('utf-8')).hexdigest() + f'/{s}/{t}', timeout=10).content)['version_string']
			cclasses = enumerate(json.loads(requests.get(f'http://api.paladins.com/paladinsapi.svc/getchampionsjson/{devid}/' + hashlib.md5((f'{devid}getchampions{authkey}{t}').encode('utf-8')).hexdigest() + f'/{s}/{t}/1', timeout=10).content))
		except Exception as e: 
			print(e)
			continue
		break		
	cclass = {}
	for ln, lc in cclasses: cclass[lc['Name']] = lc['Roles'].replace('Paladins ', '').replace('Flanker', 'Flank').replace('Front Line', 'Frontline')
	date = datetime.datetime.now()
	if str(datetime.datetime.now().hour) in '0,1,2': date -= datetime.timedelta(days=2)
	else: date -= datetime.timedelta(days=1)
	date = date.date()
	for queue in ['428', '486']:
		print(queue)
		if queue == '486':
			googlesheetid = kbmgooglesheetid
			otherversion = f'Controller Version: docs.google.com/spreadsheets/d/{controllergooglesheetid}'
		else:
			googlesheetid = controllergooglesheetid
			otherversion = f'Keyboard & Mouse Version: docs.google.com/spreadsheets/d/{kbmgooglesheetid}'
		basedir2 = f'{ basedir1}/{patch} {queue} '
		if os.path.exists( f'{basedir2}matchcount.json'): day = open(f'{basedir2}matchcount.json').read()[:8]
		else: day = '20200109'
		day0 = datetime.datetime(int(day[:4]), int(day[4] + day[5]), int(day[-2:])).date() + datetime.timedelta(days=1)
		run = 0
		while day0 <= date:
			run = 1
			day = str(day0).replace('-', '')
			print(day)
			
			if os.path.exists( f'{basedir2}matchcount.json'):
				matchcount = json.loads(open( f'{basedir2}matchcount.json').read()[8:])
				wincount = json.loads(open(f'{basedir2}wincount.json').read())
				cardmatchcount = json.loads(open(f'{basedir2}cardmatchcount.json').read())
				cardwincount = json.loads(open(f'{basedir2}cardwincount.json').read())
				itemmatchcount = json.loads(open(f'{basedir2}itemmatchcount.json').read())
				itemwincount = json.loads(open(f'{basedir2}itemwincount.json').read())
				compmatchcount = json.loads(open(f'{basedir2}compmatchcount.json').read())
				compwincount = json.loads(open(f'{basedir2}compwincount.json').read())
				enemymatchcount = json.loads(open(f'{basedir2}enemymatchcount.json').read())
				enemywincount = json.loads(open(f'{basedir2}enemywincount.json').read())
				dps = json.loads(open(f'{basedir2}dps.json').read())
				hps = json.loads(open(f'{basedir2}hps.json').read())
				sps = json.loads(open(f'{basedir2}sps.json').read())
				avgmatchcount = json.loads(open(f'{basedir2}avgmatchcount.json').read())
			else:
				matchcount = {}
				wincount = {}
				cardmatchcount = {}
				cardwincount = {}
				itemmatchcount = {}
				itemwincount = {}
				compmatchcount = {}
				compwincount = {}
				enemymatchcount = {}
				enemywincount = {}
				dps = {}
				hps = {}
				sps = {}
				avgmatchcount = {}

			bancount = {}
			pickcount = {}
			ratematchcount = 0
			t = str(datetime.datetime.now(pytz.timezone('UTC')).strftime('%Y%m%d%H%M%S'))
			while True:
				try: matches = str(requests.get(f'http://api.paladins.com/paladinsapi.svc/getmatchidsbyqueuejson/{devid}/' + hashlib.md5((f'{devid}getmatchidsbyqueue{authkey}{t}').encode('utf-8')).hexdigest() + f'/{s}/{t}/{queue}/{day}/{hour}', timeout=10).content)
				except Exception as e: 
					print(e)
					continue
				break				

			n = len(list(re.finditer('Match":"(.*?)"', matches)))
			x = 0
			m = ''
			for i in re.finditer('Match":"(.*?)"', matches):
				x += 1
				m += f'{i.group(1)},'
				if str(x).endswith('0') or x == n:
					t = str(datetime.datetime.now(pytz.timezone('UTC')).strftime('%Y%m%d%H%M%S'))
					while True:
						try: mdata = requests.get(f'http://api.paladins.com/paladinsapi.svc/getmatchdetailsbatchjson/{devid}/' + hashlib.md5((f'{devid}getmatchdetailsbatch{authkey}{t}').encode('utf-8')).hexdigest() + f'/{s}/{t}/{m}'[:-1], timeout=10).content[1:-1].decode('utf-8')
						except Exception as e: 
							print(e)
							continue
						break
					m = ''
					print(f'{x}/{n}')
					D = 0
					F = 0
					S = 0
					T = 0
					playernumber = 0
					li = list(mdata.split(',{"Account_Level'))
						
					for player in li:
						if not player.startswith('{"Account_Level'): player = '{"Account_Level' + player
						player = json.loads(player)
						champ = player['Reference_Name'].replace('\\', '')
						if champ not in pickcount: pickcount[champ] = 0
						pickcount[champ] += 1
						if len(li) != 100: continue
						if str(playernumber)[-1:] == '0':
							for ban in ['Ban_1', 'Ban_2', 'Ban_3', 'Ban_4']:
								ban = player[ban]
								if ban not in bancount: bancount[ban] = 0
								bancount[ban] += 1
							ratematchcount += 1
						playernumber += 1
						
						if player['Item_Purch_6'] == 'Maelstrom': cc = 'Damage'
						elif player['Item_Purch_6'] == 'Catalyst': cc =  'Flank'
						elif player['Item_Purch_6'] == 'Smoke and Dagger': cc =  'Support'
						else: cc = cclass[champ]
						if cc == 'Damage': D += 1
						if cc == 'Flank': F += 1
						if cc == 'Support': S += 1
						if cc == 'Frontline': T += 1
						if playernumber % 5 == 0:
							comp = f'{D}D-{F}F-{S}S-{T}T'
							if comp not in compmatchcount:
								compmatchcount[comp] = 0
								compwincount[comp] = 0
							compmatchcount[comp] += 1
							if player['Win_Status'] == 'Winner': compwincount[comp] += 1
							D = 0
							F = 0
							S = 0
							T = 0
						
						if player['Item_Purch_6'] == '': continue
						champtalent = f'{champ},' + player['Item_Purch_6'].replace(',' , '').replace('\\', '')
						if champtalent not in hps:
							dps[champtalent] = 0
							hps[champtalent] = 0
							sps[champtalent] = 0
							avgmatchcount[champtalent] = 0
						dps[champtalent] += player['Damage_Player'] / player['Time_In_Match_Seconds']
						hps[champtalent] += player['Healing'] / player['Time_In_Match_Seconds']
						sps[champtalent] += player['Damage_Mitigated'] / player['Time_In_Match_Seconds']
						avgmatchcount[champtalent] += 1
						
						batchnumber = playernumber - (playernumber % 10)
						if str(playernumber)[-1:] not in '6,7,8,9,0':
							for lin in [5,6,7,8,9]:
								lin += batchnumber
								enemy = li[lin]
								if not enemy.startswith('{"Account_Level'): enemy = '{"Account_Level' + enemy
								enemy = json.loads(enemy)['Reference_Name']
								champandenemy = f'{champ},{enemy}'
								enemyandchamp = f'{enemy},{champ}'
								if champandenemy not in enemymatchcount:
									enemymatchcount[champandenemy] = 0
									enemywincount[champandenemy] = 0
									enemymatchcount[enemyandchamp] = 0
									enemywincount[enemyandchamp] = 0
								enemymatchcount[champandenemy] += 1
								enemymatchcount[enemyandchamp] += 1
								if player['Win_Status'] == 'Winner': enemywincount[champandenemy] += 1
								
						if champ not in cardmatchcount:
							cardmatchcount[champ] = {}
							cardwincount[champ] = {}
						cn = 0
						for card in [player['Item_Purch_1'], player['Item_Purch_2'], player['Item_Purch_3'], player['Item_Purch_4'], player['Item_Purch_5']]:
							cn += 1
							card += ',' + str(player[f'ItemLevel{cn}'])
							if card not in cardmatchcount[champ]:
								cardmatchcount[champ][card] = 0
								cardwincount[champ][card] = 0
							cardmatchcount[champ][card] += 1
							if player['Win_Status'] == 'Winner': cardwincount[champ][card] += 1
						
						for item in [player['Item_Active_1'], player['Item_Active_2'], player['Item_Active_3'], player['Item_Active_4']]:
							if item == '': break
							item = f'{champ},{item}'
							if item not in itemmatchcount:
								itemmatchcount[item] = 0
								itemwincount[item] = 0
							itemmatchcount[item] += 1
							if player['Win_Status'] == 'Winner': itemwincount[item] += 1

						champrank = f"{champ},{rankindex[player['League_Tier']]}"
						champallranks = f'{champ},All Ranks'
						champmap = f"{champ},{player['Map_Game']}"
						skin = player['Skin'].replace('\\', '').replace(f' {champ}', '')
						champskin = f'{champ},#{skin}'
						rank = rankindex[player['League_Tier']]
						if champtalent not in matchcount: matchcount[champtalent] = 0
						if champtalent not in wincount: wincount[champtalent] = 0
						if champrank not in matchcount: matchcount[champrank] = 0
						if champrank not in wincount: wincount[champrank] = 0
						if champallranks not in matchcount: matchcount[champallranks] = 0
						if champallranks not in wincount: wincount[champallranks] = 0
						if champmap not in matchcount: matchcount[champmap] = 0
						if champmap not in wincount: wincount[champmap] = 0
						if champskin not in matchcount: matchcount[champskin] = 0
						if champskin not in wincount: wincount[champskin] = 0
						if rank not in matchcount: matchcount[rank] = 0
						if rank not in wincount: wincount[rank] = 0
						matchcount[champtalent] += 1
						matchcount[champrank] += 1
						matchcount[champallranks] += 1
						matchcount[champmap] += 1
						matchcount[champskin] += 1
						matchcount[rank] += 1
						matchcount['All Ranks'] += 1
						if rank == 'Diamond' or rank == 'Master':
							rankchamptalent = f'Diamond+,{champtalent}'
							if rankchamptalent not in matchcount: matchcount[rankchamptalent] = 0
							if rankchamptalent not in wincount: wincount[rankchamptalent] = 0
							matchcount[rankchamptalent] += 1
						if player['Win_Status'] == 'Winner':
							wincount[champtalent] += 1
							wincount[champrank] += 1
							wincount[champallranks] += 1
							wincount[champmap] += 1
							wincount[champskin] += 1
							wincount[rank] += 1
							wincount['All Ranks'] += 1
							if rank == 'Diamond' or rank == 'Master': wincount[rankchamptalent] += 1
								
			while True:
				try: print(str(requests.get(f'http://api.paladins.com/paladinsapi.svc/getdatausedjson/{devid}/' + hashlib.md5((f'{devid}getdataused{authkey}{t}').encode('utf-8')).hexdigest() + f'/{s}/{t}', timeout=10).content))
				except Exception as e: 
					print(e)
					continue
				break							
			
			if hour == '-1':
				open(f'{basedir2}matchcount.json', 'w').write(str(day) +  json.dumps(matchcount))
				open(f'{basedir2}wincount.json', 'w').write(json.dumps(wincount))
				open(f'{basedir2}cardmatchcount.json', 'w').write(json.dumps(cardmatchcount))
				open(f'{basedir2}cardwincount.json', 'w').write(json.dumps(cardwincount))
				open(f'{basedir2}itemmatchcount.json', 'w').write(json.dumps(itemmatchcount))
				open(f'{basedir2}itemwincount.json', 'w').write(json.dumps(itemwincount))
				open(f'{basedir2}compmatchcount.json', 'w').write(json.dumps(compmatchcount))
				open(f'{basedir2}compwincount.json', 'w').write(json.dumps(compwincount))
				open(f'{basedir2}enemymatchcount.json', 'w').write(json.dumps(enemymatchcount))
				open(f'{basedir2}enemywincount.json', 'w').write(json.dumps(enemywincount))
				open(f'{basedir2}dps.json', 'w').write(json.dumps(dps))
				open(f'{basedir2}hps.json', 'w').write(json.dumps(hps))
				open(f'{basedir2}sps.json', 'w').write(json.dumps(sps))
				open(f'{basedir2}avgmatchcount.json', 'w').write(json.dumps(avgmatchcount))

				backupdir = f'{basedir1}/paladinswinrates data backup/'
				if not os.path.exists(backupdir): os.mkdir(backupdir)
				open(f'{backupdir}matchcount {day}.json', 'w').write(str(day) +  json.dumps(matchcount))
				open(f'{backupdir}wincount {day}.json', 'w').write(json.dumps(wincount))
				open(f'{backupdir}cardmatchcount {day}.json', 'w').write(json.dumps(cardmatchcount))
				open(f'{backupdir}cardwincount {day}.json', 'w').write(json.dumps(cardwincount))
				open(f'{backupdir}itemmatchcount {day}.json', 'w').write(json.dumps(itemmatchcount))
				open(f'{backupdir}itemwincount {day}.json', 'w').write(json.dumps(itemwincount))
				open(f'{backupdir}compmatchcount {day}.json', 'w').write(json.dumps(compmatchcount))
				open(f'{backupdir}compwincount {day}.json', 'w').write(json.dumps(compwincount))
				open(f'{backupdir}enemymatchcount {day}.json', 'w').write(json.dumps(enemymatchcount))
				open(f'{backupdir}enemywincount {day}.json', 'w').write(json.dumps(enemywincount))
				open(f'{backupdir}dps.json', 'w').write(json.dumps(dps))
				open(f'{backupdir}hps.json', 'w').write(json.dumps(hps))
				open(f'{backupdir}sps.json', 'w').write(json.dumps(sps))
				open(f'{backupdir}avgmatchcount.json', 'w').write(json.dumps(avgmatchcount))
			calcandpost()
			day0 += datetime.timedelta(days=1)
		
		if run == 0: calcandpost()
	wakeuptime = datetime.datetime.now().replace(hour=3, minute=0)
	if str(datetime.datetime.now().hour) not in '0,1,2': wakeuptime += datetime.timedelta(days=1)
	print(f'Sleeping until {wakeuptime}')
	time.sleep((wakeuptime - datetime.datetime.now()).total_seconds())