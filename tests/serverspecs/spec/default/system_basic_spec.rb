require 'spec_helper'

describe command('cappa version') do
    its(:stdout) { should match /0.8.3/ }
end
