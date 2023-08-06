# Copyright 2018 The KaiJIN Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Top K"""


class TopkMetric():
  def __init__(self, topk=(1,), offset=0):
    self.topk = topk
    self.offset = offset

  def __call__(self, output, target):
    """Computes the precision@k for the specified values of k
    Inputs:
      output: [N, C]
      target: [N, ]
      topk: (1, k)
    Returns:
      list with shape(k): the correct percentage among N inputs.
    """
    maxk = max(self.topk)
    batch_size = target.size(0)

    _, pred = output.topk(maxk, 1, True, True)
    pred = self.offset + pred.t()
    correct = pred.eq(target.view(1, -1).expand_as(pred))

    res = []
    for k in self.topk:
      correct_k = correct[:k].view(-1).float().sum(0)
      res.append(correct_k.mul_(100.0 / batch_size))
    return res

  def result(self, step, top1, top5=None, elapsed=None,
             num_samples=None, by_error=False):
    s = 'Iter:%d' % step
    # top1
    if by_error:
      s += ', Error@top1:%3.2f%%' % (100. - top1)
    else:
      s += ', Prec@top1:%3.2f%%' % top1
    # top5
    if top5:
      if by_error:
        s += ', Error@top5:%3.2f%%' % (100. - top5)
      else:
        s += ', Prec@top5:%3.2f%%' % top5
    # elapsed
    if elapsed:
      s += ', Total Elapsed:%.2fs' % (elapsed / 1000)
    # samples
    if num_samples:
      s += ', Samples/Seconds:%.2f' % (num_samples * 1000 / elapsed)
    return s
