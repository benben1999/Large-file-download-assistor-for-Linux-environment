import os
import sys

size_of_chunck = 200000000

if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print("Usage: %s [url] [file size]" % sys.argv[0])
    url, file_size = sys.argv[1], sys.argv[2]
    if file_size.endswith('GB'):
        num = int(file_size.split('GB')[0])
        file_size = num * 1024 * 1024 * 1024
    elif file_size.endswith('MB'):
        num = int(file_size.split('MB')[0])
        file_size = num * 1024 * 1024
    elif file_size.endswith('KB'):
        num = int(file_size.split('MB')[0])
        file_size = num * 1024
    else:
        num = int(file_size)
        file_size = num
    xs = []
    i = 0
    while file_size > size_of_chunck:
        xs.append((str(i*size_of_chunck),
                   str((i+1)*size_of_chunck - 1),
                   '.temp___%010d' % i, url))
        file_size -= size_of_chunck
        i += 1
    xs.append((str(i*size_of_chunck), '', '.temp___%010d' % i, url))

    for x in xs:
        cmd = "curl --retry 4 -C - --range %s-%s -o %s %s" % x
        print("#", cmd)
        os.system(cmd)
    files = [x[2] for x in xs]
    filename = url.split('/')[-1]
    cmd = "cat %s > %s" % (' '.join(files), filename)
    print(cmd)
    os.system(cmd)
