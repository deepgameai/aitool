# -*- coding: UTF-8 -*-
# Copyright©2020 xiangyuejia@qq.com All Rights Reserved
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
"""
操作路径
"""
import os


def get_user_root_path() -> str:
    """
    获取用户根目录（~）的路径

    >>> get_user_root_path() # doctest: +ELLIPSIS
    '...'
    """
    return os.path.expanduser('~')


def get_current_path() -> str:
    """
    获取当前路径

    >>> get_current_path() # doctest: +ELLIPSIS
    '...'
    """
    current_directory = os.path.dirname(os.path.abspath(__file__))
    return current_directory


if __name__ == '__main__':
    import doctest

    doctest.testmod()
