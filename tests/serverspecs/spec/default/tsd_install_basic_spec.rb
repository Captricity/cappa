require 'spec_helper'

describe command('. /home/vagrant/venv/bin/activate; tsd query jquery --info') do
  let(:disable_sudo) { true }
  its(:stdout) { should contain("jQuery 1.10.x / 2.0.x") }
end
