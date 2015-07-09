require 'spec_helper'

describe command('npmg show gulp') do
  its(:stdout) { should contain('Version: 3.8.7') }
end
