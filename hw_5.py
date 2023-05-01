import platform
from datetime import datetime, timedelta

from aiohttp import ClientSession
import aiohttp
import asyncio
import sys


def js_pars(json_pb_dict):  # Виймаємо з однієї дати евро та долар
    date = json_pb_dict["date"]
    date_dict = {date: {"EUR": {}, "USD": {}}}

    for currency in json_pb_dict["exchangeRate"]:
        for el in currency:
            if currency["currency"] == "EUR":
                date_dict[date]["EUR"]["sale"] = currency["saleRate"]
                date_dict[date]["EUR"]["purchase"] = currency["purchaseRate"]

            elif currency["currency"] == "USD":
                date_dict[date]["USD"]["sale"] = currency["saleRate"]
                date_dict[date]["USD"]["purchase"] = currency["purchaseRate"]

    return date_dict


def js_pars_list(json_pb_list):  # Створюємо резельтуючий список
    result = []

    for el in json_pb_list:
        r = js_pars(el)
        result.append(r)
    return result


def get_day_number():
    if sys.argv[1]:
        number = sys.argv[1]
    else:
        number = 1
    return number


def get_date_list(date_number):
    current_datetime = datetime.now()
    current_datetime = current_datetime.date()
    date_list = []
    date_list.append(current_datetime.strftime("%d-%m-%Y"))
    date_list[0] = date_list[0].replace("-", ".")

    if date_number:
        for i in range(1, date_number):
            date = current_datetime - timedelta(days=i)
            date = date.strftime("%d-%m-%Y")
            date = date.replace("-", ".")
            date_list.append(date)

    return date_list


async def get_currency_exchange_pb(date):
    async with ClientSession() as session:
        url_pb = f"https://api.privatbank.ua/p24api/exchange_rates?json&date=" + date

        async with session.get(url_pb) as response:
            print("Status:", response.status)
            print("Content-type:", response.headers["content-type"])
            print("Cookies: ", response.cookies)
            print(response.ok)
            currency_json = await response.json()
            return currency_json


async def get_rates_list(dates):
    tasks = []
    if platform.system() == "Windows":
        for date in dates:
            tasks.append(asyncio.create_task(get_currency_exchange_pb(date)))

    results = await asyncio.gather(*tasks)

    result_list = []
    for result in results:
        result_list.append(result)

    return result_list


def main():
    date_number = get_day_number()
    dates_number = get_date_list(date_number)
    bp_json = asyncio.run(get_rates_list(dates_number))
    result = js_pars_list(bp_json)
    print(result)


if __name__ == "__main__":
    main()
