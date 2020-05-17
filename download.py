#!/usr/bin/env python3
'''
## Requirement
- Linux
- curl
- Python3
## Usage
```
chmod +x download.py
./download.py <url> [option] 
./download.py --help
```
Example: `./download.py https://www.baidu.com/index.html`
'''
#!/usr/bin/env python3
import os
import sys

SIZE_OF_CHUNCK = 1024 * 1024 * 200  # 200MB
TRY_NUMS = 5
# curl option
CURL_TIME_OUT = 60*2  # 120 seconds
CURL_RETRIES = 2
CURL = 'LD_LIBRARY_PATH=/usr/local/lib curl --connect-timeout 5'
# CURL = 'curl --connect-timeout 5'

# set by option
slient_mode = False


def download_part(url: str, filename: str, start, end='') -> int:
    flags = ''
    if slient_mode:
        flags += ' -s '
    cmd = '%s %s -m %s --retry %s --range %s-%s -o %s %s' % (
        CURL, flags, CURL_TIME_OUT, CURL_RETRIES, start, end, filename, url)
    # print("\n# {}".format(cmd))
    return os.system(cmd) == 0


def get_file_size_curl(url: str) -> int:
    cmd = "%s -sI %s | grep -i Content-Length | awk '{print $2}'" % (CURL, url)
    try:
        f = os.popen(cmd)
        lines = f.readlines()
        size = lines[0].strip()
        f.close()
        print('file size: %s byte' % size)
        return int(size)
    except (Exception, IndexError):
        print('Error: failed to get size of file')
        exit(0)


def exists(filename: str):
    if os.path.exists(filename):
        if os.stat(filename).st_size == SIZE_OF_CHUNCK:
            return True
    return False


def download(url, file_size):
    filename = url.split('/')[-1]

    num_chuncks = (file_size+SIZE_OF_CHUNCK-1)//SIZE_OF_CHUNCK
    parts = []
    succs = []
    for i in range(num_chuncks):
        part_name = '.part%d%s' % (i, filename)
        parts.append(part_name)
        start, end = i*SIZE_OF_CHUNCK, (i+1)*SIZE_OF_CHUNCK-1
        print("%d/%d %s..." % (i+1, num_chuncks, part_name))
        if exists(part_name) or download_part(url, part_name, start, end):
            succs.append(part_name)
        elif os.path.exists(part_name):
            os.remove(part_name)

    if parts == succs:
        cmd = "cat %s > %s" % (' '.join(parts), filename)
        if not slient_mode:
            print(cmd)
        if os.system(cmd) == 0:
            for f in parts:
                os.remove(f)
        return True
    else:
        print("failed to download:")
        for f in parts:
            if f not in succs:
                print(f)
    return False


if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] in ('--help', '-h', '-?'):
        print("Usage: %s <url> [option]" % sys.argv[0])
        print("Example: python3 %s https://www.baidu.com/index.html" %
              sys.argv[0])
        print("Options:")
        print("    -s   slient mode")
        exit(0)
    if '-s' in sys.argv[2:]:
        slient_mode = True

    url = sys.argv[1]
    file_size = get_file_size_curl(url)
    for _ in range(TRY_NUMS):
        if download(url, file_size):
            break
    else:
        print('Error: failed to download the file')
