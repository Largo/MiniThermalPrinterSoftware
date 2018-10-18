require 'escpos'
require 'escpos/Helpers'
require 'serialport' # use Kernel::require on windows, works better.
require 'escpos/image'

def write(text)
  @printer = Escpos::Printer.new
  @printer.write text

  data = @printer.to_escpos
  open('testfile', 'w') { |f|
    f.puts data
  }

  open('history.txt', 'a') { |f|
  f.puts text
 }

  system('print /D:"\\\DESKTOP-T84DD2P\Thermal Printer (USB)" testfile')
end

require 'fox16'
include Fox

class HelloWorld < FXMainWindow
  def initialize(app)
    super(app, "TP" , :width => 200, :height => 300)
    vFrame1 = FXVerticalFrame.new(self, :opts => LAYOUT_FILL)
    textArea = FXText.new(vFrame1, :opts => LAYOUT_FILL | TEXT_WORDWRAP)
    hFrame3 = FXHorizontalFrame.new(vFrame1)
    generateButton = FXButton.new(hFrame3, "Print")

    generateButton.connect(SEL_COMMAND) do
      write(textArea.text)
      textArea.removeText(0, textArea.length)
    end
  end
  def create
    super
    show(PLACEMENT_SCREEN)
  end
end

app = FXApp.new
HelloWorld.new(app)
app.create
app.run
