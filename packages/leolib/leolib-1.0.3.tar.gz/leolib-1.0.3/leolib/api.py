import datetime

import requests


def get_day(days: int = 0):
    """
    返回的日期格式 %Y-%m-%d
    :param days: 距离今天的天数
    :return: 格式 %Y-%m-%d
    """
    return (datetime.datetime.now() + datetime.timedelta(days=days)).strftime("%Y-%m-%d")


def get_time(str_time=None, fix=True):
    """
    获取分钟时间
    :param fix: 获取以30分钟为分度的分钟时间
    :param str_time: 格式 %H:%M 范围: 7:30 - 22:30
    :return: int: 分钟
    """
    if str_time is None:
        str_time = datetime.datetime.now().strftime("%H:%M")
        fix = False
    if len(str(str_time).split(":")) == 1:
        hour = datetime.datetime.now().hour + int(str_time)
        minute = datetime.datetime.now().minute
    else:
        hour = int(str_time.split(":")[0])
        minute = int((int(str_time.split(":")[1]) // 30)
                    * 30) if fix else int(str_time.split(":")[1])
    return minute + hour * 60


class User:
    def __return_and_log(self, json):
        if self.log_status:
            with open("seat_log.log", "a", encoding="utf-8") as f:
                f.write(
                    f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\t{str(self.username)}:\t{str(json)}\n')
        return json

    def _get_token(self):
        """
        获取token
        :return:
        """
        params = {
            "username": self.username,
            "password": self.password
        }
        res = requests.get(self.base_url + "/rest/auth",
                           params=params, headers=self.headers)
        # print(res.json()['data']['token'])
        if res.status_code == 200:
            if res.json()['status'] == "success":
                return res.json()['data']['token']

    def get_user_info(self):
        """
        获取用户信息
        :return:
        """
        params = {
            "token": self.token
        }
        res = requests.get(self.base_url + "/rest/v2/user",
                           params=params, headers=self.headers)
        if res.status_code == 200:
            return self.__return_and_log(res.json())

    def get_history(self):
        """
        获取历史信息
        :return:
        """
        params = {
            "token": self.token
        }
        res = requests.get(self.base_url + "/rest/v2/history/1/10",
                           params=params, headers=self.headers)
        if res.status_code == 200:
            return self.__return_and_log(res.json())

    def get_violation(self):
        """
        获取60天内的违约信息
        :return:
        """
        params = {
            "token": self.token
        }
        res = requests.get(self.base_url + "/rest/v2/violations",
                           params=params, headers=self.headers)
        if res.status_code == 200:
            return self.__return_and_log(res.json())

    def get_lib_status(self, lib_id, date):
        """
        获取馆内座位预约情况
        :param lib_id: 图书馆id
        :param date: %Y-%m-%d
        :return:
        """
        params = {
            "token": self.token
        }
        res = requests.get(
            self.base_url + f"/rest/v2/room/stats2/{lib_id}/{date}", params=params, headers=self.headers)
        if res.status_code == 200:
            return self.__return_and_log(res.json())

    def get_room(self):
        """
        获取所有房间信息
        :return:
        """
        params = {
            "token": self.token
        }
        res = requests.get(self.base_url + f"/rest/v2/free/filters",
                           params=params, headers=self.headers)
        if res.status_code == 200:
            return self.__return_and_log(res.json())

    def get_room_status(self, room_id, date):
        """
        获取房间内的详细信息，包括布局信息
        :param room_id: 房间 id
        :param date: %Y-%m-%d
        :return:
        """
        params = {
            "token": self.token
        }
        res = requests.get(self.base_url + f"/rest/v2/room/layoutByDate/{room_id}/{date}", params=params,
                           headers=self.headers)
        if res.status_code == 200:
            return self.__return_and_log(res.json())

    def get_reservation(self):
        """
        获取当前自己的座位预约信息
        :return:
        """
        params = {
            "token": self.token
        }
        res = requests.post(
            self.base_url + "/rest/v2/user/reservations", data=params)
        if res.status_code == 200:
            return self.__return_and_log(res.json())

    def search_seat(self, start_time, end_time, date, room_id):
        """
        可用座位查询
        :param start_time: 开始时间 分钟
        :param end_time: 结束时间 分钟
        :param date: 日期 %Y-%m-%d
        :param room_id: 房间 id
        :return:
        """
        params = {
            "token": self.token,
            "roomId": room_id,
            "batch": 9999,
            "page": 1
        }
        res = requests.get(self.base_url + f"/rest/v2/searchSeats/{date}/{start_time}/{end_time}", params=params,
                           headers=self.headers)
        if res.status_code == 200:
            return self.__return_and_log(res.json())

    def book_seat(self, seat_id, start_time, end_time, date):
        """
        预约座位
        :param seat_id: 座位 id
        :param start_time: 开始时间
        :param end_time: 结束时间
        :param date: 日期
        :return:
        """
        data = {
            "token": self.token,
            "seat": seat_id,
            "startTime": start_time,
            "endTime": end_time,
            "date": date
        }
        res = requests.post(self.base_url + "/rest/v2/freeBook", data=data)
        if res.status_code == 200:
            return self.__return_and_log(res.json())

    def check_in(self):
        """
        请在预约开始时间前 30 分钟 或 后 15 内签到
        :return:
        """
        params = {
            "token": self.token
        }
        res = requests.get(self.base_url + "/rest/v2/checkIn",
                           params=params, headers=self.headers)
        if res.status_code == 200:
            return self.__return_and_log(res.json())

    def cancel_book(self, reserve_id):
        """
        取消预约座位
        :param reserve_id: 预约 id
        :return:
        """
        params = {
            "token": self.token
        }
        res = requests.get(
            self.base_url + f"/rest/v2/cancel/{reserve_id}", params=params, headers=self.headers)
        # print(res.text)
        if res.status_code == 200:
            return self.__return_and_log(res.json())

    def release_seat(self):
        """
        会释放当前正在履约的座位
        :return:
        """
        params = {
            "token": self.token
        }
        res = requests.get(self.base_url + f"/rest/v2/stop",
                           params=params, headers=self.headers)
        if res.status_code == 200:
            return self.__return_and_log(res.json())

    def __init__(self, username, password, base_url, log_status=False):
        self.headers = {
            "User-Agent": "doSingle/11 CFNetwork/811.5.4 Darwin/16.6.0"
        }
        self.base_url = base_url
        self.username = username
        self.password = password
        self.log_status = log_status
        # 获取 token
        self.token = self._get_token()
