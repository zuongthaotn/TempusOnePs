from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import requests

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36', 'Origin': 'https://iboard.ssi.com.vn'}
VNDIRECT_DATA_HISTORY_URL = 'https://dchart-api.vndirect.com.vn/dchart/history'
SSI_HEADERS = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'DNT': '1',
        'sec-ch-ua-mobile': '?0',
        'X-Fiin-Key': 'KEY',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Fiin-User-ID': 'ID',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'X-Fiin-Seed': 'SEED',
        'sec-ch-ua-platform': 'Windows',
        'Origin': 'https://iboard.ssi.com.vn',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://iboard.ssi.com.vn/',
        'Accept-Language': 'en-US,en;q=0.9,vi-VN;q=0.8,vi;q=0.7'
        }
SSI_DATA_HISTORY_URL = 'https://iboard-api.ssi.com.vn/statistics/charts/history'
#
SSI_VN30_STOCK_GROUP_URL = 'https://iboard-query.ssi.com.vn/v2/stock/group/VN30'
SSI_VN100_STOCK_GROUP_URL = 'https://iboard-query.ssi.com.vn/v2/stock/group/VN100'
entrade_headers = {
        'authority': 'services.entrade.com.vn',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'dnt': '1',
        'origin': 'https://banggia.dnse.com.vn',
        'referer': 'https://banggia.dnse.com.vn/',
        'sec-ch-ua': '"Edge";v="114", "Chromium";v="114", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1788.0'
    }
DNSE_DATA_HISTORY_URL = 'https://services.entrade.com.vn/chart-api/v2/ohlcs/derivative'
#
VPS_DATA_HISTORY_URL = 'https://histdatafeed.vps.com.vn/tradingview/history'
vps_headers = {
        'host': 'histdatafeed.vps.com.vn',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'dnt': '1',
        'origin': 'https://chart.vps.com.vn',
        'referer': 'https://chart.vps.com.vn/',
        'sec-ch-ua': '"Edge";v="114", "Chromium";v="114", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
    }


def getDataFromSSI(params):
    return requests.get(SSI_DATA_HISTORY_URL, params=params, headers=SSI_HEADERS, timeout=7)


def getDataFromVnDirect(params):
    return requests.get(VNDIRECT_DATA_HISTORY_URL, params=params, headers=HEADERS)


def getDataFromDNSE(params):
    params.update({'symbol': 'VN30F1M'})
    return requests.get(DNSE_DATA_HISTORY_URL, params=params, headers=HEADERS, timeout=7)


def get_data_from_vps(params):
    params.update({'symbol': 'VN30F1M'})
    return requests.get(VPS_DATA_HISTORY_URL, params=params, headers=vps_headers, timeout=7)


def getStockHistoryData(ticker, timestamp_from=0, timestamp_to=0):
    if timestamp_from == 0:
        three_months = date.today() + relativedelta(months=-3)
        timestamp_from = datetime.strptime(three_months.strftime("%m/%d/%Y") + ', 00:00:0', "%m/%d/%Y, %H:%M:%S") \
            .timestamp()
    if timestamp_to == 0:
        timestamp_to = datetime.strptime(date.today().strftime("%m/%d/%Y") + ', 23:59:00', "%m/%d/%Y, %H:%M:%S") \
            .timestamp()

    response = getDataFromSSI(ticker, timestamp_from, timestamp_to)

    import numpy as np
    import pandas as pd

    timestamp = np.array(response['t']).astype(int)
    close = np.array(response['c']).astype(float)
    open = np.array(response['o']).astype(float)
    high = np.array(response['h']).astype(float)
    low = np.array(response['l']).astype(float)
    volume = np.array(response['v']).astype(int)

    dataset = pd.DataFrame({'Time': timestamp, 'Open': list(open), 'High': list(high), 'Low': list(low),
                            'Close': list(close), 'Volume': list(volume)},
                           columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
    return dataset


def getAllStockHistoryData(ticker):
    timestamp_to = datetime.strptime(date.today().strftime("%m/%d/%Y") + ', 23:59:00', "%m/%d/%Y, %H:%M:%S").timestamp()
    return getStockHistoryData(ticker, 1, timestamp_to)


def getVN30HistoryDataByMinute(ticker="VN30F1M", resolution=1, from_=1, broker='DNSE', keep_time=False):
    # using time module
    import time
    from datetime import datetime
    timestamp_to = int(time.time())

    params = {
        "resolution": resolution,
        "symbol": ticker,
        "from": from_,
        "to": int(timestamp_to)
    }

    try:
        if broker == 'DNSE':
            x = getDataFromDNSE(params)
        elif broker == 'SSI':
            x = getDataFromSSI(params)
        elif broker == 'VPS':
            x = get_data_from_vps(params)
        else:
            x = getDataFromVnDirect(params)
    except requests.exceptions.Timeout:
        print('Time out.')
        return []

    if x.status_code != 200:
        return []
    response = x.json()
    if broker == 'SSI':
        response = response['data']

    import numpy as np
    import pandas as pd

    timestamp = np.array(response['t']).astype(int)
    close = np.array(response['c']).astype(float)
    open = np.array(response['o']).astype(float)
    high = np.array(response['h']).astype(float)
    low = np.array(response['l']).astype(float)
    volume = np.array(response['v']).astype(int)

    dataset = pd.DataFrame({'Time': timestamp, 'Open': list(open), 'High': list(high), 'Low': list(low),
                            'Close': list(close), 'Volume': list(volume)},
                           columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
    if 'Time' in dataset.columns:
        dataset['DateStr'] = dataset.apply(
            lambda x: datetime.fromtimestamp(x['Time']).strftime("%Y-%m-%d, %H:%M:%S"), axis=1)
    dataset['Date'] = pd.to_datetime(dataset['DateStr'])

    ticker_data = dataset.set_index('Date')
    if not keep_time:
        ticker_data.drop(['Time'], axis=1, inplace=True)
    ticker_data.drop(['DateStr'], axis=1, inplace=True)
    return ticker_data


def get_this_month_ticker():
    from datetime import datetime
    from datetime import date

    if datetime.now().day < 14:
        ticker = "VN30F" + str(datetime.now().strftime('%y')) + str(datetime.now().strftime('%m'))
    else:
        cross_thursday_time = 0
        today = datetime.now().day
        month = datetime.now().month
        year = datetime.now().year

        for i in range(1, today):
            week_day = date(day=i, month=month, year=year).weekday()
            if week_day == 3:
                cross_thursday_time += 1

        if cross_thursday_time < 3:
            ticker = "VN30F" + str(datetime.now().strftime('%y')) + str(datetime.now().strftime('%m'))
        else:
            t = datetime.now().month + 1
            y = datetime.now().strftime('%y')
            if t < 10:
                t = "0" + str(t)
            elif t > 12:
                t = "01"
                y = int(y) + 1
            ticker = "VN30F" + str(y) + str(t)

    return ticker


YEAR_CODE_MAP = '0123456789ABCDEFGHJKLMNPQRSTVWXYZ'
MONTH_CODE_MAP = {1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6',
                  7: '7', 8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C'}


def get_new_vn30f1m_ticker():
    """
    VN30F2504 →  41I1F4000
        4: Loại CK Phái sinh
        1: Nhóm CK Phái sinh (1=Future, 2=Future Spread)
        I1: Tài sản cơ sở (VN30=I1, GB05=B5, GB10=BA, VN100=I2)
        F: Năm đáo hạn lấy 30 ký tự từ 0 → W (trừ 3 ký tự I,O,U để tránh nhầm lẫn)
        4: Tháng đáo hạn lấy 12 ký tự từ 1 → C
        000: định danh sản phẩm phái sinh (HĐTL=000)
    :return:
    """
    from datetime import datetime
    from datetime import date

    current_year = datetime.now().strftime('%Y')
    current_month = datetime.now().strftime('%m')

    if datetime.now().day >= 14:
        cross_thursday_time = 0
        today = datetime.now().day
        month = datetime.now().month
        year = datetime.now().year
        for i in range(1, today):
            week_day = date(day=i, month=month, year=year).weekday()
            if week_day == 3:
                cross_thursday_time += 1

        if cross_thursday_time >= 3:
            t = datetime.now().month + 1
            y = datetime.now().strftime('%y')
            if t > 12:
                t = "1"
                current_year = int(y) + 1
            current_month = t

    year_diff = int(current_year) - 2010
    year_code = YEAR_CODE_MAP[year_diff]
    month_code = MONTH_CODE_MAP[int(current_month)]
    return "41I1" + str(year_code) + str(month_code) + '000'
