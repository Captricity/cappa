require 'spec_helper'

describe command('npmg show bower') do
  its(:stdout) { should contain('Version: 1.4.1') }
end

describe command('npmg show gulp') do
  its(:stdout) { should contain('Version: 3.8.7') }
end