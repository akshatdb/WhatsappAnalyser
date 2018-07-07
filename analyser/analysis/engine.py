import sys
import re
import numpy as np
import datetime
fillers = [' ki ',' ka ',' ke ',' nhi ',' nahi ',' ye ',' hai ',' mein ',' se ',' hi ',' ha ',' ho ',' bhi ',' vo ',' aur ',' Ye ',' kya ',' ab ',' ra ', ' jo ', ' ko ', ' pe ', ' ne ', ' le ', ' lo ', ' wo ', ' hmm ', ' hum ', ' abhi ' , ' ek ', ' na ', ' ni ', ' mai ', ' abe ', ' mai ', ' tm ' , ' ab ', ' hua ', ' tum ', ' tha ']
fillers = fillers + [" " + i[1:].capitalize() for i in fillers]
def findAlias(name):
	return name

def breakdown(message, exp, timere, datere):
	try:
		datetime = exp.match(message).group()
	except:
		return 11, message, 0, 0, 0
	time = timere.findall(datetime)[0]
	date = datere.findall(datetime)[0]
	pos = message.index('-')
	tmp = message[pos+1:]
	try:
		colpos = tmp.index(':')
	except:
		q = tmp.find('left')
		if q >= 0:
			return 10,tmp[:q],0,0,0
		else:
			q = tmp.find('added')
			if q >= 0:
				return 1,tmp[1:q-1],tmp[q+6:-2],0,0
			else:
				q = tmp.find('removed')
				if q >= 0:
					return 2,tmp[:q],tmp[q+8:-2],0,0
				else:
					q = tmp.find("changed the subject")
					if q >= 0:
						t = tmp.find('" to "')
						return 3,tmp[1:q-1], tmp[q+26:t],tmp[t+6:-3],0
					else:
						q = tmp.find("changed their phone number")
						if q >= 0:
							return 4,tmp[:q], tmp[q:-1],0,0
						else:
							q = tmp.find("changed this group's icon")
							if q >= 0:
								return 5,tmp[:q], tmp[q:-1],0,0
							else:
								q = tmp.find("admin")
								if q >= 0:
									return 6,tmp[:q], tmp[q:-1],0,0
								else:
									q = tmp.find("changed to")
									if q >= 0:
										return 7,tmp[:q], tmp[q:-1],0,0
									else:
										q = tmp.find("deleted this group's icon")
										if q >= 0:
											return 8,tmp[:q], tmp[q:-1],0,0
										else:
											q = tmp.find("changed the group description")
											if q >= 0:
												return 9,tmp[:q], tmp[q:-1], 0,0
											else:
												q = tmp.find("revoked")
												if q>=0:
													return 11,tmp[:q], tmp[q:-1],0,0

	sender = tmp[1:colpos]
	body = tmp[colpos+1:]
	return False, date,time,findAlias(sender), body

def SenderMessageCountPlot(senderdict, senderlist):
	y = [len(senderdict[sender]) for sender in senderlist]
	names = [sender+'('+str(len(senderdict[sender])) + ')' for sender in senderlist]
	counts, names = zip(*sorted(zip(y, names)))
	return names, counts

def UsagePatternOverall(datemsgcount):
	y = [datemsgcount[key] for key in datemsgcount]
	x = [key for key in datemsgcount]
	return x, y

def UsagePatternDaywise(daycount):
	y = [daycount[str(day)] for day in range(7)]
	x = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
	return x, y
def UsagePatternDatewise(datecount):
	y = [datecount[str(d)] for d in range(1,32)]
	x = range(1,32)
	return x, y

def UsagePatternMonthWise(monthcount):
	y = [monthcount[str(d)] for d in range(1,13)]
	x = ['january','february','march','april','may','june','july','august','september','october','november','december']
	return x, y

def generateCombinedMessage(name, senderdict):
	m = ' '.join(senderdict[name])
	m = m.replace('\\n',' ')
	m = m.replace('<Media omitted>',' ')
	for filler in fillers:
		m = m.replace(filler,' ')
	pattern = re.compile("[\s]+")
	m = pattern.sub(' ', m)
	return m

def AllMessageFromAll(senderdict, senderlist):
	msgDict = {}
	for name in senderlist:
		msg = generateCombinedMessage(name, senderdict)		
		msgDict[name] = msg
	return msgDict

def create(text):

	timeFlag = 1
	text = unicode(text, 'utf-8')
	text = text.encode('unicode_escape')
	emoji_pattern = re.compile("\\\U000[0-9|A-F|a-f][0-9|A-F|a-f][0-9|A-F|a-f][0-9|A-F|a-f][0-9|A-F|a-f]")
	text = emoji_pattern.sub('', text)
	emoji_pattern = re.compile("\\\u[0-9|A-F|a-f][0-9|A-F|a-f][0-9|A-F|a-f][0-9|A-F|a-f]")
	text = emoji_pattern.sub('', text)
	emoji_pattern = re.compile("\\\\\\/x[0-9|A-F|a-f][0-9|A-F|a-f]")
	text = emoji_pattern.sub('', text)

	state = 0
	msg = []
	for i in range(len(text)):
		c = text[i]
		if state == 0:
			if c >= '0' and c<= '9':
				starti = i
				state = 1
		elif state == 1:
			if c >= '0' and c <= '9':
				state = 2
			elif c == '/':
				state = 3
			else:
				state = 0
		elif state == 2:
			if c == '/':
				state = 3
			else:
				state = 0
		elif state == 3:
			if c >= '0' and c <= '9':
				state = 4
			else:
				state = 0
		elif state == 4:
			if c >= '0' and c <= '9':
				state = 5
			elif c == '/':
				state = 6
			else:
				state = 0
		elif state == 5:
			if c == '/':
				state = 6
			else:
				state = 0
		elif state == 6:
			if c >= '0' and c <= '9':
				state = 7
			else:
				state = 0 
		elif state == 7:
			if c >= '0' and c <= '9':
				state = 8
			else:
				state = 0
		elif state == 8:
			state = 0
			msg.append(starti)
	if timeFlag == 1:
		exp = re.compile("\d{1,2}\/\d{1,2}\/\d\d\d\d, \d{1,2}:\d{1,2}")
		datere = re.compile("\d{1,2}\/\d{1,2}\/\d\d\d\d")
		timere = re.compile("\d{1,2}:\d{1,2}")
	else:
		exp = re.compile("\d{1,2}\/\d{1,2}\/\d\d, \d{1,2}:\d{1,2} [AP]M")
		datere = re.compile("\d{1,2}\/\d{1,2}\/\d\d")
		timere = re.compile("\d{1,2}:\d{1,2} [AP]M")
	senderlist = []
	senderdict = {}
	datemsgcount = {}
	timemsgcount = {}
	timedict = {}
	datedict = {}
	leftdict = {}
	addeddict = {}
	removeddict = {}
	subjectdict = {}
	pchangict = {}
	icondict = {}
	admin = {}
	channum = {}
	changedesc = {}
	daycount = {
		'0':0,
		'1':0,
		'2':0,
		'3':0,
		'4':0,
		'5':0,
		'6':0,
	}
	datecount = {
		'1':0,
		'2':0,
		'3':0,
		'4':0,
		'5':0,
		'6':0,
		'7':0,
		'8':0,
		'9':0,
		'10':0,
		'11':0,
		'12':0,
		'13':0,
		'14':0,
		'15':0,
		'16':0,
		'17':0,
		'18':0,
		'19':0,
		'20':0,
		'21':0,
		'22':0,
		'23':0,
		'24':0,
		'25':0,
		'26':0,
		'27':0,
		'28':0,
		'29':0,
		'30':0,
		'31':0,
	}
	monthcount = {
		'1':0,
		'2':0,
		'3':0,
		'4':0,
		'5':0,
		'6':0,
		'7':0,
		'8':0,
		'9':0,
		'10':0,
		'11':0,
		'12':0,
	}
	if timeFlag == 1:
		yearcount = {
			'2015':0,
			'2016':0,
			'2017':0,
			'2018':0
		}
	else:
		yearcount = {
			'15':0,
			'16':0,
			'17':0,
			'18':0
		}

	for i in range(len(msg)-1):
		message = text[msg[i]:msg[i+1]]
		leftFlag, date, time, sender, body = breakdown(message, exp, timere, datere)
		if leftFlag == 10:
			name = date
			try:
				leftdict[name] = leftdict[name]+1
			except:
				leftdict[name] = 1
			continue
		elif leftFlag == 1:
			adder = date
			added = time
			added = added.split(' , ')
			if added[-1].find(' and ') >= 0:
				tmp = added[-1].split(' and ')
				added[-1] = tmp[0]
				added.append(tmp[1])
			for ad in added:
				try:
					tmp = addeddict[ad]
					tmp.append(adder)
					addeddict[ad] = tmp
				except:
					addeddict[ad] = [adder]
			continue
		elif leftFlag == 2:
			remover = date
			removed = time
			removed = removed.split(' , ')
			if removed[-1].find(' and ') >= 0:
				tmp = removed[-1].split(' and ')
				removed[-1] = tmp[0]
				removed.append(tmp[1])
			for rem in removed:
				try:
					tmp = removeddict[rem]
					tmp.append(remover)
					removeddict[rem] = tmp
				except:
					removeddict[rem] = [remover]
			continue
		elif leftFlag == 3:
			changedby = date
			subjectfrom = time
			subjectto = sender
			try:
				tmp = subjectdict[subjectto]
				tmp[2] = tmp[2] + 1
				bylist = tmp[1]
				bylist.append(changedby)
				fromlist = tmp[0]
				fromlist.append(subjectfrom)
				subjectdict[subjectto] = [fromlist, bylist, tmp[2]]
			except:
				subjectdict[subjectto] = [[subjectfrom], [changedby], 1]
			continue
		elif leftFlag:
			continue
		try:
			tmp = senderdict[sender]
			tmp.append(body)
			senderdict[sender] = tmp
		except:
			senderlist.append(sender)
			senderdict[sender] = [body]
		try:
			timemsgcount[time] = timemsgcount[time] + 1
			tmp = timedict[time]
			tmp.append([sender, body])
			timedict[time] = tmp
		except:
			timedict[time] = [[sender, body]]
			timemsgcount[time] = 1
		if timeFlag == 1:
			day, month, year =  [int(d) for d in date.split('/')]
		else:
			month, day, year = [int(d) for d in date.split('/')]
		weekday = datetime.date(year, month, day).weekday()
		daycount[str(weekday)] = daycount[str(weekday)] + 1
		datecount[str(day)] = datecount[str(day)] + 1
		monthcount[str(month)] = monthcount[str(month)] + 1
		yearcount[str(year)] = yearcount[str(year)] + 1
		try:
			datemsgcount[date] = datemsgcount[date] + 1
			tmp = datedict[date]
			tmp.append([time, sender, body])
			datedict[date] = tmp
		except:
			datedict[date] = [[time, sender, body]]
			datemsgcount[date] = 1
	responseDict = {}
	responseDict['SenderMessageCountPlot'] = SenderMessageCountPlot(senderdict, senderlist)
	responseDict['UsagePatternOverall'] = UsagePatternOverall(datemsgcount)
	responseDict['UsagePatternDaywise'] = UsagePatternDaywise(daycount)
	responseDict['UsagePatternDatewise'] = UsagePatternDatewise(datecount)
	responseDict['UsagePatternMonthwise'] = UsagePatternMonthWise(monthcount)
	responseDict['NameMessages'] = AllMessageFromAll(senderdict, senderlist)
	responseDict['senderlist'] = senderlist
	return responseDict