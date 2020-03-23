import ssl
import json
import datetime
import logging

logger = logging.getLogger(__name__)

class Certificate(object):

	def __init__(self, domain):
		self.domain = domain
		self.cert = self.get()
	def get(self, timeout=3, port=443):
		""" Return SSL information in JSON format """
		logger.debug(f'Get SSL Certificate Informtion, site: {self.domain}')
		connector = ssl.create_connection((self.domain, port), timeout)
		context = ssl.create_default_context()
		sock = context.wrap_socket(connector, server_hostname=self.domain)
		cert = json.loads(json.dumps(sock.getpeercert()))
		logger.debug('Result')
		logger.debug(cert)
		connector.close()
		return cert
		
	def notBefore(self):
		logger.debug(f'notBefore: {self.cert["notBefore"]}')
		return self.cert["notBefore"]

	def notAfter(self):
		logger.debug(f'notAfter: {self.cert["notAfter"]}')
		return self.cert["notAfter"]

	def remaining(self):
		""" Return the number of remaining days of cert """
		gmt_datetime_format = r'%b %d %H:%M:%S %Y %Z'
		expire_datetime = datetime.datetime.strptime(self.notAfter(), gmt_datetime_format)
		current_datetime = datetime.datetime.utcnow()

		remaining = expire_datetime - current_datetime
		logger.debug(f'remaining: {remaining.days}')
		return remaining.days



