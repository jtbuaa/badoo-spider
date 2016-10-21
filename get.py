#coding=utf-8
from selenium import webdriver
import time
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Spider(object):
	js="var gender=''; var rating=document.getElementsByClassName('js-hotness-rating-text'); if (rating.length>0) {var rating0=rating[0].innerHTML; if (rating0.indexOf('He ')>=0 || rating0.indexOf('him')>=0 || rating0.indexOf('他')>=0) gender='M'; else if (rating0.indexOf('She ')>=0 || rating0.indexOf('her')>=0 || rating0.indexOf('她')>=0) gender='F';} if (gender!='') {var myDate=new Date(); var output = myDate.toLocaleTimeString() + ' ' + window.location.toString().substr(28) + ' ' + gender + '===='; var pArray=document.getElementsByTagName('p'); if (pArray.length>0) output=output + pArray[0].innerHTML; console.log(output);}"
	driver=''
	def __init__(self):
		# save log to /tmp/log1, include url and profile introduction
		self.driver=webdriver.Chrome(executable_path="chromedriver", service_args=["--log-path=/tmp/log1", "--verbose"])
		return

	def getHtml(self,page_id):
		try:
			print 'scan %d %s\n'%(page_id,time.strftime('%X',time.localtime())),
			self.driver.get('https://m.badoo.com/profile/%d'%page_id)
			time.sleep(10)
			self.driver.execute_script(self.js)
		except:
			try:
				self.driver.switch_to_alert().dismiss()
			except:
				time.sleep(0.5)
				self.driver.switch_to_alert().accept()
			print ', abandon'

	def __del__(self):
		try:
			self.driver.quit()
		except:
			pass
		return

if __name__=='__main__':
	mySpider=Spider()
	# badoo keep user id secret unless you got matched with somebody.
	# as I know, another range is (5xxxxxxxx,5yyyyyyyy). but many ids are empty.
	for i in range(158131260,158185777):
		try:
			mySpider.getHtml(i)
		except Exception,msg:
			fp=open('spider.log','a+')
			fp.write('PAGE_ID：%d，%s，%s\n'%(i,Exception,msg))
			fp.close()
			mySpider=Spider()
	print 'scan completed'
