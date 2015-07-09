require 'spec_helper'

describe command('pip show django-extensions') do
  its(:stdout) { should contain('Version: 1.5.5') }
end
