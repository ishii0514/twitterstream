# -*- coding: utf-8 -*-

import base64
import simplejson
import urllib2
import datetime
import ConfigParser
from cgi import escape

# Streaming APIのURL
STREAM_URL = 'https://stream.twitter.com/1/statuses/sample.json'


class Config:
    """設定情報クラス"""
    def __init__(self,file):
        conf = ConfigParser.SafeConfigParser()
        conf.read(file)
        self.username=conf.get('account','username')
        self.password=conf.get('account','password')
        self.streamingtime=int(conf.get('options','streamingtime'))
        self.start = datetime.datetime.now()
    
    def setstart(self):
        self.start = datetime.datetime.now()
    
    def is_timeover(self):
        return (self.streamingtime != 0 and datetime.datetime.now() - self.start > datetime.timedelta(seconds=self.streamingtime))


def is_japanese(text):
    """textにひらがなかカタカナが含まれていたら真を返す。"""
    def check_chr(x):
        return ((x >= 0x3040 and x <= 0x309f) or (x >= 0x30a0 and x <= 0x30ff))
    return [ch for ch in text if check_chr(ord(ch))]

def printHTML(json):
    data = simplejson.loads(json)
    text = data.get('text')
    if text: #and is_japanese(text):
        print('<li>'
              '<img src="%s" /> <a href="http://twitter.com/%s">%s</a> %s'
              '</li>' %
              (escape(data['user']['profile_image_url'].encode('utf-8', 'ignore')),
               escape(data['user']['screen_name'].encode('utf-8', 'ignore')),
               escape(data['user']['screen_name'].encode('utf-8', 'ignore')),
               escape(data['text'].encode('utf-8', 'ignore'))))

def getstream(conf):
    """ツイッターStreaming APIから読み込んだツイートを出力"""
    req = urllib2.Request(STREAM_URL, headers={
                          'Authorization':
                          'Basic %s' % (base64.encodestring('%s:%s' % (conf.username, conf.password))[:-1])
                          })
    
    ua = urllib2.urlopen(req)
    conf.setstart()
    for line in ua:
        printHTML(line)
        if conf.is_timeover():
            break



def main():
    #設定情報取得
    conf = Config('setting.ini')
    #stream取得
    getstream(conf)
    

if __name__ == '__main__':
    main()