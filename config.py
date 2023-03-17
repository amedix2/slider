#   from pathlib import Path


class colors:
    light_grey = '#DDDDDD'
    super_light_grey = '#EFEFEF'


class app_settings:
    path = ''
    name = ''
    ip_serv = '92.241.227.146'

    def set_path(self, p):
        app_settings.path = p
        app_settings.name = p.split('/')[-1]

    def set_ip(self, ip):
        app_settings.ip_serv = ip
