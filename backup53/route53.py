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

import pprint
import boto
import time
import boto.route53
import json
import re
from boto.route53.record import ResourceRecordSets


class Route53():

    def __init__(self, location, debug):
        self
        self.backup = dict({})
        self.location = location
        self.region = 'universal'
        self.record = ''
        self.debug = debug

    def enable_connection(self):
        self.connection = boto.route53.connect_to_region(self.region)

    def get_zones(self):
        return self.connection.get_zones()

    def create_zone(self, zone_name):
        return self.connection.create_hosted_zone(zone_name)

    def clean_text(self, text):
        return re.sub('<[^>]*>', '', text.strip())

    def zone_sorter(self, loc):
        split = loc.split('.')
        return (split[::-1], -len(split))

    def restore_zone_structure(self):
        print 'Restoring zones'
        keys = self.backup.keys()
        order = sorted(keys, key=self.zone_sorter)
        for zone in order:
            if str(self.connection.get_zone(zone)) == 'None':
                print 'Creating Zone %s' % zone
                self.create_zone(zone)
                # Rate limit for AWS, if they can't process the request before
                # the next one comes it returns a 400
                time.sleep(1)
            else:
                print 'Zone already exists : %s' % zone
        print 'Restored empty zone structure'

    def get_zone_info(self, zone_id):
        return self.connection.get_hosted_zone(zone_id)['GetHostedZoneResponse']['HostedZone']

    def store_record(self, record, zone_name):
        name = record_type = ttl = ''
        values = []
        record_values = str(record.to_xml()).split('\n')
        for attr in record_values:
            if 'Name' in attr:
                name = self.clean_text(attr)
            elif 'Value' in attr:
                values.append(self.clean_text(attr))
            elif 'TTL' in attr:
                ttl = self.clean_text(attr)
            elif 'Type' in attr:
                record_type = self.clean_text(attr)
            self.record = {'Name': name, 'Value': values, 'TTL': ttl, 'Type': record_type}
            self.backup[zone_name]['Data'].append(self.record)

    def backup_zones(self):
        try:
            zones = self.get_zones()
            for zone in zones:
                zone_records = zone.get_records()
                zone_info = self.get_zone_info(zone_records.hosted_zone_id)
                zone_name = zone_info['Name']
                self.backup[zone_name] = {'Data': [], 'Description': zone_info}
                if self.debug:
                    print zone_name
                for record in zone_records:
                    self.store_record(record, zone_name)
            if self.debug:
                pp = pprint.PrettyPrinter(indent=4)
                pp.pprint(self.backup)
            return True
        except boto.route53.exception.DNSServerError:
            return False

    def restore_ns(self, zone_name, record):
        record_name = record['Name']
        record_ttl = record['TTL']
        try:
            new_zone = self.connection.get_zone(record_name)
        except AttributeError:
            self.create_zone(new_zone)
            new_zone = self.connection.get_zone(record_name)
        root_zone = self.connection.get_zone(zone_name)
        try:
            ns_changes = ResourceRecordSets(
                self.connection, root_zone.id)
            ns_glue = ns_changes.add_change(
                "UPSERT", record_name, "NS", ttl=record_ttl)
            for value in new_zone.get_nameservers():
                ns_glue.add_value(value)
            ns_changes.commit()
        except AttributeError:
            print 'Failed to get Name Servers and set glue for %s => %s' \
                % (zone_name, record_name)
        time.sleep(0.25)
        print 'Creating NS glue for %s => %s' % (zone_name, record_name)

    def restore_other(self, record, zone_name):
        record_name = record['Name']
        record_values = record['Value']
        record_ttl = record['TTL']
        record_type = record['Type']
        zone = self.connection.get_zone(zone_name)
        try:
            record_changes = ResourceRecordSets(
                self.connection, zone.id)
            new_record = record_changes.add_change(
                "UPSERT", record_name, record_type, ttl=record_ttl)
            for value in record_values:
                new_record.add_value(value)
            record_changes.commit()
            print 'Adding record %s %s' % (record_type, record_name)
            time.sleep(0.25)
        except (boto.route53.exception.DNSServerError, AttributeError):
            print 'Failed to insert %s %s => %s' \
                % (record_type, record_name, str(record_values))

    def restore_zones(self):
        try:
            zones = self.backup.keys()
            print 'Adding records to zones'
            for zone in zones:
                zone_records = self.backup[zone]['Data']
                zone_description = self.backup[zone]['Description']
                zone_name = zone
                for record in zone_records:
                    record_name = record['Name']
                    record_type = record['Type']
                    if (record_type == 'NS' and record_name != zone_name):
                        self.restore_ns(zone_name, record)
                    elif (record_type not in ['NS', 'SOA']):
                        self.restore_other(record, zone_name)
            return True
        except boto.route53.exception.DNSServerError:
            return False

    def jsonize_data(self):
        try:
            with open(self.location, 'wb') as f:
                json.dump(self.backup, f)
            return True
        except IOError:
            return False

    def dejsonize_data(self):
        try:
            with open(self.location, 'r') as f:
                self.backup = json.load(f)
            return True
        except IOError:
            return False

    def clean_up(self):
        self = None
