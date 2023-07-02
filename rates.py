#!/usr/bin/python

import requests
import json
import config

API="https://openexchangerates.org/api/" #
APPID=config.APPID
ENDPOINT="latest.json"
BASE=config.BASE;
TARGET=config.TARGET # primary currency you care about (shows in toolbar)
SHOW_ALTERNATIVE="1" # see https://docs.openexchangerates.org/docs/alternative-currencies
EXTRA=config.EXTRA #["USD","EUR","GBP","BTC"]
MODE=config.MODE
primaryDP=config.PRIMARY_DP
extraDP=config.EXTRA_DP
lhsDP=config.LHS_DP

url = str.format("{}{}?app_id={}&show_alternative={}", API, ENDPOINT, APPID,SHOW_ALTERNATIVE)
r = requests.get(url)
resp = json.loads(r.content)

output = []
basis = 1.0

## reduce spaghetti
def getRate(s):
    return float(resp['rates'][s])

## can add more display modes here really easily
def formatRate(a, b, c, d):
    if config.MODE == config.SQUEEZE:
        return str.format("{} {}", c, d)
    else:
        return str.format("{} {} = {} {}", a, b, c, d)

if 'status' in resp:
    ## either you have no key, or you exceeded your limit
    print("<span foreground=\"red\">api rejected: " + str(resp['status']) + "</span>")
else:
    if(BASE == resp['base']):
        ## If the bases match, then no conversion is needed at all
        output.append(formatRate(1, TARGET, round(getRate(TARGET), primaryDP), BASE))
    elif(TARGET == resp['base']):
        ## If the bases are inverted, we need to make a comparison by inverting the exchange rate
        # note: if 1 NZD = 0.61 USD
        #      and 1 USD = 0.79 GBP
        #     then 1 NZD = 0.4819 GBP
        #     so a formula for this conversion is basis * currency-in-base
        basis = 1/getRate(BASE)
        output.append(formatRate(1, BASE, round(basis, primaryDP), TARGET))
    else:
        ## we need to do a little more work for our conversion
        # pretend we're going from NZD to AUD
        # note: if 1 NZD = 0.61 USD
        #      and 1 AUD = 0.67 USD
        #     then 1 NZD = 0.91 AUD
        #     so a formula for this conversion is basis / currency-in-base
        basis = 1/getRate
        targetval = getRate(target)
        output.append(formatRate(1, BASE, round(basis*targetval,primaryDP),TARGET))

    for currency in EXTRA:
        ## just multiply through by the basis we calculated and it **JUST** works
        ## what we want is x base = y currency
        if(len(currency) == 1):
            rate = float(resp['rates'][currency[0]])*basis
            rate = round(rate, extraDP)
            output.append(formatRate(1, BASE, rate,currency[0]))
        else:
            ## if we have x to y, surely we just need to divide by y?
            rate = float(resp['rates'][currency[0]])*basis
            lhs = (float(currency[1]) / rate)
            lhs  = round(lhs, lhsDP) if lhsDP > 0 else int(lhs)
            rate = rate / float(currency[1])
            rate = round(rate, extraDP)
            ## that could be simplified, but I don't care enough to figure it out

            ## there are few diffent condense modes here
            if(len(currency) > 2 and currency[2] == config.CONDENSED):
                output.append(str.format("{} {} ({})", lhs, BASE, currency[0]))
            elif(len(currency) > 2 and currency[2] == config.SMALL):
                output.append(str.format("{} ({})", lhs, currency[0]))
            else:
                output.append(str.format("{} {} = {} {}", lhs, BASE, currency[1], currency[0]))

        #amt = float(currency[0]);
        #lhs = str(rate/*mt) + " " + BASE
        #rate = str(round(rate * basis, extraDP)) + " " + currency[1];
        #output.append(lhs + " = " + rate)

for line in output:
    print(line)
