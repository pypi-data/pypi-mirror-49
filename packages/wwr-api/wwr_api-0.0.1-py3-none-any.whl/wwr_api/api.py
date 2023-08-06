#! /usr/bin/env python3
import json
import hashlib
import base64
import requests

__all__ = [
  "WorkWechatRobotAPI",
]


class WorkWechatRobotAPI(object):
  def __init__(self, web_hook):
    self.__web_hook_addr = web_hook

  def send_raw_data(self, data):
    headers = {'content-type': 'application/json'}
    response = requests.post(self.__web_hook_addr, data=json.dumps(data), headers=headers)
    print(data)
    print(response.content)

  def send_markdown(self, markdown, at_list=None):
    if at_list is None:
      at_list = []
    data = {
      "msgtype": "markdown",
      "markdown": {
        "content": markdown,
        "mentioned_list": at_list
      }
    }
    self.send_raw_data(data)

  def send_pic(self, uri):
    if uri.startswith("https://") or uri.startswith("http://"):
      context = requests.get(uri).content
    else:
      with open(uri, "rb") as f:
        context = f.read()

    b64code = base64.b64encode(context).decode("utf-8")
    md5 = hashlib.md5(context).hexdigest()

    data = {
      "msgtype": "image",
      "image": {
        "base64": b64code,
        "md5": md5
      }
    }

    self.send_raw_data(data)
