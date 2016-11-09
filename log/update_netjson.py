

dic = {"interface": {"GLOBAL": {"OUT": 0.0, "IN": 0.0},
  "vEth16": {"OUT": 0.0, "IN": 0.0},
  "vEth17": {"OUT": 0.0, "IN": 0.0},
  "vEth14": {"OUT": 0.0, "IN": 0.0},
  "vEth15": {"OUT": 0.0, "IN": 0.0},
  "vEth12": {"OUT": 0.0, "IN": 0.0},
  "vEth13": {"OUT": 0.0, "IN": 0.0},
  "vEth10": {"OUT": 0.0, "IN": 0.0},
  "vEth11": {"OUT": 0.0, "IN": 0.0},
  "vEth18": {"OUT": 0.0, "IN": 0.0},
  "vEth19": {"OUT": 0.0, "IN": 0.0},
  "vEth4": {"OUT": 0.0, "IN": 0.0},
  "vEth5": {"OUT": 0.0, "IN": 24.95},
  "vEth6": {"OUT": 0.0, "IN": 0.0},
  "vEth7": {"OUT": 0.0, "IN": 0.0},
  "vEth0": {"OUT": 0.0, "IN": 0.0},
  "vEth1": {"OUT": 0.0, "IN": 0.0},
  "vEth2": {"OUT": 0.0, "IN": 287.77},
  "vEth3": {"OUT": 287.34, "IN": 0.0},
  "vEth8": {"OUT": 0.0, "IN": 0.0},
  "vEth9": {"OUT": 0.0, "IN": 0.0},
  "vEth21": {"OUT": 0.0, "IN": 0.0},
  "vEth20": {"OUT": 0.0, "IN": 0.0}},
  "application": [{"1": "28.42MB/s"}, {"0": "2.78MB/s"}],
  "user": [{"iDownload": "7.41MB/s", "iGroupID": "Anonymous", "sUserName": "172.16.6.124", "iUpload": "2.81MB/s"}, {"iDownload": "3.38MB/s", "iGroupID": "Anonymous", "sUserName": "172.16.4.24", "iUpload": "150.54KB/s"}, {"iDownload": "102.39KB/s", "iGroupID": "Anonymous", "sUserName": "172.16.4.231", "iUpload": "2.06MB/s"}, {"iDownload": "1.58MB/s", "iGroupID": "Anonymous", "sUserName": "172.16.7.207", "iUpload": "75.14KB/s"}, {"iDownload": "39.12KB/s", "iGroupID": "Anonymous", "sUserName": "172.16.1.28", "iUpload": "1.52MB/s"}, {"iDownload": "1.41MB/s", "iGroupID": "Anonymous", "sUserName": "172.16.4.178", "iUpload": "50.98KB/s"}, {"iDownload": "70.57KB/s", "iGroupID": "Anonymous", "sUserName": "172.16.4.194", "iUpload": "1.2MB/s"}, {"iDownload": "221.26KB/s", "iGroupID": "Anonymous", "sUserName": "172.16.5.179", "iUpload": "547.58KB/s"}, {"iDownload": "52.22KB/s", "iGroupID": "Anonymous", "sUserName": "172.16.2.145", "iUpload": "708.37KB/s"}, {"iDownload": "32.97KB/s", "iGroupID": "Anonymous", "sUserName": "172.16.4.203", "iUpload": "455.93KB/s"}, {"iDownload": "32.51KB/s", "iGroupID": "Anonymous", "sUserName": "172.16.12.51", "iUpload": "435.67KB/s"}, {"iDownload": "8.42KB/s", "iGroupID": "Anonymous", "sUserName": "172.16.2.78", "iUpload": "401.58KB/s"}, {"iDownload": "83.02KB/s", "iGroupID": "Anonymous", "sUserName": "172.16.2.152", "iUpload": "233.66KB/s"}, {"iDownload": "22.25KB/s", "iGroupID": "Anonymous", "sUserName": "172.16.5.135", "iUpload": "283.34KB/s"}, {"iDownload": "0B/s", "iGroupID": "Anonymous", "sUserName": "172.16.0.254", "iUpload": "266.27KB/s"}, {"iDownload": "266.27KB/s", "iGroupID": "Anonymous", "sUserName": "10.60.1.220", "iUpload": "0B/s"}, {"iDownload": "17.52KB/s", "iGroupID": "Anonymous", "sUserName": "172.16.5.12", "iUpload": "223.97KB/s"}, {"iDownload": "198.0KB/s", "iGroupID": "Anonymous", "sUserName": "172.16.6.117", "iUpload": "41.88KB/s"}, {"iDownload": "8.38KB/s", "iGroupID": "Anonymous", "sUserName": "172.16.4.137", "iUpload": "182.51KB/s"}, {"iDownload": "166.11KB/s", "iGroupID": "Anonymous", "sUserName": "172.16.2.33", "iUpload": "19.29KB/s"}, {"iDownload": "163.79KB/s", "iGroupID": "Anonymous", "sUserName": "172.16.4.75", "iUpload": "4.56KB/s"}, {"iDownload": "128.21KB/s", "iGroupID": "Anonymous", "sUserName": "172.16.4.21", "iUpload": "25.11KB/s"}, {"iDownload": "9.28KB/s", "iGroupID": "Anonymous", "sUserName": "172.16.2.167", "iUpload": "142.3KB/s"}, {"iDownload": "133.83KB/s", "iGroupID": "Anonymous", "sUserName": "172.16.2.49", "iUpload": "4.77KB/s"}, {"iDownload": "5.9KB/s", "iGroupID": "Anonymous", "sUserName": "172.16.6.154", "iUpload": "126.74KB/s"}, {"iDownload": "108.21KB/s", "iGroupID": "Anonymous", "sUserName": "172.16.4.38", "iUpload": "16.8KB/s"}]}

import json

# file = open('alert_data.json', 'r')
#
# f = file.read()
#
# data = json.loads(f)
# print type(data)

with open("writein_json.json", "w") as json_file:
    json.dump(dic, json_file)
