#!/usr/bin/env python

import sys
import zabbix_api
from os import _exit


zabbix = 'server'
zabbixuser = 'user'
zabbixpasswd = 'password'
zabbixurl = 'http://%s/api_jsonrpc.php' % zabbix
domain = 'domain'
description = 'Doing backup'


def main( action, host ):
    zapi = zabbix_api.ZabbixAPI(server = zabbixurl)
    zapi.login(user = zabbixuser, password = zabbixpasswd)
    if not zapi.test_login(): _exit(1)
    hostid = zapi.host.get( {'filter': { 'host': '%s.%s' % (host, domain) }}  )[0]['hostid']
    try:
        if action == 'set':
            zapi.maintenance.create( { 'name': 'Backup', 'hostids': [ hostid ], 'timeperiods': [ { 'timeperiod_type': 0 } ], 'description': description } )
        elif action == 'unset':
            try:
                maintenanceid = zapi.maintenance.get( { 'hostids': [ hostid ], 'search': { 'name': [ 'Backup' ]}} )[0]['maintenanceid']
            except IndexError:
                _exit(0)
            except:
                raise
                _exit(1)
            zapi.maintenance.delete( maintenanceid )
        _exit(0)
    except zabbix_api.ZabbixAPIException:
        raise
        _exit(1)
    _exit(1)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print '''Usage: %s <action> <hostname>
action: set, unset''' % sys.argv[0]
        _exit(1)
    main( sys.argv[1], sys.argv[2] )
