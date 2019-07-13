from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.  You may obtain a copy of
# the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations under
# the License.
# ==============================================================================
import tensorflow_io.prometheus as prometheus_io  # pylint: disable=wrong-import-position
"""Tests for PrometheusDataset."""



import time
import subprocess
import sys
import pytest

import tensorflow as tf
if not (hasattr(tf, "version") and tf.version.VERSION.startswith("2.")):
  tf.compat.v1.enable_eager_execution()

if sys.platform == "darwin":
  pytest.skip(
      "prometheus is not supported on macOS yet", allow_module_level=True)


def test_prometheus_input():
  """test_prometheus_input
  """
  n=600
  q= n // 16

  for i in range(n):
    req_count = i % q
    q_count = i // q
    flip = (q_count % 2) == 1
    req_count = q - req_count if flip else req_count

    bump_factor = int(float(i) / n * q)

    for _ in range(req_count + bump_factor):
      subprocess.call(["dig", "@localhost", "-p", "1053", "www.google.com"], stdout=subprocess.PIPE)
    
    time.sleep(1)

  prometheus_dataset = prometheus_io.PrometheusDataset(
      "http://localhost:9090",
      schema="delta(coredns_dns_request_count_total[5s])[600s:5s]",
      batch=120)

  for k, v in prometheus_dataset:
    joined = zip(k.numpy(), v.numpy())
    for k1, v1 in joined:
      print(f"{k1},{v1}")

test_prometheus_input()
