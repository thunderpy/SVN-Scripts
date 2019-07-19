import os, re
from time import sleep

# change to svn repository directory
os.chdir(r'D:\repositories')
print("Directory is change to " + os.getcwd())

# Ask user to input new repository name
newSVN = input("Please enter name of new SVN: ")

if os.path.exists(newSVN):
    print("SVN with name {} already exists in {} directory, Shutting script down!!!.".format(newSVN, os.getcwd()))
    exit()
if re.findall("^[a-zA-Z0-9_-]*$", newSVN):
    print("Please wait!!!!")
    sleep(2)
    choice = input("Do you really want to create {}, enter {} or {}? ".format(newSVN, 'Y', 'N')).lower()
    if choice == 'n':
        quit()
    else:
        os.system('svnadmin create ' + newSVN)
        sleep(2)
else:
    print("Please enter a valid SVN name eg:- P100241_IKEA_35_Language ")
    exit()

# change directory to svn acl
print()
os.chdir(r'D:\svn_repository_acls')
print("Directory now changed to " + os.getcwd())
print("Creating access file")
sleep(2)

# now create a conf file
svnACl = newSVN + '-acl.conf'
file = open(svnACl,'w')
text_in_file = ['[', newSVN, ':/]', '\n', '@allusers = rw', '\n', '@admin = rw', '\n'*4, '[groups]', '\n', 'admin = sujitn', '\n', 'allusers = rajendram,prathameshs,sumitw,vickym']
file.writelines(text_in_file)
file.close()

# change directory to httpd conf
os.chdir(r'C:\Program Files (x86)\Apache Software Foundation\Apache2.2\conf')
print()
print("Appending httpd.conf")
sleep(1)

text_to_append = """\n
<Location /P100241_IKEA_35_Language>
  DAV svn
  SVNPath "d:\\repositories\\P100241_IKEA_35_Language
  AuthzSVNAccessFile d:\svn_repository_acls\\P100241_IKEA_35_Language-acl.conf
  AuthType Basic
  AuthBasicProvider ldap
  AuthzLDAPAuthoritative on
  AuthName "Subversion Repository"
  AuthLDAPBindDN "SVN-Admin@mitrmum.com"
  AuthLDAPBindPassword mitr@svn
  AuthLDAPURL "ldap://172.19.10.10:3268/dc=mitrmum,dc=com?sAMAccountName?sub?(objectClass=*)"
  Require valid-user
</Location>""".replace('P100241_IKEA_35_Language',newSVN)

with open("httpd.conf", 'a') as myfile:
    myfile.write(text_to_append)

print('=' * 50)
print(newSVN + " repository is created.")
print('=' * 50)

# Restart apache service
print("Restarting apache please wait!!!!!")
sleep(2)
os.chdir(r'C:\Program Files (x86)\Apache Software Foundation\Apache2.2\bin')
cmd = os.system('httpd.exe -k restart')
if cmd == 0:
    print('Apache restart successfully')
else:
    print('Something went wrong please check manually')
