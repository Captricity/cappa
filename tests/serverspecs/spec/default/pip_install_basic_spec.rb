require 'spec_helper'

describe command('. /home/vagrant/venv/bin/activate; pip show django-extensions') do
  let(:disable_sudo) { true }
  its(:stdout) { should contain('Version: 1.5.5') }
end
