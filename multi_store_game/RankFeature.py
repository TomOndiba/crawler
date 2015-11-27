# -*- coding: utf-8 -*-

import re
import glob

import BaiduExtractor
import WandoujiaExtractor
import XiaomiExtractor
import YingyongbaoExtractor
import Zhushou360Extractor

rankDB = {}
storeCates= {'baidu': ['allranking', 'xiuxianyizhi', 'dongzuosheji',        
                       'tiyujingji', 'jingyingyangcheng', 'juesebanyan',           
                       'saichejingsu', 'monifuzhu', 'qipaizhuoyou'],
             'wandoujia': ['allranking', 'xiuxianshijian', 'paokujingsu',   
                       'dongzuosheji', 'pukeqipai', 'tiyugedou',                   
                       'juesebanyan', 'baoshixiaochu', 'wangluoyouxi',             
                       'ertongyizhi', 'tafangshouwei', 'jingyingcelue'],
             'xiaomi': ['allranking', 'zhanzhengcelue', 'dongzuoqiangzhan', 
                       'saichetiyu', 'wangyouRPG', 'qipaizhuoyou', 
                       'gedoukuaida', 'ertongyizhi', 'xiuxianchuangyi',
                       'feixingkongzhan', 'paokuchuangguan', 'tafangmigong', 
                       'monijingying'],
             'yingyongbao': ['allranking', 'xiuxianyizhi', 'wangluoyouxi', 
                       'dongzuomaoxian', 'qipaizhongxin', 'feixingsheji', 
                       'jingyingcelue', 'juesebanyan', 'tiyujingsu'],
             'zhushou360': ['allranking', 'juesebanyan', 'xiuxianyizhi', 
                       'dongzuomaoxian', 'wangluoyouxi', 'tiyujingsu', 
                       'feixingsheji','jingyingcelue','qipaitiandi', 
                       'ertongyouxi']
             }


def queryThisStore(store, date):
    if store == 'baidu':
        extract = BaiduExtractor.extract
    elif store == 'wandoujia':
        extract = WandoujiaExtractor.extract
    elif store == 'xiaomi':
        extract = XiaomiExtractor.extract
    elif store == 'yingyongbao':
        extract = YingyongbaoExtractor.extract
    elif store == 'zhushou360':
        extract = Zhushou360Extractor.extract
    else:
        return None
    #htmlPath = '/home/zzhou/crawler/multi_store_game/%s/html' % store
    htmlPath = '%s/html' % store
    if store not in storeCates:
        return None
    cateList = storeCates[store]
    # query app-rank dict
    # for each category (and each webpage of a category)
    for cate in cateList:
        fList = glob.glob('%s/%s*%s*' % (htmlPath, cate, date))
        sortByPage(fList, store)
        bias = 0
        for fn in fList:
            with open(fn) as f:
                page = f.read()
                bias, appRank = extract(page, cate, bias)
                updateRankDB(appRank, store)


def sortByPage(fList, store):
    cmpByPage = lambda x,y: cmp(int(x.split('_')[1]), int(y.split('_')[1]))
    if store in ['baidu', 'xiaomi', 'zhushou360']:
        fList.sort(cmp=cmpByPage)


def updateRankDB(appRank, store):
    # appRank format: [app, cate, rank]
    # rankDB format: {app: {store: {cate: rank}}}
    for item in appRank:
        app  = item[0]
        cate = item[1]
        rank = item[2]
        if app not in rankDB:
            # w/o app
            rankDB[app] = {store: {cate: rank}}
        elif store not in rankDB[app]:
            # w/ app, w/o store
            rankDB[app][store] = {cate: rank}
        elif cate not in rankDB[app][store]:
            # w/ app and store, w/o cate
            rankDB[app][store][cate] = rank
        else:
            # w/ app and store and cate
            # data conflict, remain previous value
            continue
    
    
def writeResult(filename):
    f = open(filename, 'w')
    for app in rankDB:
        scr = rankDB[app]
        outline = app 
        for store in scr:
            cr = scr[store]
            outline += '|' + store + ' '
            for cate in cr:
                rank = cr[cate]
                outline += '%s:%s ' % (cate, rank)
        print >> f, outline


def getRankFeature(date):
    for store in storeCates:
        queryThisStore(store, date)
    writeResult('result')


if __name__ == '__main__':
    date = '20151127'
    getRankFeature(date)
