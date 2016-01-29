require 'spec_helper'

describe file('/home/vagrant/internal_api_clients') do
  it { should be_directory }
end
