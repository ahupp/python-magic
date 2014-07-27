'''
Generate fileMimes as:
cd libmagic/magic/Magicdir
grep -R mime . > fileMimes

Then run this script to generate file_types.py
It's a simple dictionary of all mime-types and what Magicdir file
detects them.
'''

lines = open('fileMimes', 'r').readlines()

def dedupe(fileMimes):
  mimeType = []
  source = []
  final = {}
  for item in fileMimes:
    try:
      index = source[mimeType.index(item[0])]
      try:
        index.index(item[1])
      except:
        index.append(item[1])
    except:
        mimeType.append(item[0])
        source.append([item[1]])
  for item in mimeType:
    final[item] = source[mimeType.index(item)]

  return final

      

file_types = []

for line in lines:
  try:
    temp = line.split(':!:mime')
    temp[0] = temp[0].lstrip('./')
    temp[1] = temp[1].lstrip().rstrip()
    if temp[1][0] != '#':
      try:
        temp[1] = temp[1].split('#')[0].rstrip().rstrip('.')
      except:
        pass
      file_types.append((temp[1], temp[0]))
  except:
    pass

file_types = dedupe(file_types)
file_types = ("],\n" + ' ' * 12 + "'").join(str(file_types).split("], '"))
open('file_types.py', 'w').write(' '*8 + 'self.file_types = ' + file_types)
