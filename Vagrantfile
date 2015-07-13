# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "captricity/cappatest"
  config.ssh.private_key_path = "~/.ssh/id_rsa"
  config.ssh.forward_agent = true
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
  end
end
