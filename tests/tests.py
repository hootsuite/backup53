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

import unittest
from backup53.iam import IAM
from backup53.route53 import Route53
import boto.route53

class Tests(unittest.TestCase):
	def setUp(self):
		location = 'test.json'
		self.r53 = Route53(location, False)
		self.zone_name = "test.com"
		self.record_one_type = "NS"
		self.record_two_type = "SOA"
		self.record_name = "test.com."
		self.ns_ttl = "172800"
		self.soa_value = "ns-1113.awsdns-09.org. awsdns-hostmaster.amazon.com. 1 7200 900 1209600 86400"
		self.soa_ttl = "900"
		self.ns_values = ["ns-1110.awsdns-09.org.",
		"ns-1111.awsdns-56.co.uk.",
		"ns-1112.awsdns-35.com.",
		"ns-1113.awsdns-16.net."]
	def test_load_json(self):
		self.assertTrue(self.r53.dejsonize_data())
	def test_is_dict(self):
		self.assertEquals(type(self.r53.backup), type(dict({})))
	def test_read_record_one(self):
		self.r53.dejsonize_data()
		self.assertEquals(self.r53.backup["test.com."]["Data"][0]["Type"], self.record_one_type)
		self.assertEquals(self.r53.backup["test.com."]["Data"][0]["Name"], self.record_name)
		self.assertEquals(self.r53.backup["test.com."]["Data"][0]["Value"], self.ns_values)
		self.assertEquals(self.r53.backup["test.com."]["Data"][0]["TTL"], self.ns_ttl)
	def test_read_record_two(self):
		self.r53.dejsonize_data()
		self.assertEquals(self.r53.backup["test.com."]["Data"][1]["Type"], self.record_two_type)
		self.assertEquals(self.r53.backup["test.com."]["Data"][1]["Name"], self.record_name)
		self.assertEquals(self.r53.backup["test.com."]["Data"][1]["Value"][0], self.soa_value)
		self.assertEquals(self.r53.backup["test.com."]["Data"][1]["TTL"], self.soa_ttl)
	def test_record_count(self):
		self.r53.dejsonize_data()
		self.assertEquals(self.r53.backup["test.com."]["Description"]["ResourceRecordSetCount"], str(len(self.r53.backup["test.com."].keys())))
	def test_get_zones(self):
		self.r53.enable_connection()
		self.assertEquals(type(self.r53.get_zones()), type([]))
	def test_connection(self):
		self.r53.enable_connection()
		self.assertIsInstance(self.r53.connection, boto.route53.connection.Route53Connection)
	def test_zone_sorter(self):
		url = "s3.amazonaws.com"
		self.assertEquals(self.r53.zone_sorter(url), (['com', 'amazonaws', 's3'], -3))

if __name__ == "__main__":
	unittest.main(verbosity=3)