require 'spec_helper'

describe command('yarn info underscore') do
  its(:stdout) { should contain("name: 'underscore'") }
  its(:stdout) { should contain("'dist-tags': { latest: '1.8.3', stable: '1.8.3' }") }
end
