import json
import urllib.request
import sys
import io
import matplotlib.dates
import matplotlib.pyplot as plt
import datetime


class ConvertArgumentTypes(object):
    """Converts function arguments to specified types."""

    def __init__(self, *args, **kw):
        self.args = args
        self.kw = kw

    def __call__(self, f):
        def func(*args, **kw):
            nargs = [x[0](x[1]) for x in zip(self.args, args)]
            invalidkw = [x for x in kw if x not in self.kw]
            if len(invalidkw) > 0:
                raise TypeError(f.func_name + "() got an unexpected keyword argument '%s'" % invalidkw[0])
            kw = dict([(x, self.kw[x](kw[x])) for x in kw])
            v = f(*nargs, **kw)
            return v

        return func


@ConvertArgumentTypes(str, str)
def crate(crypto_code, crypto_to='USD'):
    response = json.loads(
        urllib.request.urlopen(
            'https://min-api.cryptocompare.com/data/price?fsym=' +
            crypto_code + '&tsyms=' + crypto_to).read().decode('utf-8'))
    return response


@ConvertArgumentTypes(str, int, int, int, str)
def history(crypto_code: str, time_from: int, time_to: int, resolution: int, crypto_to='USD'):
    api_res = {1: 'minute', 60: 'hour', 1440: 'day'}
    limit = (time_to - time_from) // (resolution * 60)
    request = 'https://min-api.cryptocompare.com/data/histo' + api_res[
        resolution] + '?fsym=' + crypto_code + '&tsym=' + crypto_to + '&limit=' + str(limit)
    print(request)
    response = json.loads(urllib.request.urlopen(request).read().decode('utf-8'))
    print(response)
    dates = matplotlib.dates.date2num(list(map(lambda x: datetime.datetime.fromtimestamp(x['time']), response['Data'])))
    values = list(map(lambda x: x['close'], response['Data']))
    plt.scatter(dates, values)
    plt.plot_date(dates, values, '-o')
    plt.gcf().autofmt_xdate()
    plt.title(crypto_code + ' currency')
    plt.xlabel('Date')
    plt.ylabel(crypto_code + ' to ' + crypto_to)
    plt.show()


minput = "".join(open("in.txt", "r").readlines())
sys.stdin = io.StringIO(minput)
print(crate(input()))
print(history(*input().split()))
