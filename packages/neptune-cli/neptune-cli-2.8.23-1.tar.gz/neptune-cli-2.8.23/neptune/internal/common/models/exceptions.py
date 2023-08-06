#
# Copyright (c) 2016, deepsense.io
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
#
from neptune.internal.common import NeptuneException


class NeptuneInvalidArgumentException(NeptuneException):
    def __init__(self, message):
        super(NeptuneInvalidArgumentException, self).__init__(message)


class NeptuneParameterConversionException(NeptuneException):
    def __init__(self, param_api_model, param_value, destination_type, reason):
        super(NeptuneParameterConversionException, self).__init__(
            u"{reason} Failed to convert experiment parameter '{name}'={value} to {type}.".format(
                reason=reason,
                name=param_api_model.name,
                value=param_value,
                type=destination_type.__name__
            )
        )
