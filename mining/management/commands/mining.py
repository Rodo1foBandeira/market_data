from django.core.management.base import BaseCommand, CommandError
from mining.models import Trade, Active
import urllib.request, json, datetime, pytz

class Command(BaseCommand):
    trade = {}
    trade['WINM19'] = Trade()
    trade['WDOM19'] = Trade()
    trade['WINM19'].active = Active.objects.get(id=1)
    trade['WDOM19'].active = Active.objects.get(id=2)

    def handle(self, *args, **options):
        url = "https://mdgateway04.easynvest.com.br/iwg/snapshot/?t=webgateway&c=5448062&q=WINM19|WDOM19"
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
