import sys
def main(fileName):
    oldfile=open(fileName,'r')
    index=fileName.find('.')
    fileName=fileName[:index]+'C.vm'
    newfile=open(fileName,'w')
    print("Processing")
    while True:
        line=oldfile.readline()
        if line=='':
            break
        for pos,char in enumerate(line):
            if char=='/':
                if pos==1:
                    line=''
                else:
                    line=line[:pos]
        if not line=='':
            newfile.write(line+'\n')

    oldfile.close()
    newfile.close()
    print("Comments Removed")

if __name__=="__main__":
    fileName=sys.argv[-1]
    main(fileName)
