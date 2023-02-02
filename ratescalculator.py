from datetime import date
from datetime import timedelta
import aiohttp
import asyncio

headers = { 
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
  'content-type': 'application/json',
}

async def getUnistreamRate(session, currency):
  async with session.get('https://online.unistream.ru/card2cash/calculate?destination=GEO&amount=10&currency='+currency+'&accepted_currency=RUB&profile=unistream_front') as response:
    json = await response.json()
    return float(json['fees'][0]['acceptedAmount'])/10

async def getKoronaPay(session): 
  async with session.get('https://koronapay.com/transfers/online/api/transfers/tariffs?sendingCountryId=RUS&sendingCurrencyId=810&receivingCountryId=GEO&receivingCurrencyId=981&paymentMethod=debitCard&receivingAmount=100&receivingMethod=cash&paidNotificationEnabled=false') as response:
    json = await response.json()
    return float(json[0]['exchangeRate'])

async def parseBinance(session, payType,fiat, tradeType = "BUY"):
  body = {"proMerchantAds":False,"page":1,"rows":1,"payTypes":[payType],"countries":[],"asset":"USDT","fiat":fiat,"tradeType":tradeType}
  async with session.post("https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search", json = body) as response:
    json = await response.json()
    return float(json['data'][0]['adv']['price'])

async def parseUnionPay(session, date = date.today()):
  today = str(date).replace('-','')
  try:
    async with session.get("https://m.unionpayintl.com/jfimg/"+today+".json") as response:
      idr = 0
      json = await response.json()
      for i in json['exchangeRateJson']:
        if (i['baseCur']=="CNY") and (i['transCur']=="IDR"):
          idr = float(i['rateData'])
          break
      return idr
  except:
    return await parseUnionPay(session, today - timedelta(days = 1))

async def parseTinkoffInvest(session, ticker):
  async with session.get("https://www.tinkoff.ru/api/trading/currency/get?ticker="+ticker) as response:
    json = await response.json()
    return float(json['payload']['lotPrice']['value'])

async def thousandRupiahInRub(session):
  async with session.get("https://www.currency.me.uk/remote/ER-CCPAIR-AJAX.php?ConvertTo=RUB&ConvertFrom=IDR&amount=1000") as response:
    rupiah = await response.text()
    return float(rupiah)


async def loadAllData():
  async with aiohttp.ClientSession(headers=headers) as session:
    tasks = [
      getUnistreamRate(session, "USD"),
      getUnistreamRate(session, "GEL"),
      getKoronaPay(session),
      parseBinance(session, "TinkoffNew", "RUB"),
      parseBinance(session, "TBCBank", "GEL"),
      parseBinance(session, "CREDOBANK", "GEL"),
      parseBinance(session, "Maybank", "IDR", tradeType = "SELL"),
      parseTinkoffInvest(session, "CNYRUB"),
      thousandRupiahInRub(session),
      parseUnionPay(session),
    ] 

    async_tasks = map(lambda task: asyncio.create_task(task), tasks)
    original_result = await asyncio.gather(*async_tasks)
    return original_result

def roundTwoDigits(val):
  return round(val,2)

def calculateRates():
    result = asyncio.run(loadAllData())
    unistreamUsdToRub = result[0]
    unistreamGelToRub = result[1]
    koronaPayGelToRub = result[2]
    tinkoffUsdt = result[3]
    tbcUsdt = result[4]
    credoUsdt = result[5]
    usdtToIdr = result[6]
    tinkoffCny = result[7]
    thousandIdrInRub = result[8]
    idrToCny = 1/result[9]

    variablesTable = {
      "Unistream USD":  round(unistreamUsdToRub,2),
      "Unistream GEL":  round(unistreamGelToRub,2),
      "Korona GEL":  round(koronaPayGelToRub,2),
      "Tinkoff USDT":  round(tinkoffUsdt,2),
      "TBC USDT":  round(tbcUsdt,2),
      "Credo USDT":  round(credoUsdt,2),
      "USDT IDR":  round(usdtToIdr,2),
      'Tinkoff CNY':  round(tinkoffCny,2),
      'CNY to IDR':  round(idrToCny,2),
    }
    resultTable = {
      "Stock price": round(thousandIdrInRub,2),
      "Unistream GEL USDT": round(1000/(usdtToIdr/(unistreamGelToRub*tbcUsdt)),2),
      "Korona GEL USDT": round(1000/(usdtToIdr/(koronaPayGelToRub*tbcUsdt)),2),
      "Korona GEL Credo USDT": round(1000/(usdtToIdr/(koronaPayGelToRub*credoUsdt)),2),
      "Tinkoff USDT": round(1000/(usdtToIdr/tinkoffUsdt),2),
      "TBC USD IDR": round(1000/(14367/unistreamUsdToRub),2),
      "Tinkoff CNY": round(tinkoffCny*(1000/idrToCny),2),
    }
    return (variablesTable, resultTable)
