from django.core.management.base import BaseCommand, CommandError
from mining.models import Trade, Active
import urllib.request, json 

class Command(BaseCommand):
    def handle(self, *args, **options):
        url = "https://mdgateway04.easynvest.com.br/iwg/snapshot/?t=webgateway&c=5448062&q=WINM19"
        req = urllib.request.Request(url)
        trade = Trade()
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode())

                price = float(data['Value'][0]['Ps']['P'])
                business = int(data['Value'][0]['Ps']['TC'])
                tot_ctrcts_papers = int(data['Value'][0]['Ps']['TT'])

                if trade.price != price or trade.business != business or trade.tot_ctrcts_papers != tot_ctrcts_papers:
                    trade.id = None
                    trade.active = Active.objects.get(id=1)
                    datetime = data['Value'][0]['UT']
                    # 2019-05-07T18:01:23.932
                    trade.time_stamp = datetime.datetime(int(datetime[0:4]), int(datetime[5:7]), int(datetime[8:10]), int(datetime[11:13]), int(datetime[14:16]), int(datetime[17:19]), int(datetime[20:24]))
                    trade.price = price
                    trade.business = business
                    trade.tot_ctrcts_papers = tot_ctrcts_papers
                    trade.save()

        except urllib.error.URLError as e:
            print(e.reason)