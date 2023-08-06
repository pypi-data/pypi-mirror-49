# fakeua
*Python3 module made as a wrapper of fake-useragent.*

## Rationale:
fake-useragent package (https://github.com/hellysmile/fake-useragent)
have an API which is brittle and too verbose for cases when you just want
predictability and the work done without unnecesary headaches.

## Installation
### Install with pip
```
pip3 install --user -U fakeua
```

## Usage
FakeUA can be used from the shell too.

fakeua -h

Or importing its functions.

```
In [1]: import fakeua

# Update useragent DB in a json file (~/.fakeua_databrowsers.json)
In [2]: fakeua.update_useragent_db()
Out[2]: True

In [3]: fakeua.get_useragent_list()
Out[3]: 
['Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0',
 'Mozilla/5.0 (X11; Linux i586; rv:63.0) Gecko/20100101 Firefox/63.0',
 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:62.0) Gecko/20100101 Firefox/62.0']

In [4]: fakeua.load_useragent_db()                                                 
Out[4]: ...
# It throws a dict containing the browsers scraped by fake-useragent.

In [5]: fakeua.get_random_ua()
Out[5]: 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0'
```
