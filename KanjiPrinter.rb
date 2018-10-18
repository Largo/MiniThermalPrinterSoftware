require 'escpos'
require 'escpos/Helpers'
require 'serialport' # use Kernel::require on windows, works better.
require 'escpos/image'

while true do
@printer = Escpos::Printer.new
#@printer.Helpers.encode(1)
#@printer.write Escpos::Helpers.encode("日本語能力試験-JLPT／N3")
@printer.write gets
#@printer.write "\n"
#@printer.cut!

data = @printer.to_escpos


# require 'rubyserial'
# serialport = Serial.new 'COM3', 115200, 8, :none, 1
# serialport.write(data)
# serialport.close

#params for serial port
# port_str = "COM4"  #may be different for you
# baud_rate = 115200
# data_bits = 8
# stop_bits = 1
# parity = SerialPort::NONE
#
# sp = SerialPort.new(port_str, baud_rate, data_bits, stop_bits, parity)
# sp.sync = true
# sp.write(data)

open('testfile', 'w') { |f|
  f.puts data
}

open('history.txt', 'w+') { |f|
	f.puts data
}

system('print /D:"\\\DESKTOP-T84DD2P\Thermal Printer (USB)" testfile')
end
