require 'spec_helper'

describe command('tsd query jquery --info') do
  its(:stdout) { should contain("jQuery 1.10.x / 2.0.x") }
end
