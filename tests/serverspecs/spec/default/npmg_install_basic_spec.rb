require 'spec_helper'

describe command('. /home/vagrant/venv/bin/activate; npm show jshint') do
  let(:disable_sudo) { true }
  its(:stdout) { should contain("version: '2.8.0'") }
end