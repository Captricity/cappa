require 'spec_helper'

describe command('pip show Django') do
  let(:disable_sudo) { true }
  its(:stdout) { should contain('Version: 1.8.5') }
  its(:stdout) { should contain('pypy') }
end
