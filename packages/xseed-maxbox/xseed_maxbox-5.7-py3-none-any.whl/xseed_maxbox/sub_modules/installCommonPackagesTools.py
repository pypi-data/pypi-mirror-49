#Common packages installation

import os
import subprocess as sp

def install(x,y,z):
    sudo_password = z
    try:
        null = open("log.txt", "a")
        os.system('%s' % y)
        null.close()

    except OSError:
        print (e.message)
        print ("Exiting the process because of above error")
        exit();

def installCommonPackagesTools(password):
    # common packages
    packages = {
        "ecryptfs-utils": "sudo apt install ecryptfs-utils -y",
        "mscorefonts": "echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | sudo debconf-set-selections && sudo apt-get install ttf-mscorefonts-installer -y",
        "curl": "sudo apt install curl -y",
        "vim": "sudo apt install vim -y",
        "git": "sudo apt install git -y",
        "pv": "sudo apt-get install pv -y",
        "ssh": "sudo apt install ssh -y",
        "imagemagick": "sudo apt install imagemagick libcairo2-dev libjpeg-dev libpango1.0-dev libgif-dev build-essential g++ -y",
        "ubuntu-restricted-extras": "sudo apt-get install ubuntu-restricted-extras -y",
        "nginx": "sudo apt-get install nginx -y",
        "nodejs": "sudo apt-get install nodejs -y",
        "net-tools": "sudo apt-get install net-tools -y",
        "mongodb-clients":"sudo apt install mongodb-clients -y"
        }

    # common tools
    tools = {
        "google-chrome-stable" : "wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && sudo dpkg -i google-chrome-stable_current_amd64.deb && sudo apt -f install -y",
        "docker-ce" : "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - &&  sudo add-apt-repository \"deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable\" && sudo apt-get update &&  apt-cache policy docker-ce && sudo apt-get install -y docker-ce &&sudo curl -L \"https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m)\"  -o /usr/local/bin/docker-compose && sudo mv /usr/local/bin/docker-compose /usr/bin/docker-compose && sudo chmod +x /usr/bin/docker-compose",
        #"teamviewer" : "wget https://download.teamviewer.com/download/teamviewer_i386.deb && sudo dpkg -i teamviewer_i386.deb && sudo apt -f install -y",
        #"robomongo" : "wget https://download.robomongo.org/0.9.0/linux/robomongo-0.9.0-linux-x86_64-0786489.tar.gz && tar -xvzf robomongo-0.9.0-linux-x86_64-0786489.tar.gz && sudo mkdir /usr/local/bin/robomongo && sudo mv  robomongo-0.9.0-linux-x86_64-0786489/* /usr/local/bin/robomongo && cd /usr/local/bin/robomongo/bin && sudo chmod +x robomongo && cd ~/Downloads/",
        "graphql-ide" : "git clone https://github.com/andev-software/graphql-ide.git && cd graphql-ide/ && npm install -g electron && npm install && npm run package --all && cd ..",
        "zerotier-one" : "sudo curl -s https://raw.githubusercontent.com/zerotier/download.zerotier.com/master/htdocs/contact%40zerotier.com.gpg |gpg --import &&  if z=$(curl -s https://install.zerotier.com/ | gpg); then echo \"$z\" | sudo bash; fi"
        }

    command = 'apt-get update -y'
    os.system('echo %s|sudo -S %s' % (password, command))
    for x, y in packages.items():
        install(x,y,password)

    for x,y in tools.items():
       command1 = 'dpkg -s'
       package = sp.getoutput('%s %s| grep Status' %(command1,x))
       print("package = %s\n x = %s" %(package, x))
       if (package == "Status: install ok installed"):
           print('%s already found' % x)
       else:
           install(x,y,password)
