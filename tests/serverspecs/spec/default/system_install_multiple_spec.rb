require 'spec_helper'

describe package('postgresql-client') do
  it { should be_installed }
end

describe package('libpq-dev') do
  it { should be_installed }
end
