require 'spec_helper'

describe command('npm list underscore') do
  its(:stdout) { should contain("underscore@1.8.2") }
end
