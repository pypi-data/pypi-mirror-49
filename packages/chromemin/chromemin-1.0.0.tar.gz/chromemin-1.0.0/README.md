## chromemin
A Python Package for the Google Chrome Dev Protocol

## Installation
To install pychrome, simply:
```bash
pip install -U chromemin
```

or from source:
```bash
python setup.py install
```

## Setup Chrome

simply
```bash
google-chrome --remote-debugging-port=9222
```

or headless mode (chrome version >= 59):

```bash
google-chrome --headless --disable-gpu --remote-debugging-port=9222
```

## Getting Started

```python
import asyncio
import chromemin

def sync_cmd(cmd):
    asyncio.get_event.loop().run_until_complete(s)

async def request_will_be_sent(**kwargs):
    print("loading: %s" % kwargs.get('request').get('url'))

if __name__ == '__main__':
    browser = chromemin.Chrome(host='localhost', port=9222)
    tab_info = sync_cmd(browser.create_tab())
    tab = chromemin.Tab(title=tab_info['title'], url=tab_info['url'], ws_uri=tab_info['webSocketDebuggerUrl'], tab_id=tab['id'])
    sync_cmd(tab.connect())
    tab.Network.requestWillBeSent=request_will_be_sent
    aync_cmd(tab.Network.enable())
    aync_cmd(tab.Page.navigate(url="https://github.com/mousemin"))

```

## Ref

* [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
