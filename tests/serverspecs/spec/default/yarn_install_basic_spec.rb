require 'spec_helper'

describe command('yarn info underscore') do
  its(:stdout) { should contain("'underscore'") }
  its(:stdout) { should contain("1.8.3") }
end
