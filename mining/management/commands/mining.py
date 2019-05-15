from django.core.management.base import BaseCommand, CommandError
from mining.models import Trade, Active
import urllib.request, json, datetime, pytz
from datetime import date

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
    trade[winfut] = Trade()
    trade[wdofut] = Trade()
    trade[winfut].active = Active.objects.get(id=1)
    trade[wdofut].active = Active.objects.get(id=2)

    def handle(self, *args, **options):
        url = "https://mdgateway04.easynvest.com.br/iwg/snapshot/?t=webgateway&c=5448062&q="+winfut+"|"+wdofut
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
        price = float(response['Ps']['P'])
        business = int(response['Ps']['TC'])
        tot_ctrcts_papers = int(response['Ps']['TT'])

        if self.trade[response['S']].price != price or self.trade[response['S']].business != business or self.trade[response['S']].tot_ctrcts_papers != tot_ctrcts_papers:
            self.trade[response['S']].id = None
            datetime_buss = response['UT']
            self.trade[response['S']].datetime_buss = datetime.datetime(int(datetime_buss[0:4]), int(datetime_buss[5:7]), int(datetime_buss[8:10]), int(datetime_buss[11:13]), int(datetime_buss[14:16]), int(datetime_buss[17:19]), int(datetime_buss[20:24]), tzinfo=pytz.UTC)
            self.trade[response['S']].price = price
            self.trade[response['S']].business = business
            self.trade[response['S']].tot_ctrcts_papers = tot_ctrcts_papers
            self.trade[response['S']].save()
