require 'spec_helper'

describe command('bower list --allow-root') do
  let(:disable_sudo) { true }
  its(:stdout) { should contain("jquery#2.1.4") }
end
