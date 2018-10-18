#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy

import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont

from escpos.printer import Usb

from time import sleep

g_pos_y = 0

def draw_text(img, text, align='left', size=24):
  global g_pos_y
  draw = PIL.ImageDraw.Draw(img)
  draw.font = PIL.ImageFont.truetype(
    'fonts/NotoSansCJKjp-Regular.otf', size)

  img_size = numpy.array(img.size)
  txt_size = numpy.array(draw.font.getsize(text))
  pos = (img_size - txt_size) / 2

  if align == 'center':
    x = ((img_size - txt_size) / 2)[0]
  elif align == 'right':
    x = (img_size - txt_size)[0]
  else:
    x = 0

  #draw.text(pos, text, (0, 0, 0))
  draw.text((x, g_pos_y), text, (0, 0, 0))
  g_pos_y += size

def create_img(name, tadashi, copy=''):
  global g_pos_y
  g_pos_y = 0

  img = PIL.Image.new('RGB', (384, 550), (255,255,255))

  draw_text(img, '領収書' + copy, align='center', size=48)
  draw_text(img, ' ')
  draw_text(img, '平成29年10月31日', align='right')
  draw_text(img, ' ')
  draw_text(img, name + ' 様', size=36)
  draw_text(img, ' ')
  draw_text(img, '===================', align='center')
  draw_text(img, '金額 ¥1,000円', align='center', size=36)
  draw_text(img, '===================', align='center')
  draw_text(img, ' ')
  draw_text(img, '但し、')
  draw_text(img, tadashi + 'として')
  draw_text(img, '上記正に領収致しました。')
  draw_text(img, '                                ')
  draw_text(img, '      〒xxx-xxxx xxx市xxxxx', align='right')
  draw_text(img, '                 xx公民館内', align='right')
  draw_text(img, '                   xx自治会', align='right', size=36)
  draw_text(img, '               担当：　　　', align='right')
  gray = img.convert('L')
  img = gray.point(lambda x: 0 if x < 128 else 255)
  #img.show()
  img.save('output.png')

def main():
  names = [
    '神社 太郎',
    '神社 次郎',
    '神社 三郎',
  ]
  tadashi = 'xx神社祭典運営費拠出金'

  for name in names:
    create_img(name, tadashi)
    sleep(0.5)
    p = Usb(0x0416, 0x5011, out_ep=3)
    p.image('output.png')
    p.text('\n\n\n')

    print('Please hit any key')
    input()

    create_img(name, tadashi, copy=' ＜控＞')
    sleep(0.5)
    p = Usb(0x0416, 0x5011, out_ep=3)
    p.image('output.png')
    p.text('\n\n\n')

    print('Please hit any key')
    input()


main()