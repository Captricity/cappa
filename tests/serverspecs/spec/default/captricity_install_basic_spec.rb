require 'spec_helper'

describe command('captricity show pip') do
  its(:stdout) { should contain("'name': ") }
end
