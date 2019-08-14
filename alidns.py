# copy from https://github.com/luoyeah/alidns

from aliyunsdkcore import client
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest       import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DeleteDomainRecordRequest    import DeleteDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest    import UpdateDomainRecordRequest

import os, json, socket

class Alidns(object):
    def __init__(self, access_key, access_key_secret, domain):
        '''init'''
        self.__domain = domain
        self.__client = client.AcsClient(access_key, access_key_secret, 'cn-hangzhou')
        self.__records = self.query()
        self.__print = ''

    def query(self):
        '''Query all host records.'''
        req = DescribeDomainRecordsRequest()
        req.set_accept_format('json')
        req.set_DomainName(self.__domain)
        js = json.loads(self.__client.do_action_with_exception(req).decode())
        ret = {}
        strs = ''
        for x in js['DomainRecords']['Record']:
            RR = x['RR']
            Type = x['Type']
            Value = x['Value']
            RecordId = x['RecordId']
            TTL = x['TTL']
            strs = strs + '[*]%12s.%s -> %-24s;  %-12s;%s\n' % (RR, self.__domain, Value, Type, TTL)
            ret[RR] = [Value, Type, TTL, RecordId]
        self.__print = strs
        return ret

    def list(self, update=True):
        '''Print query results.'''
        if update:
            self.query()
        print(self.__print, flush=True)

    def __is_exist(self, r):
        '''Record exist?'''
        for i in self.__records:
            if r == i:
                return True
        return False

    def __get_ip(self):
        '''Get default interface ip address(v4)'''
        s = socket.socket()
        s.connect(('baidu.com',80))
        r = s.getsockname()[0]
        s.close()
        return r

    def __update_record(self, record_id, record, value, record_type, ttl):
        '''Update record.'''
        req = UpdateDomainRecordRequest()
        req.set_RecordId(record_id)
        req.set_accept_format('json')
        req.set_RR(record)
        req.set_Type(record_type)
        req.set_TTL(ttl)
        req.set_Value(value)
        js = json.loads(self.__client.do_action_with_exception(req).decode())
        print('[U]%12s.%s -> %-24s;  %-12s;%s' % (record, self.__domain, value, record_type, ttl), flush=True)
        
    def __add_record(self, record, value, record_type, ttl):
        '''Add record.'''
        req = AddDomainRecordRequest()
        req.set_DomainName(self.__domain)
        req.set_accept_format('json')
        req.set_RR(record)
        req.set_Type(record_type)
        req.set_TTL(ttl)
        req.set_Value(value)
        js = json.loads(self.__client.do_action_with_exception(req).decode())        
        print('[A]%12s.%s -> %-24s;  %-12s;%s' % (record, self.__domain, value, record_type, ttl), flush=True)

    def add(self, record, value, record_type='A', ttl=600):
        '''Add record'''
        if not record:
            record = '@'
        if self.__is_exist(record):
            if not value:
                if self.__records[record][1] == 'A':
                    value = self.__get_ip()
                else:
                    value = self.__records[record][0] 
            ttl = int(ttl)
                
            if self.__records[record][0] != value:
                self.__update_record(self.__records[record][3], record, value, record_type, ttl)
            elif self.__records[record][1] != record_type:
                self.__update_record(self.__records[record][3], record, value, record_type, ttl)
            elif self.__records[record][2] != ttl:
                self.__update_record(self.__records[record][3], record, value, record_type, ttl)
            else:
                pass
        else:
            if not value:
                value = self.__get_ip()
            self.__add_record(record, value, record_type, ttl)
        # self.list()
        
    def __remove_record(self, record_id):
        '''Remove record'''
        req = DeleteDomainRecordRequest()
        req.set_RecordId(record_id)
        js = json.loads(self.__client.do_action_with_exception(req).decode())
            
    def remove(self, record):
        '''Remove record'''
        if self.__is_exist(record):
            self.__remove_record(self.__records[record][3])
        else:
            print('[-]Record: {} is not existence.'.format(record), flush=True)
        self.list()
        