import json
import urllib.request
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
    return json.dumps(response)


@ConvertArgumentTypes(str, int, int, str, str)
def history(crypto_code: str, time_from: int, time_to: int, resolution: str, crypto_to='USD'):
    api_res = {'minute': 1, 'hour': 60, 'day': 1440}
    limit = (time_to - time_from) // (api_res[resolution] * 60)
    request = 'https://min-api.cryptocompare.com/data/histo' + resolution + '?fsym=' + crypto_code + '&tsym=' + crypto_to + '&limit=' + str(
        limit) + '&toTs=' + str(time_to)
    response = json.loads(urllib.request.urlopen(request).read().decode('utf-8'))
    dates = matplotlib.dates.date2num(list(map(lambda x: datetime.datetime.fromtimestamp(x['time']), response['Data'])))
    values = list(map(lambda x: x['close'], response['Data']))
    plt.scatter(dates, values)
    plt.plot_date(dates, values, '-o')
    plt.gcf().autofmt_xdate()
    plt.title(crypto_code + ' currency')
    plt.xlabel('Date')
    plt.ylabel(crypto_code + ' to ' + crypto_to)
    plt.savefig('tmp_fig.png')
    plt.close()
