require 'spec_helper'

INSTALLED_PACKAGES = ['fortune', 'Delorean', 'lodash@4.2.1', 'nyancat@0.0.4', 'jquery#2.1.4']
NOT_INSTALLED_PACKAGES = ['cowsay', 'scipy', 'bootstrap', 'brain', 'browserify']

describe command('cappa list') do
  let(:disable_sudo) { true }

  INSTALLED_PACKAGES.each do |pkg|
      its(:stdout) { should contain(pkg) }
  end

  NOT_INSTALLED_PACKAGES.each do |pkg|
      its(:stdout) { should_not contain(pkg) }
  end
end
