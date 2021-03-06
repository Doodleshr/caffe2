# Copyright (c) 2016-present, Facebook, Inc.
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
##############################################################################

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from caffe2.python import core
from hypothesis import given
import caffe2.python.hypothesis_test_util as hu
import hypothesis.strategies as st
import numpy as np


class TestElementwiseOps(hu.HypothesisTestCase):

    @given(n=st.integers(2, 10), m=st.integers(4, 6),
           d=st.integers(2, 3), **hu.gcs)
    def test_div(self, n, m, d, gc, dc):
        X = np.random.rand(n, m, d).astype(np.float32)
        Y = np.random.rand(n, m, d).astype(np.float32) + 5.0

        def div_op(X, Y):
            return [np.divide(X, Y)]

        op = core.CreateOperator(
            "Div",
            ["X", "Y"],
            ["Z"]
        )

        self.assertReferenceChecks(
            device_option=gc,
            op=op,
            inputs=[X, Y],
            reference=div_op,
        )

        self.assertGradientChecks(
            gc, op, [X, Y], 0, [0], stepsize=1e-4, threshold=1e-2)

    @given(n=st.integers(5, 6), m=st.integers(4, 6), **hu.gcs)
    def test_log(self, n, m, gc, dc):
        X = np.random.rand(n, m).astype(np.float32) + 1.0

        def log_op(X):
            return [np.log(X)]

        op = core.CreateOperator(
            "Log",
            ["X"],
            ["Z"]
        )

        self.assertReferenceChecks(
            device_option=gc,
            op=op,
            inputs=[X],
            reference=log_op,
        )

        self.assertGradientChecks(
            gc, op, [X], 0, [0], stepsize=1e-4, threshold=1e-2)

    @given(n=st.integers(5, 6), m=st.integers(4, 6), **hu.gcs)
    def test_sqr(self, n, m, gc, dc):
        X = np.random.rand(n, m).astype(np.float32)

        def sqr_op(X):
            return [np.square(X)]

        op = core.CreateOperator(
            "Sqr",
            ["X"],
            ["Z"]
        )

        self.assertReferenceChecks(
            device_option=gc,
            op=op,
            inputs=[X],
            reference=sqr_op,
        )

        self.assertGradientChecks(
            gc, op, [X], 0, [0], stepsize=1e-4, threshold=1e-2)

    @given(n=st.integers(5, 6), m=st.integers(4, 6), **hu.gcs)
    def test_sigmoid(self, n, m, gc, dc):
        X = np.random.rand(n, m).astype(np.float32)

        def sigmoid(X):
            return [1. / (1. + np.exp(-X))]

        op = core.CreateOperator(
            "Sigmoid",
            ["X"],
            ["Z"]
        )

        self.assertReferenceChecks(
            device_option=gc,
            op=op,
            inputs=[X],
            reference=sigmoid,
        )

        self.assertGradientChecks(
            gc, op, [X], 0, [0], stepsize=1e-4, threshold=1e-2)
