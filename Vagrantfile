Vagrant.configure("2") do |config|

    config.vm.provider "virtualbox" do |v|
        v.memory = 4096
        v.cpus = 2
    end
      
    config.vm.define "iobox" do |iobox|
        iobox.vm.box = "ubuntu/bionic64"
        iobox.vm.hostname = "iobox"
        iobox.vm.provision "ansible" do |ansible|
            ansible.playbook = "ansible-setup.yaml"
        end
    end
end