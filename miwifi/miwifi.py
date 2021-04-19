import time as Time
import math as Math
import random as Random
from Crypto.Hash import SHA1
import json
import requests


def sha1(string):
    return SHA1.new(str.encode(string)).hexdigest()


class Api:
    url = ''
    token = ''
    key = ''
    deviceId = ''
    addr = ''
    password = ''

    def __init__(self, key, deviceId, addr, password) -> None:
        self.key = key
        self.deviceId = deviceId
        self.addr = addr
        self.password = password
        self.login()

    def _post(self, url, parm) -> dict:
        while(True):
            print('[UP][POST][Url]:%s [Data]%s' %
                  (self.addr+url, json.dumps(parm)))
            req = requests.post(url=self.addr+url, data=parm).text
            print('[DOWM][POST][Data]%s' % (req))
            r = json.loads(req)
            if(r['code'] == 401):
                self.verifyToken()
            else:
                break
        return r

    def _get(self, url) -> dict:
        while(True):
            print('[UP][GET][Url]:%s' % (self.addr+url))
            req = requests.get(url=self.addr+url).text
            print('[DOWM][GET][Data]%s' % (req))
            r = json.loads(req)
            if(r['code'] == 401):
                self.verifyToken()
            else:
                break
        return r

    def post(self, url, parm) -> dict:
        return self._post(url=self.url+url, parm=parm)

    def get(self, url) -> dict:
        return self._get(url=self.url+url)

    def login(self) -> dict:
        nonce = "_".join([str(0), str(self.deviceId), str(Math.floor(
            Time.time())), str(Math.floor(Random.randint(1, 10000)))])
        param = {'username': 'admin', 'password': sha1(
            nonce + sha1(self.password + self.key)), 'logtype': 2, 'nonce': nonce}
        req = self._post('/cgi-bin/luci/api/xqsystem/login', param)
        self.url = req['url'].rstrip('/web/home')
        self.token = req['token']

    def verifyToken(self):
        while(True):
            if(self.api_misystem_messages()['code'] == 401):
                self.login()
            else:
                break

    # GET请求
    def api_misystem_messages(self) -> dict:
        return self.get('/api/misystem/messages')

    def api_xqnetdetect_nettb(self) -> dict:
        return self.get('/api/xqnetdetect/nettb')

    def api_xqnetwork_wifi_detail_all(self) -> dict:
        return self.get('/api/xqnetwork/wifi_detail_all')

    def api_misystem_bandwidth_test(self) -> dict:
        return self.get('/api/misystem/bandwidth_test?history=1')

    def api_misystem_newstatus(self) -> dict:
        return self.get('/api/misystem/newstatus')

    def api_xqsystem_country_code(self) -> dict:
        return self.get('/api/xqsystem/country_code')

    def api_xqnetwork_wan_info(self) -> dict:
        return self.get('/api/xqnetwork/wan_info')

    def api_xqnetwork_pppoe_status(self) -> dict:
        return self.get('/api/xqnetwork/pppoe_status')

    def api_misystem_web_access_info(self) -> dict:
        return self.get('/api/misystem/web_access_info')

    def api_xqnetwork_wifi_macfilter_info(self) -> dict:
        return self.get('/api/xqnetwork/wifi_macfilter_info')

    def api_xqnetwork_lan_dhcp(self) -> dict:
        return self.get('/api/xqnetwork/lan_dhcp')

    def api_xqnetwork_lan_info(self) -> dict:
        return self.get('/api/xqnetwork/lan_info')

    def api_xqsystem_check_rom_update(self) -> dict:
        return self.get('/api/xqsystem/check_rom_update')

    def api_misystem_sys_time(self) -> dict:
        return self.get('/api/misystem/sys_time')

    def api_misystem_qos_info(self) -> dict:
        return self.get('/api/misystem/qos_info')

    def api_misns_wifi_share_info(self) -> dict:
        return self.get('/api/misns/wifi_share_info')

    def api_xqnetwork_macbind_info(self) -> dict:
        return self.get('/api/xqnetwork/macbind_info')

    def api_xqnetwork_ddns(self) -> dict:
        return self.get('/api/xqnetwork/ddns')

    def api_xqnetwork_portforward_list1(self) -> dict:
        return self.get('/api/xqnetwork/portforward?ftype=1')

    def api_xqnetwork_portforward_list2(self) -> dict:
        return self.get('/api/xqnetwork/portforward?ftype=2')

    def api_xqnetwork_dmz(self) -> dict:
        return self.get('/api/xqnetwork/dmz')

    def api_xqsystem_vpn(self) -> dict:
        return self.get('/api/xqsystem/vpn')

    def api_misystem_smartvpn_info(self) -> dict:
        return self.get('/api/misystem/smartvpn_info')

    def api_misystem_mi_vpn_info(self) -> dict:
        return self.get('/api/misystem/mi_vpn_info')

    def api_xqsystem_vpn_status(self) -> dict:
        return self.get('/api/xqsystem/vpn_status')

    def api_xqsystem_upnp(self) -> dict:
        return self.get('/api/xqsystem/upnp')

    # 端口转发保存
    def api_xqnetwork_redirect_apply(self) -> dict:
        return self.get('/api/xqnetwork/redirect_apply')

    # POST请求
    # 单个端口转发添加
    def api_xqnetwork_add_redirect(self, name, proto, sport, ip, dport) -> dict:
        return self.post('/api/xqnetwork/add_redirect', {'name': name, 'proto': proto, 'sport': sport, 'ip': ip, 'dport': dport})

    # 单个/范围端口转发删除
    def api_xqnetwork_delete_redirect(self, port, proto) -> dict:
        return self.post('/api/xqnetwork/delete_redirect', {'port': port, 'proto': proto})

    #范围端口转发
    def api_xqnetwork_add_range_redirect(self,name,proto,fport,tport,ip) -> dict:
        return self.post('/api/xqnetwork/add_range_redirect',{'name': name, 'proto': proto, 'fport': fport, 'tport': tport, 'ip': ip})