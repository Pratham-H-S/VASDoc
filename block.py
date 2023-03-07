import hashlib


def hashGenerator(data):
  result = hashlib.sha256(data.encode())
  return result.hexdigest()


class Block:

  def __init__(self, data, hash, prev_hash):
    self.data = data
    self.hash = hash
    self.prev_hash = prev_hash


class Blockchain:

  def __init__(self):
    hashLast = hashGenerator('gen_last')
    hashStart = hashGenerator('gen_hash')

    genesis = Block('gen-data', hashStart, hashLast)
    self.chain = [genesis]

  def add_block(self, data):
    prev_hash = self.chain[-1].hash
    hash = hashGenerator(data + prev_hash)
    block = Block(data, hash, prev_hash)
    self.chain.append(block)


class new_block:
  # def __init__(self):
  #   hashLast=hashGenerator('gen_last')
  #   hashStart=hashGenerator('gen_hash')

  #   genesis=Block('gen-data',hashStart,hashLast)
  #   self.chain=[genesis]
  def __init__(self):
    self.chain = []
  
  def add_block(self, data):
    prev_hash = "0x00000000000000000"
    hash = hashGenerator(data + prev_hash)
    block = Block(data, hash, prev_hash)
    self.chain.append(block)


bc = Blockchain()
bc.add_block('student')
mentors_count = input("Enter the number of mentors: ")
mentors_list = []
mentors = new_block()
# mentors.add_block('usha')
for i in range(0,int(mentors_count)):
  mentors_list.append(input("Enter the mentor name:"))
  mentors.add_block(mentors_list[i]) 
print(mentors_list)



for i in mentors.chain:
  bc.add_block(i.hash)

for i in mentors.chain:
  print(i.__dict__)
  # print(i.hash)
  
for block in bc.chain:
    print(block.__dict__)
    # print("hash is :\n",block.hash)
