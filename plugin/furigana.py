#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import re

import sys

# get the length of the commong prefix of str1 and str2
def common_prefix(str1, str2):
  for i, c in enumerate(str1):
    if str2[i] != c:
      return i

# get the length of the commong suffix of str1 and str2
def common_suffix(str1, str2):
  for i, c in enumerate(reversed(str1)):
    if str2[-(i + 1)] != c:
      return i

def format_string(format_str, kanji, reading):
  return format_str.replace('%k', kanji).replace('%r', reading).replace('%%', '%')

def add_ruby(string, format_str='%k[%r]'):
  # open kakasi
  try:
    kakasi = subprocess.Popen(['kakasi', '-iutf8', '-outf8', '-KH', '-u'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  except OSError:
    raise Exception("Error running kakasi")

  # open mecab
  try:
    mecab = subprocess.Popen(['mecab', '--node-format=%m[%f[7]]\x1f', '--eos-format=\\n', '--unk-format=%m[]\x1f'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  except OSError:
    raise Exception("Error running mecab")

  # split into parts to preserve spaces
  parts = []
  for part in string.split(' '):
    mecab.stdin.write(part + '\n')
    mecab.stdin.flush()
    nodes = unicode(mecab.stdout.readline(), 'utf-8').rstrip('\r\n')

    out = ""
    for node in nodes.split('\x1f'):
      if not node:
        continue

      (kanji, reading) = re.match('(.+)\[(.*)\]', node).groups()
      if not reading:
        out += kanji
      else:
        # transform reading to hiragana
        kakasi.stdin.write(reading.encode('utf-8') + '\n')
        kakasi.stdin.flush()
        result = unicode(kakasi.stdout.readline(), 'utf-8').rstrip('\r\n')

        # transform kanji to hiragana (to check for katakana).
        # kakasi only transforms katakana to hiragana. if transformed "kanji"
        # is identical to transformed reading it was katakana.
        kakasi.stdin.write(kanji.encode('utf-8') + '\n')
        kakasi.stdin.flush()
        result_kanji = unicode(kakasi.stdout.readline(), 'utf-8').rstrip('\r\n')

        if kanji == result: # no reading
          out += kanji
        elif result == result_kanji: # Katakana
          out += kanji
        else:
          prefix = common_prefix(kanji, result)
          suffix = common_suffix(kanji, result)
          if suffix != 0:
            out += kanji[:prefix]
            out += format_string(format_str, kanji[prefix:-suffix], result[prefix:-suffix])
            out += kanji[-suffix:]
          else:
            out += kanji[:prefix]
            out += format_string(format_str, kanji[prefix:], result[prefix:])

    parts.append(out)

  mecab.terminate()
  kakasi.terminate()
  return ' '.join(parts)

def add_ruby_substring(string, col_start, col_end, format_str='%k[%r]'):
  content = string[0:col_start]
  content += add_ruby(string[col_start:col_end], format_str)
  content += string[col_end:]
  return content


if __name__ == '__main__':
  print 'Ahoy!'

  # TODO: move format string into setting
  format_str = "\\ruby{%k}{%r}"

  sentence = 'ご飯はfoo bar baz置いてますか。お金が欲しい。テニスをします。\n'

  print add_ruby(sentence, format_str)
  print add_ruby(sentence)

  print 'Bye!'
