#                             pyCloudFlareUpdater
#                  Copyright (C) 2019 - Javinator9889
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#                   (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#               GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.


class UserPreferences(object):
    def __init__(self, **kwargs):
        if kwargs:
            try:
                self.__domain = kwargs["domain"]
                self.__name = kwargs["name"]
                self.__time = kwargs["time"]
                self.__key = kwargs["key"]
                self.__mail = kwargs["mail"]
                self.__proxy = kwargs["proxy"]
                self.__pid = kwargs["pid"]
                self.__log = kwargs["log"]
            except KeyError:
                raise AttributeError("Some value was not provided while creating user preferences\n"
                                     "Values are:\n"
                                     "  - Domain\n"
                                     "  - Name (of A Record)\n"
                                     "  - Time (update time)\n"
                                     "  - Key\n")
        else:
            self.__domain = None
            self.__name = None
            self.__time = None
            self.__key = None
            self.__mail = None
            self.__pid = None
            self.__log = None
        self.__latest_ip = "0.0.0.0"
        self.__proxy = True
        self.__daemonize = True

    @staticmethod
    def get_preferences_file():
        import os

        return os.path.dirname(os.path.abspath(__file__)) + "/cloudflare.user.preferences"

    def load_preferences(self):
        import pickle
        import os

        from base64 import b64decode

        if os.path.exists("cloudflare.user.preferences"):
            with open("cloudflare.user.preferences", "rb") as fpreferences:
                preferences = pickle.load(fpreferences)
            self.__domain = preferences["domain"]
            self.__time = preferences["time"]
            self.__key = b64decode(preferences["key"]).decode("utf-8")
            self.__mail = b64decode(preferences["mail"]).decode("utf-8")
            self.__name = preferences["name"]
            self.__proxy = preferences["proxy"]
            self.__latest_ip = preferences["latest_ip"]
            self.__pid = preferences["pid"]
            self.__log = preferences["log"]
        else:
            raise FileNotFoundError("There are no saved user preferences. Call \"save_preferences\" the first time")

    def save_preferences(self, filename="cloudflare.user.preferences"):
        import pickle

        from base64 import b64encode
        from os import path
        from os import makedirs

        preferences = {"domain": self.__domain,
                       "name": self.__name,
                       "time": self.__time,
                       "key": b64encode(bytes(self.__key, "utf-8")),
                       "mail": b64encode(bytes(self.__mail, "utf-8")),
                       "proxy": self.__proxy,
                       "latest_ip": self.__latest_ip,
                       "pid": self.__pid,
                       "log": self.__log}
        file_dir = path.dirname(path.abspath(filename))
        if not path.exists(file_dir):
            makedirs(path=file_dir, exist_ok=True)
        with open(filename, "wb") as fpreferences:
            pickle.dump(preferences, fpreferences, pickle.HIGHEST_PROTOCOL)

    def get_domain(self):
        return self.__domain

    def get_name(self):
        return self.__name

    def get_time(self):
        return self.__time

    def get_key(self):
        return self.__key

    def get_mail(self):
        return self.__mail

    def is_record_behind_proxy(self):
        return self.__proxy

    def get_latest_ip(self):
        return self.__latest_ip

    def get_pid_file(self):
        return self.__pid

    def get_log_file(self):
        return self.__log

    def is_running_as_daemon(self):
        return self.__daemonize

    def set_domain(self, domain):
        self.__domain = domain

    def set_name(self, name):
        self.__name = name

    def set_time(self, time):
        self.__time = time

    def set_key(self, key):
        self.__key = key

    def set_mail(self, mail):
        self.__mail = mail

    def set_latest_ip(self, ip):
        self.__latest_ip = ip

    def set_pid_file(self, pid):
        self.__pid = pid

    def set_log_file(self, log):
        self.__log = log

    def record_behind_proxy(self, behind_proxy: bool):
        self.__proxy = behind_proxy

    def run_as_daemon(self, daemonize: bool):
        self.__daemonize = daemonize

    @staticmethod
    def are_preferences_stored():
        import os

        return os.path.exists("cloudflare.user.preferences")
