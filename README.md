# Badoo introduction spider

## install chromedriver
https://sites.google.com/a/chromium.org/chromedriver/downloads

unzip it, copy it to /user/bin/, or config its path in get.py

both chromedriver and phantomjs should be ok, but this script do not fully support phantomjs.

chromedriver has GUI, phantomjs do not have GUI, so have more higher performance.

## install selenium
download selenium from
https://pypi.python.org/packages/54/4e/5efe0adb5210c2d96c060287d70274d5aa1987c052a0e56e4d8fe31207ad/selenium-3.0.0b3.tar.gz#md5=794adea4d20d6dc66d48891c2287ade0

      tar -xvf selenium-3.0.0b3.tar.gz, enter its folder,
      sudo python setup.py install

## make sure your account can log into badoo in chrome browser.
yes of course, you need have chrome browser installed.

## get interesting self-introduction on badoo:
1. run "python get.py" in one console,
2. then run below cmd in another console:
tail -f /tmp/log1  | grep text | grep ==== | grep -v "Please rotate your phone"

you will get sth like this

      "text": "https://m.badoo.com/profile/15810xxxx ==== Know Me!!! ;)",
      "text": "https://m.badoo.com/profile/15810xxxy ==== Cool, careing loving n social ...",
      "text": "https://m.badoo.com/profile/15810xxxz ==== accepter et respecter autrui ...",
