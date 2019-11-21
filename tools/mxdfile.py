#!/usr/bin/env python
#*- encoding: utf-8 -*
import struct
import zlib
import json

import pdb

ALIGNMENT = [
  'Hero',
  'Rogue',
  'Vigilante',
  'Villain',
  'Loyalist',
  'Resistance',
]

def readFloat(bs):
  f, = struct.unpack('f', bs[:4])
  return f, bs[4:]

def readInt(bs):
  i, = struct.unpack('i', bs[:4])
  return i, bs[4:]

def readByte(bs):
  b, = struct.unpack('b', bs[0])
  return b, bs[1:]

def readBool(bs):
  b, = struct.unpack('?', bs[0])
  return b, bs[1:]

def readString(bytestream):
  R = bytestream[:]
  length, R = readByte(R)
  if length == 0:
    return '', bytestream[1:]
  keepgoing, length = bool(length & 0x80), (length & 0x7f)
  kg = 1
  shift = 0
  while keepgoing:
    kg += 1
    shift += 7
    n, R = readByte(R)
    keepgoing, nn = bool(n & 0x80), n & 0x7f
    length += (nn << shift)

  return R[:length], bytestream[(kg + length):]

class MXDFile(object):
  _filename = ''
  _raw = ''
  _info = {}

  def __init__(self, filename, raw):
    self._filename = filename
    self._raw = raw
    self._process_raw_data()

  def dump(self):
    print "Hero File: %s" % self._filename
    print json.dumps(self._info, indent=2, separators=(',', ': '))

  @classmethod
  def load(cls, filename):
    with open(filename, 'r') as mxdfile:
      lines = mxdfile.read()
      lines = lines.replace('||', '|\n|')
      lines = lines.split('\n')

      # Ignore all the plaintext.
      lines = [line for line in lines if line.startswith('|') and line.endswith('|')]

      # Ignore all the lines that don't start with '|MxD'
      while lines and not lines[0].startswith('|MxD'):
        lines = lines[1:]

      # Ignore all the lines that are just dashes
      lines = [line for line in lines if not line.startswith('|-') and not line.startswith('-|')]

      assert len(lines) >= 2
      header = lines[0].strip('|')
      encoded = ''.join([line.strip('|') for line in lines[1:]])

      fields = header.split(';')
      assert len(fields) == 6

      MAGIC_UNCOMPRESSED = 'MxDu'
      MAGIC_COMPRESSED = 'MxDz'

      magicNumber = fields[0]
      compressed = False

      if magicNumber == MAGIC_COMPRESSED:
        compressed = True
      elif magicNumber == MAGIC_UNCOMPRESSED:
        compressed = False

      size_uncompressed = int(fields[1], 10)
      size_compressed = int(fields[2], 10)
      size_encoded = int(fields[3], 10)

      assert size_compressed < size_uncompressed

      hex_field = fields[4]
      assert hex_field == 'HEX'

      empty = fields[5]
      assert empty == ''

      assert len(encoded) == size_encoded

      compressed = bytearray.fromhex(encoded)
      assert len(compressed) == size_compressed

      uncompressed = zlib.decompress(str(compressed))
      assert len(uncompressed) == size_uncompressed

      return cls(filename=filename, raw=uncompressed)

  def _process_raw_data(self):
    info = {}

    if not self._raw:
      return
    R = self._raw[:]

    MAGIC_NUMBER = 'MxD' + chr(12)
    while R and R[:4] != MAGIC_NUMBER:
      R = R[1:]

    assert R[:4] == MAGIC_NUMBER
    R = R[4:]

    version, R = readFloat(R)
    assert version <= 2.0
    self._version = version
    info["Version"] = version

    qualifiedNames, R = readBool(R)

    hasSubPower, R = readBool(R)

    classID, R = readString(R)
    info['Class ID'] = classID

    originID, R = readString(R)
    info['Origin ID'] = originID

    if version >= 1.0:
      alignment, R = readInt(R)
      info['Alignment'] = ALIGNMENT[alignment]

    charName, R = readString(R)
    info['Character Name'] = charName

    powerSetCount, R = readInt(R)
    info['Powerset Count'] = powerSetCount

    info['Powersets'] = []
    seen = 0
    while seen < powerSetCount:
      powerSetName, R = readString(R)
      if powerSetName:
        info['Powersets'].append(powerSetName)
        seen += 1

    assert seen == powerSetCount

    powerCount, R = readInt(R)
    info['Power Count'] = powerCount


    # DONE.
    self._info = info



if __name__ == '__main__':
  import argparse
  ap = argparse.ArgumentParser()
  ap.add_argument("filename", type=str)
  args, _ = ap.parse_known_args()
  hero = MXDFile.load(args.filename)
  try:
    hero.dump()
  except UnicodeDecodeError:
    print hero._info
