# Large-file-download-assistor-for-Linux-environment
1. Introduction

Wget is not suitable for downloading large files, and this script solves this problem

2. Problem description

Download large files (more than 10g) from remote server, there will be sudden interruption in the middle of the phenomenon, sometimes need to re-download from scratch, inefficient.If the file is extremely large (20 gigabytes or more), it is extremely difficult to download, and it is almost impossible to download successfully

3. Problem analysis

case1:

https://forums.wsusoffline.net/viewtopic.php?f=9&t=7069#

case2:

remote server does not support wget -c instruction

4. Instruction

(1) Download the python file "download.py"
(2) python download.py [download link] [file size] 
(3) for example, python download.py https://baidu.com/index.html 200MB  (if filed, you need install the "curl" toolkit)
