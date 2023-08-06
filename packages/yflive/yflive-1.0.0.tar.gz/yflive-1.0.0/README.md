# yflive v1.0.0

[![Build Status](https://github.com/mbnlc/yflive/actions/workflows/build.yml/badge.svg)](https://github.com/mbnlc/yflive/actions/workflows/build.yml)
[![DeepSource](https://deepsource.io/gh/mbnlc/yflive.svg/?label=active+issues&show_trend=true)](https://deepsource.io/gh/mbnlc/yflive/?ref=repository-badge)

yflive is a [Yahoo! Finance](https://finance.yahoo.com) live data streamer. Originally created as an alternative to scraping prices of Yahoo! Finance, yflive implements a websocket client for receiving live quotes from Yahoo! Finance directly.

For historic prices or other financial information, [yfinance](https://github.com/ranaroussi/yfinance) is recommended.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install yflive.

```bash
pip install yflive
```

## Usage

### Quick start

The following example shows a simple setup, which subscribes to the tickers AAPL and TSLA and prints received quotes until interrupted.

```python
from yflive import QuoteStreamer

qs = QuoteStreamer()
qs.subscribe(["AAPL", "TSLA"]) 

qs.on_quote = lambda qs, q: print(q)

# Non-blocking if should_thread=True (default is False)
qs.start(should_thread=False)
```

Quotes are in real time (with [exceptions](https://help.yahoo.com/kb/finance-for-web/exchanges-data-providers-yahoo-finance-sln2310.html)) and normally only available during trading hours.

For additional information regarding Yahoo! Finance data, please refer to their section on data accuracy found [here](https://help.yahoo.com/kb/finance-for-web/#/).

## Collaboration

**This is very early stage**

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

**yflive** is distributed under the [Apache-2.0 License](http://www.apache.org/licenses/). Review [LICENSE.txt](https://github.com/mbnlc/yflive/blob/master/LICENSE.txt) for further information.
