#this script has the following dependencies: Windows, 7zip, and Python 3.10
#both 7zip and Python must have their path listed in windows environment variables
import os
import time
import subprocess
import pathlib
#input subdir, file, array where subdir is the path from root, file is the file name, and array is an array of integers 
#compresstest() runs the given file through 4 compression algorithms LZMA2, Deflate, PPMd, and windows' native compression
#each algorithm creates and stores its own version of the file and stores it in its respective compressed format
#The files size will be recorded and the files deleted
#return: array of integers 
def compresstest(subdir,file,array):
    t= ';' 
    FilePath = os.path.join(subdir, file)       #create full file path for reference
    OGFileSize= os.path.getsize(FilePath)       #obtain original file size to reference for compression ratio
#####################################################################################################
#begin mx test
    array[0] += int(OGFileSize/1000)            #add file size to data set to be returned as output
    if(OGFileSize==0):                          #scrub cases where the file is a stub
        return
    RealTime = time.time()                      #Take start time for Data collection
    MXnamestart=file+'mx9test.7z'               #setup file name for mx9 test
    MXname = os.path.join(subdir,MXnamestart)   #Create a file disignation for mx9 compressed file
    cmd = ['7z', 'a', MXname , FilePath, '-mx9']
    subprocess.run(cmd)                         #Run mx9 command
    CompMethod = '7zip: LZMA2 '
    EndRealTime = time.time()                   #End Timer 
    ENDFileSize = os.path.getsize(MXname)       #get new file size (in bytes)
    MXS= ENDFileSize 
    MXdata = str(CompMethod) + t + str(OGFileSize) +t +str(ENDFileSize)+ t+ str(ENDFileSize/OGFileSize)+ t+ (pathlib.Path(file).suffix) +t +str(EndRealTime - RealTime)#compile data collected to be written to a file
    array[1] += int(ENDFileSize/1000)           #add file size to data set to be returned as output
#end mx test 
######################################################################################################
#begin deflate test
    FilePath = os.path.join(subdir, file)
    RealTime = time.time()                      #Take start time for Data collection
    Deflatenamestart=file+'Deflatetest.7z'      #setup file name for deflate test
    Deflatename = os.path.join(subdir,Deflatenamestart)
    cmd = ['7z', 'a', Deflatename , FilePath, '-m1=deflate']
    subprocess.run(cmd)                         #Run Deflate command
    CompMethod = '7zip: Deflate '
    EndRealTime = time.time()                   #End Timer
    ENDFileSize = os.path.getsize(Deflatename)  #get new file size (in bytes)
    DeflateS = ENDFileSize
    Deflatedata = str(CompMethod) + t + str(OGFileSize) +t +str(ENDFileSize)+ t+ str(ENDFileSize/OGFileSize)+ t+ (pathlib.Path(file).suffix) +t +str(EndRealTime - RealTime)#compile data collected to be written to a file
    array[2] += int(ENDFileSize/1000)           #add file size to data set to be returned as output
#end deflate test (DeflateS)
######################################################################################################
#begin Windows compress-archive test
    W=0
    FilePath = os.path.join(subdir, file)
    RealTime = time.time()                       #Take start time for Data collection
    Winfile = '\"' +os.path.join(subdir,file)+'"'#setup file name for win test
    Winname = FilePath+ 'wint.zip'
    pwrname = '\"' + Winname +'\"'
    cmd = ['powershell', 'compress-archive', Winfile ,  pwrname ]
    subprocess.run(cmd)                          #Powershell compress-archive -Path String -DestinationPath String
    Winname = os.path.join(subdir, Winname)
    CompMethod = 'Windows Compress '
    EndRealTime = time.time()                    #End Timer 
    if os.path.isfile(Winname):                  #windows compress archive fails when used through powershell on large files. This is for error catching.
        ENDFileSize = os.path.getsize(Winname)   #get new file size (in bytes)
        W=1
        WinS = ENDFileSize
        array[3] += int(WinS/1000)               #add file size to data set to be returned as output
        Windata = str(CompMethod) + t + str(OGFileSize) +t +str(ENDFileSize)+ t+ str(ENDFileSize/OGFileSize)+ t+ (pathlib.Path(file).suffix) +t +str(EndRealTime - RealTime)#compile data collected to be written to a file
    else:
        Windata = str(CompMethod) + t + 'FAILURE'#record errors
#end Windows compress-archive test
######################################################################################################
#begin PPMd 
    FilePath = os.path.join(subdir, file)
    RealTime = time.time()                          #Take start time for Data collection
    PPMdnamestart=file+'PPMdtest.7z'                #setup file name for PPMd test
    PPMdname = os.path.join(subdir,PPMdnamestart)
    cmd = ['7z', 'a', PPMdname , FilePath, '-m1=PPMd']
    subprocess.run(cmd)                             #Run Deflate command
    CompMethod = '7zip: PPMd '
    EndRealTime = time.time()                       #End Timer 
    ENDFileSize = os.path.getsize(PPMdname)      #get new file size (in bytes)
    PPMdS = ENDFileSize
    PPMddata = str(CompMethod) + t + str(OGFileSize) +t +str(ENDFileSize)+ t+ str(ENDFileSize/OGFileSize)+ t+ (pathlib.Path(file).suffix) +t +str(EndRealTime - RealTime)#compile data collected to be written to a file
    array[4] += int(ENDFileSize/1000)               #add file size to data set to be returned as output
#End PPMd
######################################################################################################
#Record which file had the best compression ratio:
    if(W==1):
        if(MXS <= DeflateS and MXS <=WinS and MXS<=PPMdS):
            array[5] +=int(MXS/1000)
        elif(DeflateS <=MXS and DeflateS <=WinS and DeflateS<= PPMdS):
            array[5] += int(DeflateS/1000)
        elif(WinS<=MXS and WinS <=DeflateS and WinS <=PPMdS):
            array[5] +=int(WinS/1000)
        else:
            array[5] += int(PPMdS/1000)
    elif(W==0):
        if(MXS<=DeflateS and MXS<=PPMdS):
            array[5] +=int(MXS/1000)
        elif(DeflateS<=MXS and DeflateS<= PPMdS):
            array[5] +=int(DeflateS/1000)
        else:
            array[5] += int(PPMdS/1000)
#end record
######################################################################################################            
#clear compressed versions of files
    os.remove(MXname)
    os.remove(Deflatename)
    if os.path.isfile(Winname):
        os.remove(Winname)
    os.remove(PPMdname)
#compressed files removed
######################################################################################################
#write results to data file
    f= open('C:\Capstonedata\data.txt', 'a')
    f.write('\n')
    f.write(MXdata)
    f.write('\n')
    f.write(Deflatedata)
    f.write('\n')
    f.write(Windata)
    f.write('\n')
    f.write(PPMddata)
    f.close()
#Write complete
    return(array) #end of compressiontest function

#input subdir, file where subdir is the path from root, file is the file name
#compress() runs the given file through 4 compression algorithms LZMA2, Deflate, PPMd, and windows' native compression
#each algorithm creates and stores its own version of the file and stores it in its respective compressed format
#The files size will be recorded and the all but the smallest file will be deleted
#return: 
def compress(subdir,file):
    t= ';' 
    FilePath = os.path.join(subdir, file)       #create full file path for reference
    OGFileSize= os.path.getsize(FilePath)       #obtain original file size to reference for compression ratio
#####################################################################################################
#begin mx test
    if(OGFileSize==0):                          #scrub cases where the file is a stub
        return
    RealTime = time.time()                      #Take start time for Data collection
    MXnamestart=file+'mx9test.7z'               #setup file name for mx9 test
    MXname = os.path.join(subdir,MXnamestart)   #Create a file disignation for mx9 compressed file
    cmd = ['7z', 'a', MXname , FilePath, '-mx9']
    subprocess.run(cmd)                         #Run mx9 command
    CompMethod = '7zip: LZMA2 '
    EndRealTime = time.time()                   #End Timer 
    ENDFileSize = os.path.getsize(MXname)       #get new file size (in bytes)
    MXS= ENDFileSize 
    MXdata = str(CompMethod) + t + str(OGFileSize) +t +str(ENDFileSize)+ t+ str(ENDFileSize/OGFileSize)+ t+ (pathlib.Path(file).suffix) +t +str(EndRealTime - RealTime)#compile data collected to be written to a file
#end mx test 
######################################################################################################
#begin deflate test
    FilePath = os.path.join(subdir, file)
    RealTime = time.time()                      #Take start time for Data collection
    Deflatenamestart=file+'Deflatetest.7z'      #setup file name for deflate test
    Deflatename = os.path.join(subdir,Deflatenamestart)
    cmd = ['7z', 'a', Deflatename , FilePath, '-m1=deflate']
    subprocess.run(cmd)                         #Run Deflate command
    CompMethod = '7zip: Deflate '
    EndRealTime = time.time()                   #End Timer
    ENDFileSize = os.path.getsize(Deflatename)  #get new file size (in bytes)
    DeflateS = ENDFileSize
    Deflatedata = str(CompMethod) + t + str(OGFileSize) +t +str(ENDFileSize)+ t+ str(ENDFileSize/OGFileSize)+ t+ (pathlib.Path(file).suffix) +t +str(EndRealTime - RealTime)#compile data collected to be written to a file
#end deflate test (DeflateS)
######################################################################################################
#begin Windows compress-archive test
    W=0
    FilePath = os.path.join(subdir, file)
    RealTime = time.time()                       #Take start time for Data collection
    Winfile = '\"' +os.path.join(subdir,file)+'"'#setup file name for win test
    Winname = FilePath+ 'wint.zip'
    pwrname = '\"' + Winname +'\"'
    cmd = ['powershell', 'compress-archive', Winfile ,  pwrname ]
    subprocess.run(cmd)                          #Powershell compress-archive -Path String -DestinationPath String
    Winname = os.path.join(subdir, Winname)
    CompMethod = 'Windows Compress '
    EndRealTime = time.time()                    #End Timer 
    if os.path.isfile(Winname):                  #windows compress archive fails when used through powershell on large files. This is for error catching.
        ENDFileSize = os.path.getsize(Winname)   #get new file size (in bytes)
        W=1
        WinS = ENDFileSize
        Windata = str(CompMethod) + t + str(OGFileSize) +t +str(ENDFileSize)+ t+ str(ENDFileSize/OGFileSize)+ t+ (pathlib.Path(file).suffix) +t +str(EndRealTime - RealTime)#compile data collected to be written to a file
    else:
        Windata = str(CompMethod) + t + 'FAILURE'#record errors
#end Windows compress-archive test
######################################################################################################
#begin PPMd 
    FilePath = os.path.join(subdir, file)
    RealTime = time.time()                          #Take start time for Data collection
    PPMdnamestart=file+'PPMdtest.7z'                #setup file name for PPMd test
    PPMdname = os.path.join(subdir,PPMdnamestart)
    cmd = ['7z', 'a', PPMdname , FilePath, '-m1=PPMd']
    subprocess.run(cmd)                             #Run Deflate command
    CompMethod = '7zip: PPMd '
    EndRealTime = time.time()                       #End Timer 
    ENDFileSize = os.path.getsize(PPMdname)      #get new file size (in bytes)
    PPMdS = ENDFileSize
    PPMddata = str(CompMethod) + t + str(OGFileSize) +t +str(ENDFileSize)+ t+ str(ENDFileSize/OGFileSize)+ t+ (pathlib.Path(file).suffix) +t +str(EndRealTime - RealTime)#compile data collected to be written to a file
#End PPMd
######################################################################################################
#Record which file had the best compression ratio and delete other files:
    if(W==1):
        if(MXS <= DeflateS and MXS <=WinS and (MXS<=OGFileSize or os.path.isdir(FilePath)) and MXS <=PPMdS):
            os.remove(Deflatename)
            os.remove(Winname)
            os.remove(PPMdname)
        elif(DeflateS <=MXS and DeflateS <=WinS and (DeflateS<=OGFileSize or os.path.isdir(FilePath)) and DeflateS <=PPMdS):
            os.remove(MXname)
            os.remove(Winname)
            os.remove(PPMdname)
        elif(WinS<=MXS and WinS <=DeflateS and (WinS<=OGFileSize or os.path.isdir(FilePath)) and WinS <=PPMdS):
            os.remove(MXname)
            os.remove(Deflatename)
            os.remove(PPMdname)
        elif(PPMdS<=MXS and PPMdS<=DeflateS and PPMdS <= WinS and (PPMdS <=OGFileSize or os.path.isdir(FilePath))):
            os.remove(MXname)
            os.remove(Deflatename)
            os.remove(Winname)
        else:
            os.remove(MXname)
            os.remove(Deflatename)
            os.remove(Winname)
            os.remove(PPMdname)
    elif(W==0):
        if(MXS<=DeflateS and MXS<=PPMdS and (MXS<=OGFileSize or os.path.isdir(FilePath))):
            os.remove(Deflatename)
            os.remove(PPMdname)
        elif(DeflateS<=MXS and DeflateS<=PPMdS and (DeflateS <=OGFileSize or os.path.isdir(FilePath))):
            os.remove(MXname)
            os.remove(PPMdname)
        elif(PPMdS<=MXS and PPMdS <= DeflateS and (PPMdS <=OGFileSize or os.path.isdir(FilePath))):
            os.remove(MXname)
            os.remove(Deflatename)
        else:
            os.remove(MXname)
            os.remove(Deflatename)
            os.remove(PPMdname)

#end cleanup
######################################################################################################
#write results to data file
    f= open('C:\Capstonedata\data.txt', 'a')
    f.write('\n')
    f.write(MXdata)
    f.write('\n')
    f.write(Deflatedata)
    f.write('\n')
    f.write(Windata)
    f.write('\n')
    f.write(PPMddata)
    f.close()
#Write complete
    return() #end of compression function   

dir_list = os.listdir()# Get the list of all files and directories in the root directory
rootdir = os.getcwd()
#setup data file
t= ';'
f= open('C:\Capstonedata\data.txt', 'a')
f.write('\n')
f.write('CompMethod') 
f.write(t)
f.write('Original file size')
f.write(t)
f.write('compressed file size')
f.write(t)
f.write('compression ratio')
f.write(t)
f.write('File Type')
f.write(t)
f.write('real time')
f.close()
#create array to store[total data amount, total data compressed as LZMA2, total data as Deflate, total data as win, total data as PPM-whatever , and total data when taking the best result]
import array as arr
array = arr.array('l', [0, 0, 0, 0, 0, 0])
print('enter "T" for compression test, enter "C" to compress files')
Input= input()
if(Input == 'T'):                                        # Test all files in all subdirectory individually
    for subdir, dirs, files in os.walk(rootdir):     #Walkthrough entire current working directory
        for file in files:
            print(os.path.join(subdir, file))
            array = compresstest(subdir,file,array)
    f= open('C:\Capstonedata\data.txt', 'a')
    string = '\n' + 'Total bytes tested: '+ str(array[0]) +'000'+ t + 'Total after LZMA2 compression: ' + str(array[1]) +'000'+ t +'Total after Deflate compression: ' + str(array[2])+'000' + t + 'Total after windows compression: '+ str(array[3]) +'000' +t + 'Total after PPMd compresswion: ' + str(array[4])+ t + 'Total bytes with best compression selected: ' + str(array[5])+'000'
    f.write(string)                                     #record data from 'array' to the data.txt file
    f.close()
elif(Input =='C'):                                      #Practical application of the program
    print('Enter "S" to compress all contained files individually, enter "F" to compress only files and folders in the current directory')
    Input= input()                                      #user decides if they will do all files in all subdirectorie, or only files and folders in the current working directory 
    if(Input =='S'):
        for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                print(os.path.join(subdir, file))
                compress(subdir,file)
    elif(Input == 'F'):
        for files in os.listdir(rootdir):
            print(files)
            compress(rootdir,files)
    else:
        print('invalid input. Script ending')  
    f.close()
else:
    print('invalid input. Script ending')   