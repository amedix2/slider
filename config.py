class colors:
    light_grey = '#DEDEDE'


class app_settings:
    path = ''
    name = ''
    ip_serv = '217.29.179.167'

    def set_path(self, p):
        app_settings.path = p
        app_settings.name = p.split('/')[-1]

    def set_ip(self, ip):
        app_settings.ip_serv = ip
