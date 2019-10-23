require 'spec_helper'

describe command('tsd query jquery:JQuery --info') do
  its(:stdout) { should contain("jquery:JQuery") }
end
describe file('/cappa-master/tests/serverspecs/typings/jquery') do
  it { should be_directory }
end