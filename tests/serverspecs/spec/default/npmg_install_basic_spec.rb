require 'spec_helper'

describe command('npm show jshint') do
  its(:stdout) { should contain("version: '2.8.0'") }
end