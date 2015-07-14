require 'spec_helper'

describe command('bower info bootstrap') do
  let(:disable_sudo) { true }
  its(:stdout) { should contain("version: '3.3.5'") }
end
