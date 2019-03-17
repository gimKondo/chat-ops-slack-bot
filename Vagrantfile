# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-18.04"
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
  end

  config.vm.provision "shell", inline: <<-SHELL
    echo "*************** start setup general package *******************"
    apt update
    apt install -y tree git tmux tig lynx zip
    echo "*************** complete setup general package *******************"
    echo ""

    echo "*************** start setup aws cli *******************"
    curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
    python get-pip.py
    rm -f get-pip.py
    pip install awscli
    echo "*************** complete setup aws cli *******************"
    echo ""
  SHELL
end
