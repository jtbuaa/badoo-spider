#coding=utf-8
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#driver=webdriver.Chrome('chromedriver')
class Spider(object):
	js='var x=document.body.scrollTop=document.body.scrollHeight'
	driver=''
	def __init__(self):
		# self.driver=webdriver.PhantomJS('../phantomjs')
		self.driver=webdriver.Chrome('chromedriver')
		return

	def getHtml(self,page_id):
		try:
			print 'scan %d'%page_id,
			self.driver.get('https://m.badoo.com/profile/%d'%page_id)
			self.driver.execute_script(self.js)
			time.sleep(10)
			html=self.driver.page_source
			if html.find('页面不存在')==-1:
				print ', got page source'
				return [1,html]
			else:
				print ', abandon'
		except:
			try:
				self.driver.switch_to_alert().accept()
			except:
				time.sleep(0.5)
				self.driver.switch_to_alert().accept()
			print '，abandon'
		return [0]

	def getData(self,page_id,html):
		conn=MySQLdb.connect(host='localhost', port=3306,user='root', passwd='1234', db='crawler', charset='utf8',)
		title=stt=''
		soup=BeautifulSoup(html,'lxml')
		dd=soup.find('dd')
		if dd.find(class_='dd_top'):
			title=dd.find(class_='dd_top').a['title']
		author=dd.find(class_='name').text
		view=dd.find(class_='ico_view').parent.get_text()
		des_num=soup.find(class_='des_num')
		start_date=des_num.find(class_='time').parent.get_text()[3:]
		time=des_num.find(class_='days').parent.get_text()[5:-1]
		money=des_num.find(class_='money').parent.get_text()[5:]
		if soup.find('ul',class_='object_list'):
			object_list=soup.find('ul',class_='object_list')
			li_list=object_list.find_all('li')
			for li in li_list:
				span=li.find_all('span')
				for item in span:
					stt+=item.text+'，'
			# print stt
		cur=conn.cursor()
		cur.execute("insert into page(title,author,start,time,price,reader,list,pid)values(%s,%s,%s,%s,%s,%s,%s,%s)",\
			(title,author,start_date,time,money,view,stt,page_id))
		cur.execute("select id from page where pid=%d"%page_id)
		page_id=cur.fetchone()[0]
		days=soup.find_all(class_="days _j_scrollitem _j_days")
		for day in days:
			summary=''
			day_num=day.get('id')
			path=day.find(class_="d_title clearfix").h2.get_text()
			if day.find(class_='day_word'):
				summary=day.find(class_='day_word').get_text()[5:]
			cur.execute("insert into day(day,path,summary,pid)values(%s,%s,%s,%s)",(day_num,path,summary,page_id))
			cur.execute("select id from day where day='%s' and pid=%d"%(day_num,page_id))
			day_id=cur.fetchone()[0]
			if day.find(class_='days_block traffic'):
				traffics=day.find_all(class_='traffic_info')
				for traffic in traffics:
					price=number=tip=''
					item=traffic.find_all('span')
					start_pos=item[0].text
					way=traffic.i['class'][0]
					end_pos=item[1].text
					if traffic.find_all('dl'):
						dls=traffic.find_all('dl')
						for dl in dls:
							if dl.has_attr('class') and dl['class'][0].strip()=='price':
								price=dl.dd.text
							else:
								number=dl.dd.text
					if traffic.find_next_sibling(class_='day_tips'):
						tips=traffic.find_next_sibling(class_='day_tips')
						if tips.find_previous_sibling(class_='traffic_info').find('span').text==start_pos:
							tips.strong.clear()
							tip=tips.get_text().strip()
					cur.execute("insert into traffic(start_pos,end_pos,way,price,number,tip,pid)values(%s,%s,%s,%s,%s,%s,%s)"\
						,(start_pos,end_pos,way,price,number,tip,day_id))
			sites=day.find_all(class_=re.compile('day_item'))
			for site_raw in sites:
				site=site_raw.find(class_=re.compile('day_detail'))
				data={}
				data['time']=data['area']=data['price']=data['explain']=data['others']=data['distance']='';
				data['name']=site.h3.get_text()
				contents=site.ul.find_all('li')
				for item in contents:
					stt=''
					title=item['class'][0]
					prefix=item.find(class_='prefix');
					stt+=prefix.text
					prefix.clear()
					if item.find(attrs={'data-fulltext':True}):
						stt+=item.find(attrs={'data-fulltext':True})['data-fulltext']
					else:
						stt+=item.get_text().strip()
					data[title]=stt
				if site_raw.find_next_sibling(class_="day_go"):
					day_go=site_raw.find_next_sibling(class_="day_go")
					if day_go.find_previous_sibling(class_=re.compile('day_item')).find(class_=re.compile('day_detail')).h3.get_text()==data['name']:
						go_detail=day_go.find(class_='go_detail')
						stk=''
						if go_detail.find('strong'):
							stk+=go_detail.find('strong').text.strip()+' '
							go_detail.find('strong').clear()
						stk+=day_go.find(class_='go_detail').get_text().strip()
						data['distance']=stk
				cur.execute("insert into site(name,price,time,explains,area,others,distance,pid)values(%s,%s,%s,%s,%s,%s,%s,%s)",\
					(data['name'],data['price'],data['time'],data['explain'],data['area'],data['others'],data['distance'],day_id))
		cur.close()
		conn.commit()
		conn.close()
		return

	def __del__(self):
		try:
			self.driver.quit()
		except:
			pass
		return

if __name__=='__main__':
	mySpider=Spider()
	for i in range(158184776,158184779):
		try:
			arr=mySpider.getHtml(i)
			if arr[0]==1:
				mySpider.getData(i,arr[1])
		except Exception,msg:
			fp=open('spider.log','a+')
			fp.write('PAGE_ID：%d，%s，%s\n'%(i,Exception,msg))
			fp.close()
			mySpider=Spider()
	#driver.quit()
	print 'scan completed'
