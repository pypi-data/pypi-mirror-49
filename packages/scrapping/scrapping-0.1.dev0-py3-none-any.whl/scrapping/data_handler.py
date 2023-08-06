import json
import datetime

class JsonDataHandler:
    "Data handler for json files"
    def __init__(self, filename=None, daemon=False, filemode='a'):
        self.filename = filename
        self.daemon = daemon
        self.filemode = filemode

        self.__first = True

        assert not (self.daemon and not self.filename), "Daemon set with no filename specified"

    def setUp(self, spider):
        if not self.filename:
            time = datetime.datetime.now()
            self.filename = "{spider_name}-{time}.json".format(spider_name=spider.name, time=time.strftime('%Y-%m-%d-%H-%M-%S'))
        if not self.daemon:
            self.out = open(self.filename, self.filemode, encoding='utf8')
            self.out.write('[')

    def process(self, data):
        if not self.daemon:
            if not self.__first:
                self.out.write(', ')
                self.out.write('\n')
            else:
                self.__first = False
            self.out.write(json.dumps(data))

        else:
            with open(self.filename, self.filemode) as out:
                out_dict = {'time': datetime.datetime.now().isoformat(), 'data': data}
                if self.first:
                    out_str = '[' + json.dumps(out_dict)
                else:
                    out_str = ', ' + json.dumps(out_dict)
                out.write(out_str)

    def tearDown(self):
        if not self.daemon:
            self.out.write(']')
            self.out.close()
        else:
            with open(self.filename, self.filemode) as out:
                out.write(']')
