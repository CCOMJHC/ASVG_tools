#!/usr/bin/env python
#
#

import sys
import requests
import xml.etree.ElementTree as et
from bs4 import BeautifulSoup
import time
import datetime 

circuit_ids = ["RAILLOAD0","RAILLOAD1","RAILLOAD2","RAILLOAD3","RAILLOAD4"]
circuit_stat_ids = ["RAILENA0","RAILENA1","RAILENA2","RAILENA3","RAILENA4"]

class circuit():
	def __init__(self,cktname):
		self.updatetime = None
		self.cktname = cktname
		self.status = 0
		self.voltage = 0.0
		self.current = 0.0

	def power(self):
		return self.voltage * self.current

	def print_data(self):
		print("%s,%s,%s,%s,%s,%s" % (datetime.datetime.fromtimestamp(self.updatetime).isoformat(),self.updatetime,self.cktname,self.status,self.voltage,self.current))

class west_mountain_radio():

	def __init__(self,ip_address):
		self.url = "http://" + ip_address 
		self.circuits = []

	def get_names(self):

		# We use Beautiful soup to get the node names from the front page.
		r = requests.get(self.url)
		#r = requests.get("http://192.168.100.212")
		bs = BeautifulSoup(r.text)
		table = bs.find("table", attrs={"class":"info_table"})
		rows = table.find_all("tr")
		for row in rows:
			cols = row.find_all("td")
			if cols:
				rowname = str(cols[0].text.strip())
				if rowname != "Power Supply" and rowname != "":
					self.circuits.append(circuit(rowname))

	def get_status(self):
	
		# Gets the status xml page.
		r = requests.get(self.url + "/status.xml")
		#r = requests.get("http://192.168.100.212/status.xml")
		updatetime = time.time()
		bs = BeautifulSoup(r.text)
		items = bs.get_text().split('\n')
		voltage = items[1]
		current = items[2:7]
		status = items[7:]


		for i in range(self.circuits.__len__()):
			self.circuits[i].updatetime = updatetime
			self.circuits[i].voltage = voltage
			self.circuits[i].current = current[i]
			self.circuits[i].status = status[i]

	def print_status(self):
		print ""
		print "Status for " + self.url
		for c in self.circuits:
			c.print_data()

if __name__ == '__main__':

	if sys.argv[1] == '-h':
		print "Usage:"
		print "  ./west_mountain_radio 192.168.100.224"
		sys.exit()

	wmr = west_mountain_radio(sys.argv[1])
	wmr.get_names()
	wmr.get_status()
	wmr.print_status()
