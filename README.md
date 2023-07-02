## awesomewm-exchange-rates
An exchange rate monitoring widget for awesome wm.

## features
* Quickly check what your money is worth in other countries (useful if you shop online a lot)
* Keep track of what your stash of (whatever supported currency) is worth in terms of your money
* Simple and easy to use
* Adjust layout easily to find a format you like

Here's what NZD to USD looks like today.
![exchange_1_000](https://github.com/NBKelly/awesomewm-exchange-rates/assets/9095245/5a02c2f3-ecd9-43b5-9969-94dcd10b3735)

Here's NZD to GBP today.
![exchange_1_001](https://github.com/NBKelly/awesomewm-exchange-rates/assets/9095245/1820d509-9607-454f-9bec-ffd4603bbf69)

Here's an example of the widget jammed into an existing layout.
![exchange_1_002](https://github.com/NBKelly/awesomewm-exchange-rates/assets/9095245/b76ac04b-990a-43e1-b808-78343b7dade5)

Here's what a fictional quantity of BTC is worth in NZD today.
![exchange_1](https://github.com/NBKelly/awesomewm-exchange-rates/assets/9095245/2548de5d-6b0f-4901-957a-dddb33726b7a)

## setup
* this depends on `requests, json` in `python3`
* this also depends on `awful, wibox` modules in lua (I think these are both packaged with awesomewm)
* Get an api key from openexchangerates.org so you can use their api.
* clone this repo into .config/awesome/
* edit the config.py (see below)
* include and add the widget in your rc.lua file

## config
* Set your base currency (BASE) and your target currency (TARGET) to whatever you use in daily life. For me, that would be NZD (my currency) and USD (what 90% of my purchases are).
* Adjust the decimal places for the main, extra, and condensed modes if you feel like it
* If you want a bulkier layout, like `1 NZD = 0.2 EUR`, then change mode from `SQUEEZE` to `FULL`
* Add all the currencies you care about in EXTRA as a list of 1/2/3-tuples
* Add in your appid

Note that 
* 1-tuples here are just "what's 1 (my currency) worth"
* 2-tuples are "what's 'X target currency' worth in my currency"
* 3-tuples just add a format modifer

## awesome config
This is subject to change, and might be different for you than it is for me.

* open rc.lua
* import exchangeRates somewhere near the top of your file
```
local exchangeRates = require("awesomewm-exchange-rates.rates")
```
* call the function somewhere in your layout when the wibar is being created. For me, this looks like:
```
volumebar_widget({
    main_color = '#dcdccc',
    mute_color = '#ff0000',
    width = 80,
		shape = 'powerline',
    margins = 8
}),

rateWidget(),  
```
## Supported Currencies
Exactly what openexchangerates supports. This includes a few cryptocurrencies. For more info, see https://docs.openexchangerates.org/docs/alternative-currencies.

Note that these values only update hourly (to avoid hitting the api rate limits). This is not suitable for trading purposes

## Credit
While not directly following any guides, I did pull from some of the material that Pavel Makhov authored. Check him out at https://github.com/streetturtle/ or https://pavelmakhov.com/.
