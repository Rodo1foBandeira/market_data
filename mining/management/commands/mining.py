from django.core.management.base import BaseCommand, CommandError
from mining.models import Trade, Active
import urllib.request, json, datetime, pytz

class Command(BaseCommand):
    def handle(self, *args, **options):
        url = "https://mdgateway04.easynvest.com.br/iwg/snapshot/?t=webgateway&c=5448062&q=WINM19"
        req = urllib.request.Request(url)
        trade = Trade()
        while(True):
            try:
                with urllib.request.urlopen(req) as resp:
                    data = json.loads(resp.read().decode())

                    price = float(data['Value'][0]['Ps']['P'])
                    business = int(data['Value'][0]['Ps']['TC'])
                    tot_ctrcts_papers = int(data['Value'][0]['Ps']['TT'])

                    if trade.price != price or trade.business != business or trade.tot_ctrcts_papers != tot_ctrcts_papers:
                        trade.id = None
                        trade.active = Active.objects.get(id=1)
                        datetime_buss = data['Value'][0]['UT']
                        trade.datetime_buss = datetime.datetime(int(datetime_buss[0:4]), int(datetime_buss[5:7]), int(datetime_buss[8:10]), int(datetime_buss[11:13]), int(datetime_buss[14:16]), int(datetime_buss[17:19]), int(datetime_buss[20:24]), tzinfo=pytz.UTC)
                        trade.price = price
                        trade.business = business
                        trade.tot_ctrcts_papers = tot_ctrcts_papers
                        trade.save()
                        print('Preco: ' + data['Value'][0]['Ps']['P'])
                        print('Negocios: ' + data['Value'][0]['Ps']['TC'])
                        print('Contratos: ' + data['Value'][0]['Ps']['TT'])

            except urllib.error.URLError as e:
                print(e.reason)
