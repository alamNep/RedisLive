from .BaseController import BaseController
import tornado.ioloop
import tornado.web
import dateutil.parser
import datetime


class TopCommandsController(BaseController):

    def get(self):
        return_data = dict(data=[],
                           timestamp=datetime.datetime.now().isoformat())

        server = self.get_argument("server")
        from_date = self.get_argument("from", None)
        to_date = self.get_argument("to", None)

        if not from_date or not to_date:
            end = datetime.datetime.now()
            delta = datetime.timedelta(seconds=120)
            start = end - delta
        else:
            start = dateutil.parser.parse(from_date)
            end   = dateutil.parser.parse(to_date)
        
        utc9 = datetime.timezone(datetime.timedelta(hours=9))
        dt1_utc9 = start.replace(tzinfo=utc9)
        dt2_utc9 = end.replace(tzinfo=utc9)

        dt1_utc = dt1_utc9.astimezone(datetime.timezone.utc)
        dt2_utc = dt2_utc9.astimezone(datetime.timezone.utc)

        start = dt1_utc
        end = dt2_utc
        

        for data in self.stats_provider.get_top_commands_stats(server, start,
                                                               end):
            return_data['data'].append([data[0], data[1]])

        self.write(return_data)
