import json
import sys

result={}                               #Dictionary to store data in required format

#function passwdoperation(passwdfile)
#input : /etc/passwd file
#output : Boolean value, true if successful execution else false
def passwdoperation(passwdfile):
    try:
        filep = open(passwdfile, "r")               #Handle case when /etc/passwd file cannot be opened
    except:
        print("Cannot open /etc/passwd file")
        return False
    for line in filep:
        if line[0] == '#':              #Handle comments in /etc/passwd file if any
            continue
        if line.find(':') == -1:                #Handle case when /etc/passwd file not in proper format
            print("ERROR : File not in proper format(Malformed file)")
            return False
        passwdarr=line.split(':')
        username=passwdarr[0]
        uid=passwdarr[2]
        fullname=passwdarr[4]
        temp={"uid":uid,"full_name":fullname,"groups":[]}
        result[username]=temp
    return True
        
#function groupoperation(groupfile)
#input : /etc/group file
#output : Boolean value, true if successful execution else false
def groupoperation(groupfile):
    try:
        fileg = open(groupfile, "r")                #Handle case when /etc/group file cannot be opened
    except:
        print("Cannot open /etc/group file")
        return False
    for line in fileg:
        if line[0] == '#':              #Handle comments in /etc/group file if any
            continue
        if line.find(':') == -1:                #Handle case when /etc/group file not in proper format
            print("ERROR : File not in proper format(Malformed file)")
            return False
        grouparr=line.split(':')
        gname=grouparr[0]
        uname=grouparr[3].split(',')
        uname[len(uname)-1]=uname[len(uname)-1].split('\n')[0]
        if len(uname)>=1 and uname[0]!='':
            for user in uname:
                result[user]["groups"].append(gname)
    return True
    
#function invoker(passwdfile,groupfile)
#input: /etc/passwd & /etc/etc/group files
#output : return json object after successful parsing of the above files
def invoker(passwdfile,groupfile):    
    successpasswd = passwdoperation(passwdfile)
    if successpasswd:
        successgroup = groupoperation(groupfile)            #Perform operation on group file only if successful on passwd file
    if successpasswd and successgroup:
        resultobj=json.dumps(result,indent=4)                #Create json object from dictionary created by parsing passwd & group files
        writefile = open("/etc/output.json",'w')          #File to write output
        writefile.truncate()                        #Clear the existing contents of file before writing to it
        json.dump(result,writefile,indent=4)            #Write the current parsing output to the output.json file
        #output.json will have existing users info and their groups after the current run in a cron job
        return(resultobj)

if __name__ == "__main__":
    outputobj = invoker(sys.argv[1],sys.argv[2])
    print(outputobj)                #print JSON object created
