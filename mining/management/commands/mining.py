from django.core.management.base import BaseCommand, CommandError
from mining.models import Trade, Active
import urllib.request, json, pytz
from datetime import date, datetime

class Command(BaseCommand):
    meses = (
    'F', # Jan
    'G', # Fev
    'H', # Mar
    'J', # Abr
    'K', # Mai
    'M', # Jun
    'N', # Jul
    'Q', # Ago
    'U', # Set
    'V', # Out
    'X', # Nov
    'Z'  # Dez
    )

    hoje = date.today()

    if  (hoje.month % 2 > 0):
        winfut = 'WIN' + meses[hoje.month] + str(hoje.year)[2:4]
    elif (hoje.weekday() >= 2 and (hoje.day + 5-hoje.weekday() >= 15)):
        winfut = 'WIN' + meses[hoje.month+1] + str(hoje.year)[2:4]
    else:
        winfut = 'WIN' + meses[hoje.month-1] + str(hoje.year)[2:4]

    wdofut = 'WDO' + meses[hoje.month] + str(hoje.year)[2:4]

    trade = {}
    trade[winfut] = Trade.objects.filter(active_id=1).order_by('-id')[:1]
    trade[winfut].active = Active.objects.get(id=1)

    trade[wdofut] = Trade.objects.filter(active_id=2).order_by('-id')[:1]
    trade[wdofut].active = Active.objects.get(id=2)

    def handle(self, *args, **options):
        url = "https://mdgateway04.easynvest.com.br/iwg/snapshot/?t=webgateway&c=5448062&q="+self.winfut+"|"+self.wdofut
        req = urllib.request.Request(url)
        
        while(True):
            try:
                with urllib.request.urlopen(req) as resp:
                    data = json.loads(resp.read().decode())
                    self.save(data['Value'][0])
                    self.save(data['Value'][1])
            except urllib.error.URLError as e:
                print(e.reason)

    def save(self, response):

        for item in response['Ts']:
            item['DT'] = self.toDate(item['DT'])
            item['Br'] = int(item['Br'])
            item['Sr'] = int(item['Sr'])
            item['Q'] = int(item['Q'])
            item['P'] = float(item['P'])
            
        response['Ps']['P'] = float(response['Ps']['P'])
        response['Ps']['TC'] = int(response['Ps']['TC'])
        response['Ps']['TT'] = int(response['Ps']['TT'])

        novos = filter(lambda x: (x['DT'] >= self.trade[response['S']].datetime_buss and (x['Br'] != self.trade[response['S']].buyer or x['Sr'] != self.trade[response['S']].seller or x['Q'] != self.trade[response['S']].qtd or x['P'] != self.trade[response['S']].price)), response['Ts'])
        for item in sorted(novos, key=lambda x: x['DT']):        
            self.trade[response['S']].id = None
            self.trade[response['S']].datetime_buss = item['DT']
            self.trade[response['S']].buyer = item['Br']
            self.trade[response['S']].seller = item['Sr']
            self.trade[response['S']].price = item['P']
            self.trade[response['S']].qtd = item['Q']
            self.trade[response['S']].tot_qtd = response['Ps']['TT']
            self.trade[response['S']].tot_buss = response['Ps']['TC']
            self.trade[response['S']].save()
        
    def toDate(self, dtStr):
        return datetime(int(dtStr[0:4]), int(dtStr[5:7]), int(dtStr[8:10]), int(dtStr[11:13]), int(dtStr[14:16]), int(dtStr[17:19]), int(dtStr[20:24]), tzinfo=pytz.UTC)
