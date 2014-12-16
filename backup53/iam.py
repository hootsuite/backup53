# Copyright 2014 Steven Richards - Hootsuite Media -
# <steven.richards@hootsuite.com>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# 	http://www.apache.org/license/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License

import boto
import boto.iam


class IAM():

    def get_account_info(self):
        self.account_info = self.connection.get_account_alias()
        try:
            return self.account_info['list_account_aliases_response']['list_account_aliases_result']['account_aliases'][0]
        except IndexError:
            return 'confirm'

    def enable_connection(self):
        self.connection = boto.iam.connect_to_region('universal')

    def __init__(self):
        self
        self.connection = None
        self.account_info = None
