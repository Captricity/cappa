require 'spec_helper'

describe command('bower info jquery') do
  let(:disable_sudo) { true }
  its(:stdout) { should contain("version: '2.1.4'") }
end
