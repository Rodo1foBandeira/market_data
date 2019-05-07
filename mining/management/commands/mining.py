from django.core.management.base import BaseCommand, CommandError
from mining.models import Trade
import urllib.request, json 

class Command(BaseCommand):
    def handle(self, *args, **options):
        url = "https://mdgateway04.easynvest.com.br/iwg/snapshot/?t=webgateway&c=5448062&q=WINM19"
        req = urllib.request.Request(url)
        trade = Trade()
        while(1):
            try:
                with urllib.request.urlopen(req) as resp:
                    data = json.loads(resp.read().decode())

                    price = float(data['Value'][0]['Ps']['P'])
                    business = int(data['Value'][0]['Ps']['TC'])
                    tot_ctrcts_papers = int(data['Value'][0]['Ps']['TT'])

                    if trade.price != price or trade.business != business or trade.tot_ctrcts_papers != tot_ctrcts_papers
                        trade.id = None
                        trade.active = 1
                        time_stamp = data['Value'][0]['UT']
                        trade.price = price
                        trade.business = business
                        trade.tot_ctrcts_papers = tot_ctrcts_papers
                        trade.save()

            except urllib.error.URLError as e:
                print(e.reason)