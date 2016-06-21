require 'spec_helper'

describe command('typings info listify') do
  its(:stdout) { should contain("name        listify") }
end
