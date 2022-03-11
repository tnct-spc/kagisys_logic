#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import signal
import sys
import nfc
import threading
import os

from zemisys_helper import ZemisysHelper


class NFC_Kagisys():
	"""サーボモータの制御"""
	def __init__(self):
		"""基本設定とスレッドの呼び出し"""
		#基本的なセッティング
		self.api_helper = ZemisysHelper()
		signal.signal(signal.SIGINT, self.exit_handler)
		th = threading.Thread(target=self.run, name="th", args=())
		th.setDaemon(True)
		th.start()

		while True:
			time.sleep(1000)

	def exit_handler(self, signal, frame):
		"""終了時処理"""
		print('Exit nfc')
		self.clf.close()
		sys.exit(0)

	def run(self):
		"""メイン"""
		self.clf = nfc.ContactlessFrontend('usb')

		#繰り返し
		while True:
			self.clf.connect(rdwr={'on-connect': self.touched,'interval': 0.01})
			time.sleep(3)
			print("relese")

	def touched(self,tag):
		"""タッチされたときの処理"""
		#idの照合
		tag_id = tag.identifier.encode("hex").lower()
		print(tag_id)

		# toggleの受け取り
		toggle = self.get_toggle()
		is_open = toggle == "open"

		if not self.api_helper.auth(tag_id, not is_open):  # 状態を変更したいので現在の状態の逆を渡す
			#データが正しいidと異なっていた場合
			print("No matching Key")
			print("setting OK.")
			return

		if toggle == "lock":
			#鍵の解錠
			os.system("open_kagi")
		elif toggle == "open":
			#鍵の施錠
			os.system("lock_kagi")
		else:
			print("error ! please check file path")

	def get_toggle(self):
		"""toggleデータの取得"""
		os.chdir("/home/pi/project/kagisys_logic/")
		file_ = open("kagisys.toggle")
		result = file_.read()
		file_.close()
		return result


if __name__ == '__main__':
	NFC_Kagisys()
