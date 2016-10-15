#coding=utf-8
from selenium import webdriver
import time
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Spider(object):
	#js="document.getElementsByClassName('profile-action  js-vote-action js-touchable')[0].click();"
	js=" var pArray = document.getElementsByTagName('p'); if (pArray.length > 0) console.log(window.location + ' ==== ' + pArray[0].innerHTML);"
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
	for i in range(158104262,158185777):
		try:
			mySpider.getHtml(i)
		except Exception,msg:
			fp=open('spider.log','a+')
			fp.write('PAGE_ID：%d，%s，%s\n'%(i,Exception,msg))
			fp.close()
			mySpider=Spider()
	print 'scan completed'
