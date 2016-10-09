1. config

1) install selenium:
download selenium from
https://pypi.python.org/packages/54/4e/5efe0adb5210c2d96c060287d70274d5aa1987c052a0e56e4d8fe31207ad/selenium-3.0.0b3.tar.gz#md5=794adea4d20d6dc66d48891c2287ade0
tar -xvf selenium-3.0.0b3.tar.gz, enter its folder,
sudo python setup.py install

2) install Beautifulsoup
download beautifulsoup from
https://www.crummy.com/software/BeautifulSoup/bs4/download/4.5/beautifulsoup4-4.5.0.tar.gz
tar -xvf beautifulsoup4-4.5.0.tar.gz, enter its folder,
sudo python setup.py install

3) install mysql-python
sudo apt-get install libmysqlclient-dev
download mysql-python from https://pypi.python.org/packages/a5/e9/51b544da85a36a68debe7a7091f068d802fc515a3a202652828c73453cad/MySQL-python-1.2.5.zip#md5=654f75b302db6ed8dc5a898c625e030c
unzip MySQL-python-1.2.5.zip and enter its folder,
sudo python setup.py install

4) install chromedriver
https://sites.google.com/a/chromium.org/chromedriver/downloads
unzip it, copy it to /user/bin/, or config its path in get.py

both chromedriver and phantomjs should be ok, but this script do not fully support phantomjs.
chromedriver has GUI, phantomjs do not have GUI, so have more higher performance.

2. make sure your account can log into badoo in chrome browser.

3. get badoo user info:
python get.py
