require 'spec_helper'

describe command('pip show Django') do
  let(:disable_sudo) { true }
  its(:stdout) { should eq '' }
end

describe command('pip3 show Django') do
  let(:disable_sudo) { true }
  its(:stdout) { should contain('Version: 1.8.5') }
end
