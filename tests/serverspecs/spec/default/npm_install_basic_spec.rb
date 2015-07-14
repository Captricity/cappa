require 'spec_helper'

describe command('. /home/vagrant/venv/bin/activate; npm show underscore') do
  let(:disable_sudo) { true }
  its(:stdout) { should contain("name: 'underscore'") }
  its(:stdout) { should contain("'dist-tags': { latest: '1.8.3', stable: '1.8.3' }") }
end
