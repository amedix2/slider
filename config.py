from PyQt5.QtWidgets import QMessageBox


class colors:
    light_grey = '#c8d1db'
    super_light_grey = '#dedede'
    super_dark_grey = '#121212'
    dark_grey = '#262626'

    color_main = super_light_grey
    color_supp = light_grey

    @staticmethod
    def set_theme(self, theme):
        if theme == 'light':
            colors.color_bg = colors.super_light_grey
            colors.color_btn = colors.light_grey
        elif theme == 'dark':
            colors.color_bg = colors.super_dark_grey
            colors.color_btn = colors.dark_grey

        QMessageBox.critical(self, 'restart an app', 'Перезапустите приложение, чтобы изменения вступили в силу')


class app_settings:
    version = 'Slider alfa ver 1.03'
    ip_serv = '45.9.41.237'

    path = ''
    name = ''

    @staticmethod
    def set_path(p):
        app_settings.path = p
        app_settings.name = p.split('/')[-1]

    @staticmethod
    def set_ip(ip):
        app_settings.ip_serv = ip