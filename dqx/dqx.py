# -*- coding: utf-8 -*-

# 
# dqx.py
# 
# Created by FUKUBAYASHI Yuichiro on 2012/08/11
# Copyright (c) 2012, FUKUBAYASHI Yuichiro
# 
# last update: <2012/08/11 00:49:46>
# 

import urllib
import datetime
import re
from bs4 import BeautifulSoup
import bs4

URL_HIROBA_CHARA='http://hiroba.dqx.jp/sc/character/'
DATETIME_FORMAT=u'%Y/%m/%d %H:%M'
LASTUPDATE_PATTERN = re.compile(r'.*([0-9]{4}/[0-9]{1,2}/[0-9]{1,2} [0-9]{1,2}:[0-9]{1,2})')
STRIP_CHARS=u' 　[]： '

class User(object):
    def __init__(self, uid):
        self.uid = str(uid.strip())
        self.title = None
        self.name = None
        self.cid = None
        self.race = None
        self.sex = None
        self.job = None
        self.level = None
        self.imglastupdate = None

        self.welcomefriend = None
        self.message = None
        self.equipment = None
        self.location = None
        
        self.parameter = None
        self.skillpoint = {}
        self.skills = {}
        self.skilleffects = {}
        self.spells = []

    def retrieve_and_update_basic(self):
        profile_res = urllib.urlopen(self.url_profile)

        # リダイレクト (=非公開)
        if not self.url_profile == profile_res.geturl():
            raise RetrieveError(u'redirected from %s to %s' % (self.url_profile, profile_res.geturl()))

        self.update_profile(profile_res.read())
        

    def retrieve_and_update(self):
        self.retrieve_and_update_basic()

        # 詳細
        profile_detail_res = urllib.urlopen(self.url_profile_detail)
        self.update_profile_detail(profile_detail_res.read())
        

    def update_profile(self, html):
        soup = BeautifulSoup(html)

        # エラーチェック (raise ParseError)
        checkErrorPage(soup)

        # 称号
        soup_myCharacterTitle = getSoupElementById(soup, 'myCharacterTitle')
        title = getPlainText(soup_myCharacterTitle).strip(STRIP_CHARS)
        self.title = title

        # 名前
        soup_myCharacterName = getSoupElementById(soup, 'myCharacterName')
        name = getPlainText(soup_myCharacterName).strip(STRIP_CHARS)
        self.name = name

        # 状態
        soup_myCharacterStatusList = getSoupElementById(soup, 'myCharacterStatusList')
        status_list = getDicFromDL(soup_myCharacterStatusList('dl')[0])

        cid = status_list[u'キャラID'].strip(STRIP_CHARS)
        self.cid = cid

        race = status_list[u'種　族']
        self.race = race

        sex = status_list[u'性　別']
        self.sex = sex

        job = status_list[u'職　業']
        self.job = job

        level = int(status_list[u'レベル'])
        self.level = level

        # サポート仲間とうろく状況
        soup_welcomefriend = getSoupElementById(soup, 'welcomeFriend')
        dl_welcomefriend = soup_welcomefriend('dl')
        if len(dl_welcomefriend)>0:
            welcome_dict = getDicFromDL(dl_welcomefriend[0])
            self.welcomefriend = welcome_dict[u'サポート仲間とうろく中！']
            

        # 画像の最終更新日
        soup_txt_update = soup('p',{'class':'txt_update'})[0]
        txt_update = getPlainText(soup_txt_update).strip(STRIP_CHARS)
        lastupdate_matcher = LASTUPDATE_PATTERN.match(txt_update)
        if lastupdate_matcher:
            self.imglastupdate = datetime.datetime.strptime(lastupdate_matcher.group(1), DATETIME_FORMAT)

        
        # そうび
        soup_equipment = soup('div', {'class':'equipment'})[0]
        equipment_dict = getDictFromTable(soup_equipment('table')[0])

        self.equipment = Equipment(rhand=equipment_dict[u'みぎて'],
                                   lhand=equipment_dict[u'ひだりて'],
                                   head=equipment_dict[u'アタマ'],
                                   ubody=equipment_dict[u'からだ上'],
                                   lbody=equipment_dict[u'からだ下'],
                                   arm=equipment_dict[u'ウデ'],
                                   foot=equipment_dict[u'足'],
                                   faceacc=equipment_dict[u'顔アクセ'],
                                   neckacc=equipment_dict[u'首アクセ'],
                                   fingacc=equipment_dict[u'指アクセ'],
                                   othacc=equipment_dict[u'他アクセ'],
                                   art=equipment_dict[u'しょくにん'])
        
        # メッセージ
        soup_message = soup('div', {'class':'message'})[0]
        self.message = getPlainText(soup_message('p')[0]).strip()

        # いる場所
        soup_where = soup('div', {'class': 'where'})[0]
        location_dict = getDicFromDL(soup_where('dl')[0])
        self.location = Location(server=location_dict[u'サーバー'], field=location_dict[u'フィールド'])
        
        
    def update_profile_detail(self, html):
        soup = BeautifulSoup(html)
        
        # パラメータ
        soup_parameter = soup('div', {'class': 'parameter'})[0]
        parameter_dict = getDictFromTable(soup_parameter('table')[0])
        self.parameter = Parameter(
            maxhp=int(parameter_dict[u'さいだいHP']),
            maxmp=int(parameter_dict[u'さいだいMP']),
            attack=int(parameter_dict[u'こうげき力']),
            defend=int(parameter_dict[u'しゅび力']),
            mattack=int(parameter_dict[u'こうげき魔力']),
            mhealing=int(parameter_dict[u'かいふく魔力']),
            power=int(parameter_dict[u'ちから']),
            speed=int(parameter_dict[u'すばやさ']),
            guard=int(parameter_dict[u'みのまもり']),
            dext=int(parameter_dict[u'きようさ']),
            charm=int(parameter_dict[u'みりょく']),
            appearance=int(parameter_dict[u'おしゃれさ']),
            weight=int(parameter_dict[u'おもさ']))

        # スキルポイント
        soup_skillp = soup('div', {'class': 'skill'})[0]
        self.skillpoint = parseDictValues(getDictFromTable(soup_skillp('table')[0]), int)

        # とくぎ
        soup_skills = soup('div', {'class': 'specialSkill'})[0]
        self.skills = getDictFromTable(soup_skills('table')[0], tdIsList=True)

        # スキル効果
        soup_skilleffects = soup('div', {'class': 'skillEffect'})[0]
        self.skilleffects = getDictFromTable(soup_skilleffects('table')[0], tdIsList=True)

        # じゅもん
        soup_spells = soup('div', {'class': 'spell'})[0]
        self.spells =  getListFromTable(soup_spells('table')[0])


    @property
    def url_profile(self):
        return URL_HIROBA_CHARA + self.uid + "/"

    @property
    def url_profile_detail(self):
        return self.url_profile + "status/"

    @property
    def url_img_bup(self):
        return self.url_profile + "img/bup/"

    @property
    def url_img_all(self):
        return self.url_profile + "img/all/"

    def __unicode__(self):
        return u"uid:%s\nかたがき:%s\nなまえ:%s\nキャラID:%s\n種族:%s\n性別:%s\n\
職業:%s\nレベル:%s\nサポート仲間とうろく状況:%s\n画像の最終更新日時:%s\nメッセージ:%s\nいる場所:{%s}\nそうび:{%s}\n\
パラメータ:{%s}\nスキルポイント:{%s}\n\
とくぎ:{%s}\nスキル効果:{%s}\n\
じゅもん:[%s]" % (self.uid, self.title, self.name, self.cid, self.race, self.sex,
                  self.job, str(self.level), u'とうろく中 (%s)' % (self.welcomefriend) if self.welcomefriend else u'なし', self.imglastupdate, self.message, self.location, self.equipment,
                  self.parameter, dicToUnicode(self.skillpoint),
                  dicToUnicode(self.skills), dicToUnicode(self.skilleffects),
                  ",".join(self.spells))

    def __str__(self):
        return self.__unicode__().encode('utf-8')

class Equipment(object):
    def __init__(self,
                 rhand=None,
                 lhand=None,
                 head=None,
                 ubody=None,
                 lbody=None,
                 arm=None,
                 foot=None,
                 faceacc=None,
                 neckacc=None,
                 fingacc=None,
                 othacc=None,
                 art=None
                 ):
        self.rhand=rhand
        self.lhand=lhand
        self.head=head
        self.ubody=ubody
        self.lbody=lbody
        self.arm=arm
        self.foot=foot
        self.faceacc=faceacc
        self.neckacc=neckacc
        self.fingacc=fingacc
        self.othacc=othacc
        self.art=art

    def __unicode__(self):
        return u'みぎて:%s, ひだりて:%s, アタマ:%s, からだ上:%s, からだ下:%s, ウデ:%s, \
足:%s, 顔アクセ:%s, 首アクセ:%s, 指アクセ:%s, 他アクセ:%s, しょくにん:%s' % (self.rhand, self.lhand, self.head, self.ubody, self.lbody, self.arm,
                                                                             self.foot, self.faceacc, self.neckacc, self.fingacc, self.othacc, self.art)

    def __str__(self):
        return self.__unicode__().encode('utf-8')

class Location(object):
    def __init__(self, server=None, field=None):
        self.server = server
        self.field = field

    def __unicode__(self):
        return u'サーバー:%s, フィールド:%s' % (self.server, self.field)

    def __str__(self):
        return self.__unicode__().encode('utf-8')

class Parameter(object):
    def __init__(self,
                 maxhp=None,
                 maxmp=None,
                 attack=None,
                 defend=None,
                 mattack=None,
                 mhealing=None,
                 power=None,
                 speed=None,
                 guard=None,
                 dext=None,
                 charm=None,
                 appearance=None,
                 weight=None):
        self.maxhp=maxhp
        self.maxmp=maxmp
        self.attack=attack
        self.defend=defend
        self.mattack=mattack
        self.mhealing=mhealing
        self.power=power
        self.speed=speed
        self.guard=guard
        self.dext=dext
        self.charm=charm
        self.appearance=appearance
        self.weight=weight
        
    def __unicode__(self):
        return u'さいだいHP:%d, さいだいMP:%d, こうげき力:%d, しゅび力:%d, こうげき魔力:%d, \
かいふく魔力:%d, ちから:%d, すばやさ:%d, みのまもり:%d, きようさ:%d, みりょく:%d, おしゃれさ:%d, おもさ:%d' % (self.maxhp, self.maxmp, self.attack, self.defend, self.mattack,
                                                                                                               self.mhealing, self.power, self.speed, self.guard, self.dext, self.charm, self.appearance, self.weight)
    def __str__(self):
        return self.__unicode__().encode('utf-8')


def checkErrorPage(soup):
    error = soup(id='errorCommon')
    if len(error) > 0:
        raise ParseError('%s' % (getErrorMessage(error[0])))



def getSoupElementById(soup, id):
    return soup.find_all(id=id)[0]

def getDicFromDL(dl):
    dl_dict = {}
    key = None
    value = None

    for child in dl.find_all(['dt','dd']):
        if child.name == 'dt':
            key = getPlainText(child).strip(STRIP_CHARS)
        elif child.name == 'dd':
            value = getPlainText(child).strip(STRIP_CHARS)
            
            if (key is not None and value is not None):
                dl_dict[key] = value

                key = None
                value = None

    return dl_dict


def getDictFromTable(table, tdIsList=False):
    table_dict = {}

    for tr in table('tr'):
        th = tr('th')
        td = tr('td')
        
        if len(th)>0 and len(td)>0:
            key = getPlainText(th[0]).strip(STRIP_CHARS)

            if tdIsList:
                value = getListFromTd(td[0])
            else:
                value = getPlainText(td[0]).strip(STRIP_CHARS)

            table_dict[key] = value

    return table_dict


def getListFromTable(table):
    table_list = []

    for td in table('td'):
        text = getPlainText(td).strip(STRIP_CHARS)
        table_list.append(text)

    return table_list


def getPlainText(soup):
    text = ''.join([s.string.strip() if s.string else getPlainText(s) for s in soup ])
    return text

def getListFromTd(td):
    return_list=[]
    for a in td.find_all('a'):
        text = ''.join([s.string.strip() if s.string and isinstance(s, bs4.element.NavigableString) else "" for s in a])
        return_list.append(text)

    return return_list

def getErrorMessage(body):
    div = body('div',{'class': 'error_common'})[0]
    td_first = div('td')[0]

    return td_first['title']


def parseDictValues(dic, f):
    parsed_dic = {}
    for k in dic:
        parsed_dic[k] = f(dic[k])

    return parsed_dic

def dicToUnicode(dic):
    return u", ".join(map(lambda k: u"%s:%s" % (k, dicToUnicode(dic[k]) if isinstance(dic[k], dict) else ",".join(dic[k]) if isinstance(dic[k], list) else unicode(dic[k])), dic.keys()))



class RetrieveError(Exception):
    def __init__(self, message):
        self.message = message

    def __unicode__(self):
        return self.message

    def __str__(self):
        return self.__unicode__().encode('utf-8')


class ParseError(Exception):
    def __init__(self, message):
        self.message = message

    def __unicode__(self):
        return self.message

    def __str__(self):
        return self.__unicode__().encode('utf-8')


