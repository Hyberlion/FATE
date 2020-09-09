#
#  Copyright 2019 The FATE Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
import numpy
from federatedml.feature.sparse_vector import SparseVector


def dataset_to_list(src):
    if isinstance(src, numpy.ndarray):
        return src.tolist()
    elif isinstance(src, list):
        return src
    elif isinstance(src, SparseVector):
        vector = [0] * src.get_shape()
        for idx, v in src.get_all_data():
            vector[idx] = v
        return vector
    else:
        return [src]


def get_header_schema(header_line):
    header_source_item = header_line.split(',')
    return {'header': ','.join(header_source_item[1:]).strip(), 'sid': header_source_item[0]}


def default_output_path(name, namespace):
    return f"/fate/output_data/{namespace}/{name}"


def default_input_path(name, namespace):
    return f"/fate/input_data/{namespace}/{name}"
