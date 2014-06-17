#!  /usr/bin/ruby

require 'sanitize'

def cmain args
  args.each do |arg|
    File.open(arg) do |fch|
      got = Sanitize.clean(fch.read, Sanitize::Config::RELAXED)
      $stdout.puts got
    end
  end
  0
end

exit(cmain(ARGV))
