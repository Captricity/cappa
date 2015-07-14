require 'spec_helper'

describe command('. /home/vagrant/venv/bin/activate; pip show internal-api-clients') do
  let(:disable_sudo) { true }
  its(:stdout) { should contain("Version: 0.0.3") }
end
