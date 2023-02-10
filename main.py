class Expression():
  def __init__(self, data):
    self.children = []
    self.data = data

  def __repr__(self):
    return self.data
  
  def add_child(self, child):
    self.children.append(child)

  def parallelise(self, parallelism, buckets=None):
    if not buckets:
      buckets = [[] for bucket in range(0, parallelism)]
    for child in self.children:
      buckets = child.parallelise(parallelism, buckets)
    return buckets

class Variable():
  def __init__(self):
    pass

class EndJump(Expression):
  def __init__(self, loop, loop_variable, limit):
    super(EndJump, self).__init__("jump to {}".format(loop))
    self.loop = loop

class Loop(Expression):
  def __init__(self, index, limit):
    super(Loop, self).__init__("for i = 0 i < {} i++".format(limit))
    self.index = index
    self.limit = limit
    self.loop_variable = Variable()
    self.end = EndJump(self, self.loop_variable, limit)

  def parallelise(self, parallelism, buckets):
    bucket_count = self.limit / parallelism
    print(self.limit)
    print(bucket_count)
    current_bucket = 0
    for bucket_index, bucket in enumerate(range(round(bucket_count))):
        
        for line_index, line in enumerate(self.children):
          buckets[(current_bucket) % len(buckets)].append(line)
          current_bucket = current_bucket + 1
    return buckets
    

root = Expression("root")
loop = Loop(0, 100)
root.add_child(loop)
loop.add_child(Expression("d += 100"))
loop.add_child(Expression("m += 200"))
loop.add_child(Expression("j += 300"))
loop.add_child(Expression("c += 400"))

items = 100 * 4

for bucket_index, bucket in enumerate(root.parallelise(12)):
  print("###### {} bucket".format(bucket_index))
  print(bucket)