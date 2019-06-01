from django.core.management.base import BaseCommand, CommandError
from mining.models import Trade
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
    trade[winfut] = Trade.objects.filter(active__startswith='WIN').last()

    trade[wdofut] = Trade.objects.filter(active__startswith='WDO').last()

    def add_arguments(self, parser):
        parser.add_argument('-i', '--infinite', type=int, help='Define if infinite')

    def handle(self, *args, **options):
        url = "https://mdgateway04.easynvest.com.br/iwg/snapshot/?t=webgateway&c=5448062&q="+self.winfut+"|"+self.wdofut
        req = urllib.request.Request(url)

        if (options['infinite'] == 1):
            while(True):
                try:
                    with urllib.request.urlopen(req) as resp:
                        data = json.loads(resp.read().decode())
                        for item in data['Value']:
                            self.save(item)
                except urllib.error.URLError as e:
                    print(e.reason)
        else:
            try:
                with urllib.request.urlopen(req) as resp:
                    data = json.loads(resp.read().decode())
                    for item in data['Value']:
                        self.save(item)
            except urllib.error.URLError as e:
                print(e.reason)    

    def save(self, response):
        if response['Ts'] != None and len(response['Ts']) > 0:
            for item in response['Ts']:
                item['DT'] = datetime.strptime(item['DT'], '%Y-%m-%dT%H:%M:%S.%f').replace(tzinfo=pytz.UTC)
                item['Br'] = int(item['Br'])
                item['Sr'] = int(item['Sr'])
                item['Q'] = int(item['Q'])
                item['P'] = float(item['P'])
                
            #response['Ps']['P'] = float(response['Ps']['P'])
            response['Ps']['TC'] = int(response['Ps']['TC'])
            response['Ps']['TT'] = int(response['Ps']['TT'])

            # nao existe possibilidade de duplicidade
            # novos: existe possibilidade de perder informaçao entre requisiçoes, pois pode haver um novo negocio identico,
            # mas temos os totalizadores, e o mais importante é pegar as variações do preco        
            novos_decrescente = sorted(
                filter(
                    lambda item:
                        self.trade[response['S']] == None
                        or (item['DT'] >= self.trade[response['S']].datetime_buss
                        and (item['Br'] != self.trade[response['S']].buyer 
                        or item['Sr'] != self.trade[response['S']].seller 
                        or item['Q'] != self.trade[response['S']].qtd 
                        or item['P'] != self.trade[response['S']].price)
                        ),
                    response['Ts']
                ),
                key=lambda x: x['DT']
            )

            if len(novos_decrescente) > 0:
                Trade.objects.bulk_create(
                    map(
                        lambda item:
                            Trade(active=response['S'], datetime_buss=item['DT'], buyer = item['Br'], seller = item['Sr'], price = item['P'], qtd = item['Q'], tot_qtd = response['Ps']['TT'], tot_buss = response['Ps']['TC']),
                        novos_decrescente
                    )
                )

                self.trade[response['S']].datetime_buss = novos_decrescente[-1]['DT']
                self.trade[response['S']].buyer = novos_decrescente[-1]['Br']
                self.trade[response['S']].seller = novos_decrescente[-1]['Sr']
                self.trade[response['S']].price = novos_decrescente[-1]['P']
                self.trade[response['S']].qtd = novos_decrescente[-1]['Q']