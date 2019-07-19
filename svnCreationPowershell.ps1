# Create SVN Repository

# change to svn repository directory
cd E:\Repositories
$repoPath = Get-Location

Write-Host "Directory is change to $(Get-Location)"

Write-Host

# Ask user to input new repository name
$newSVN = Read-Host "Please enter name of new SVN"
$pattern = "^[a-zA-Z0-9_-]*$"

# Test-Path $repoPath"\$newSVN"

if (Test-Path $repoPath"\$newSVN")
    {
        Write-Host "SVN with name $newSVN already exists in $repoPath directory, Shutting down script!!!"
        sleep 1
        break
    }

if ($newSVN -match $pattern)
    {
        Write-Host "Please wait!!!"
        sleep 2
        $choice = Read-Host "Do you really want to create $newSVN SVN, enter Y or N?"
        if ($choice -eq 'n'.ToLower())
        {
            Write-Host "Exiting Script"
            break
        }
        elseif ($choice -eq 'y'.ToLower())
        {
            Write-Host "Creating SVN"
            sleep 1

        }
        else
        {
            break
        }

    }

# change directory to svn acl
sleep 1
cd E:\svn_repository_acls
Write-Host "Directory changed to $(Get-Location) "

Write-Verbose -Message "Creating access file" -Verbose
sleep 1
$svnACl = $newSVN + '-acl.conf'

# Create file and add content to file
Add-Content $svnACl -Value "[$newSVN`:/]`n@allusers = rw`n@admin = rw`n`n`n[groups]`nadmin = sujitn`nallusers = rajendram,prathameshs,sumitw"

# change directory to httpd conf
cd "C:\Program Files (x86)\Apache Software Foundation\Apache2.2\conf"
Write-Verbose "Appending httpd.conf" -Verbose
sleep 1
Add-Content .\httpd.conf -Value "`n<Location /$newSVN>`n  DAV svn`n  SVNPath 'd:\\repositories\\$newSVN'`n  AuthzSVNAccessFile d:\svn_repository_acls\\$newSVN-acl.conf`n  AuthType Basic`n  AuthBasicProvider ldap`n  AuthzLDAPAuthoritative on`n  AuthName 'Subversion Repository'`n  AuthLDAPBindPassword com@svn`n  AuthLDAPURL 'ldap://172.19.10.10:3268/dc=company,dc=com?sAMAccountName?sub?(objectClass=*)'`n  Require valid-user`n</Location>"

Write-Host "$newSVN SVN is created." -ForegroundColor Green

# Restart apache service
Write-Host "Restarting apache please wait!!!!!" -ForegroundColor DarkYellow
sleep 2
cd ..\bin
.\httpd.exe -l restart
