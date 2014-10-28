import boto
import boto.route53
import pprint
import argparse
import json
from boto.route53.record import ResourceRecordSets


class Route53():
    
    def enable_connection(self):
        self.connection = boto.route53.connect_to_region(self.region) 
        
    def get_records(self,zone):
        return zone.get_records()
    
    def get_zones(self):
        return self.connection.get_zones()

    def backup_zones(self):
    	zones = self.get_zones()
    	for zone in zones:
    		zone_name = str(zone).split(':')[1].split('.>')[0]
    		self.backup[str(zone_name)] = str(self.get_records(zone))
    	return self.backup

    def jsonize_records(self):
    	try:
    		with open(self.location, 'w') as f:
    			json.dump(self.backup, f)
    			return True
    	except IOError:
    		return False

    def clean_up(self):
    	self = None
        
    def __init__(self, location, region):
        self
        self.backup = dict({})
        self.location = location
        self.region = region

class Main():

    def main():
    	opt = argparse.ArgumentParser(description='AWS Instance Provisioning Tool') 
    	opt.add_argument('--region', help='Specify connection region for Route53', required=False, default='us-east-1')
    	opt.add_argument('--location', help='Location to store JSON backup of records', required=True)
        args = vars(opt.parse_args())

        r53 = Route53(args['location'],args['region'])
        r53.enable_connection()
        r53.backup_zones()
        r53.jsonize_records()
        r53.clean_up()


    if __name__ == '__main__':
        main()