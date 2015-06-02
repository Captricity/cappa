require 'spec_helper'

describe package('postgresql-client') do
  it { should be_installed }
end
