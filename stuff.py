import re

def logs():
    with open("logdata.txt", "r") as file:
        logdata = file.read()
        logs_list = re.split("\n", logdata)
        ans = []
        for log in logs_list:
            items = re.finditer("(?P<host>^[\d.]+) - (?P<user_name>[\w\d-]+) \[(?P<time>[\w\d\/: -]+)\] \"(?P<request>[\w \/\d.\+-]+)", log)
            for item in items:
                ans.append(item.groupdict())
    return ans

if __name__ == '__main__':
    print(len(logs()) == 979)
    
    one_item={'host': '146.204.224.152',
    'user_name': 'feest6811',
    'time': '21/Jun/2019:15:45:24 -0700',
    'request': 'POST /incentivize HTTP/1.1'}
    print(one_item in logs())