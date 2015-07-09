require 'spec_helper'

describe package('postgresql-client') do
  it { should be_installed.with_version('1.0.0') }
end

describe package('libpq-dev') do
  it { should be_installed }
end

describe package('some-package') do
  it { should be_installed }
end