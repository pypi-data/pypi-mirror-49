import requests as rq
import json, shutil

class monitoring2:
	def __init__(self, login, password, url = 'http://taxplayer.ensyco.local', crpt = False):
		self.URL = url
		self.login = login
		self.__password = password
		if crpt: self.__password = self.crypt(password)
		self.log = []
		self.mon_sess()

	def crypt(self, pas):
		password=''
		for x in pas:
			if ord(x)-len(pas)<32: password+= chr(ord(x)-len(pas)+96)
			else: password+=chr(ord(x)-len(pas))
		return password

	def logger(self, text):
		self.log.append(text)
		self.log.append(self.r.status_code)
		print(text, self.r.status_code)
		if self.r.status_code == 200:
			return self.r.json()
		else: 
			return self.r.status_code		

	def mon_sess(self):
		self.ms = rq.Session()
		json = {"username":self.login,"password":self.__password}
		self.r = self.ms.post('{}/api/login'.format(self.URL), json = json)
		self.ms.headers.update({'Authorization': self.r.json()['token'], 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36', 'Connection':'keep-alive'})
		return self.logger('Авторизация в мониторинге...')

	def seek_by_inn(self, inn, rows = 50, page = 1, sidx = 'orgId', sord = 'desc'):
		form = {'rows' : rows, 'page' : page , 'sidx' : sidx, 'sord' : sord, 'orgTag' : inn}
		self.r = self.ms.post('{}/api/organisations/filter'.format(self.URL), data=form)
		return self.logger('Поиск организации {}...'.format(inn))

	def seek_by_orgId(self, orgId):
		self.r = self.ms.get('{}/api/organisations/{}'.format(self.URL, orgId))
		return self.logger('Поиск организации id {}...'.format(orgId))

	def seek_by_contract(self, contract):
		self.r = self.ms.get('{}/api/organisations/byContract?id={}'.format(self.URL, contract))
		return self.logger('Поиск организации с договором {}...'.format(contract))

	def seek_kkm(self, kkm):
		self.r = self.ms.get('{}/api/kkms/find?query={}'.format(self.URL, kkm))
		return self.logger('Поиск ККТ {}...'.format(kkm))

	def seek_transaction(self, transaction):
		self.r = self.ms.get('{}/api/tickets/transaction/{}'.format(self.URL, transaction))
		return self.logger('Поиск транзакции {}...'.format(transaction))

	def create_report(self, *, clazz, distributionList, inns, scheduleDate, fromDate, toDate, kkmIdlePeriod = 259200, priority = 1000):
		form = {"clazz":clazz ,"distributionList":distributionList,"inns":inns,"kkmIdlePeriod":kkmIdlePeriod,"priority":priority,"scheduleDate":scheduleDate,"fromDate":fromDate,"toDate":toDate}
		self.r = self.ms.post('{}/api/reports/generate'.format(self.URL), json=form)
		return self.logger('Планирование отчёта по {}...'.format(inns))

	def get_report_info(self, uuid):
		self.r = self.ms.get('{}/api/reports/{}'.format(self.URL, uuid))
		return self.logger('Поиск отчёта {}...'.format(uuid))

	def download_report(self, *, uuid, file):
		fullpath = '{}/api/reports/{}/download'.format(self.URL, uuid)
		filereq = self.ms.get(fullpath,stream = True)
		with open(file,"wb") as receive:
			shutil.copyfileobj(filereq.raw,receive)
		del filereq

	def cancel_report(self, uuid):
		self.r = self.ms.get('{}/api/reports/{}/cancel'.format(self.URL, uuid))
		return self.logger('Отмена отчёта {}...'.format(uuid))

	def ctrl(self, org_id ,ctrl_login):
		form = {"orgId" : org_id, 'serviceLogin' : ctrl_login}
		self.r = self.ms.post('{}/api/organisations/assign'.format(self.URL), json=form)
		return self.logger('Контролимся к {}...'.format(org_id))