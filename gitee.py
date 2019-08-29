import urllib2, lxml.html, sys, os, commands

header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36'}
homepage = False
no_file_link_list = []

def getDirAndFileList(url):
    global homepage
    global no_file_link_list
    req = urllib2.Request(url=url, headers=header)
    dirList = []
    fileList = []
    try:
        html = urllib2.urlopen(req, timeout=120).read()
        doc  = lxml.html.fromstring(html)
        # this means : gitee.com/user/project, gitee.com/user/project/tree/branch
        if len(url.split("//")[1].split('/')) == 3 or (len(url.split("//")[1].split('/')) == 5 and url.split("//")[1].split('/')[-2]=="tree" ):
            # print("homepage")
            homepage = True
        else:
            # print("Not homepage")
            homepage = False
        itemList = doc.xpath('//div[@id="tree-slider"]/div[@data-type]')
        for row in itemList:
            if 'folder' == row.xpath('div/@data-type')[0]:
                dirList.append( row.xpath('div/a/@title')[0])
            elif 'file' == row.xpath('div/@data-type')[0]:
                fileList.append(row.xpath('div/a/@title')[0])
        if len(fileList) == 0:
            # print("Please make sure that this link doesn't contain files: %s " % url)
            no_file_link_list.append(url)
            # f = open('%s.html'%url.split('/')[-1], 'w')
            # f.write(html)
            # f.close()
        return dirList, fileList
    except Exception, e:
        print("Exception has happened: "+e.message)

def downloadFile(dirPath, fileList, url):
    origin_work_dir = os.getcwd()
    # print("origin_work_dir: %s" % origin_work_dir)
    os.chdir(dirPath)
    for fileName in fileList:
        downloadUrl = url.replace('tree','raw')+'/'+fileName
        print("Downlading %s" % dirPath+'/'+fileName)
        commands.getstatusoutput('wget %s' % downloadUrl)
    os.chdir(origin_work_dir)

def createDir(dirPath, dirList):
    origin_work_dir = os.getcwd()
    os.chdir(dirPath)
    for dirItem in dirList:
        os.makedirs(dirItem)
    os.chdir(origin_work_dir)

def recursive(curDir, url):
    # print(url)
    subDirList, fileList = getDirAndFileList(url)
    urlSubDirList = subDirList
    branch = 'master'
    urlSplitList = url.split("//")[1].split('/')
    if len(urlSplitList) > 3 and urlSplitList[urlSplitList.index('tree')+1] != 'master':
        branch = urlSplitList[urlSplitList.index('tree')+1]
    if len(fileList) != 0:
        downloadFile(curDir, fileList, url)
    if homepage:
        urlSubDirList = [ 'tree/'+branch+'/'+subdir for subdir in subDirList]
    if len(subDirList) != 0:
        createDir(curDir, subDirList)
        for dirItem in urlSubDirList:
            recursive(curDir+'/'+dirItem.replace('tree/'+branch+'/', ''), url+'/'+dirItem)

def getSubDir(url, path):
    if len(path) != 0:
        if os.path.exists(path):
            os.chdir(path)
        else:
            print("Path doesn't exist. Create it for you first.")
            os.mkdir(path)
            os.chdir(path)
    curDir = url.split('/')[-1]
    if os.path.exists(curDir):
        print("%s exists, please change to another directory." % ( os.getcwd()+ '/' + curDir))
        exit(0)
    else:
        os.mkdir(curDir, 0755)
        # subDirList = []
        # rootDir = os.getcwd() + "/" + curDir
        recursive(curDir, url)
        if len(no_file_link_list) != 0:
            print("\nThese following links don't contain files, please confirm:")
            for url in no_file_link_list:
                print(url)
