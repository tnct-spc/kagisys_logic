#! /usr/bin/python
# -*- coding: utf-8 -*-

import configparser
import json
import requests
import yaml


class ZemisysHelper():
    def __init__(self):
        """APIのURLをkagisys.confから取ってくる"""
        self.config = configparser.SafeConfigParser()
		self.config.read('/home/pi/project/kagisys.conf')
        api_url = self.config.get('Zemisys', 'url')
        self.url = api_url

    def auth(idm, is_open):
        # ZemisysのDBに小文字で保存しているので一応処理する
        idm = idm.lower()

        headers = {
            "content-type": "application/json"
        }
        auth_data = json.dumps({
            "idm": idm,
            "is_open": is_open
        })
        response = requests.post(url=self.url, data=auth_data, headers=headers)
        res_json = response.json()

        # is_authがfalseだったら認証失敗
        return res_json.is_auth is not None
