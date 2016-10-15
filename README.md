# Badoo introduction spider

## install chromedriver
https://sites.google.com/a/chromium.org/chromedriver/downloads
unzip it, copy it to /user/bin/, or config its path in get.py

both chromedriver and phantomjs should be ok, but this script do not fully support phantomjs.
chromedriver has GUI, phantomjs do not have GUI, so have more higher performance.

## make sure your account can log into badoo in chrome browser.

## get interesting self-introduction on badoo:
1. run "python get.py" in one console,
2. then run below cmd in another console:
tail -f /tmp/log1  | grep text | grep ==== | grep -v "Please rotate your phone"
