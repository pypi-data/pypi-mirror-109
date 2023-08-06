import pymysql,requests,json
from retrying import retry
from influxdb import InfluxDBClient




class InfluxdbClient:
    def __init__(self, config, db_name):
        self.config = config
        self.db_name = db_name
        self.client = InfluxDBClient(self.config.get('server_ip'), 8086, self.config.get('username'), self.config.get('password'), self.db_name)

    @retry(stop_max_attempt_number=5, wait_random_min=200, wait_random_max=5000)
    def query_influxdb(self, query_string):
        return self.client.query(query_string)


class MysqlClient:
    def __init__(self, config):
        self.config=config

    def connectDatabase(self):
        try:
            self.conn = pymysql.connect(**self.config)
        except:
            print("connectDatabase failed")
            return False
        self.cur = self.conn.cursor()
        return True

    def close(self):
        if self.conn and self.cur:
            self.cur.close()
            self.conn.close()
        return True


    def execute(self, sql, params=None):
        self.connectDatabase()
        try:
            if self.conn and self.cur:
                self.cur.execute(sql, params)
                self.conn.commit()
        except:
            print("execute failed: " + sql)
            print("params: " + params)
            self.close()
            return False
        return True

    def fetchall(self, sql, params=None):
        self.execute(sql, params)
        return self.cur.fetchall()

    def fetchone(self, sql, params=None):
        self.execute(sql, params)
        return self.cur.fetchone()


def dingdingAlert(text, webhook):

    data={
        "msgtype": "text",
        "text": {
            "content": text
        },
        "at": {
            "atMobiles": [
            ],
            "isAtAll": False
        }
    }
    headers = {'Content-Type': 'application/json'}
    x=requests.post(url = webhook,data = json.dumps(data), headers = headers)
