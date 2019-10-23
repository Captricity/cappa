require 'spec_helper'

describe command('jshint -v') do
  its(:stderr) { should contain("v2.8.0") }
end
