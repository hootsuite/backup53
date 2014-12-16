backup53
==========

#Purpose 

DNS is just sort of important, it's the glue that resolves names to addresses. Ensuring the integrity of it and the ability to backup and restore it is critical for organizations that do not have a secondary provider. Since Amazon does not provide a tool to backup and restore your hosted zones this tool allows you to backup and dynamically restore them; persisting nameserver glue records between zones. It is still early in testing and a recovery from a total DNS record/zone loss still requres a few manual steps (pointing root level domain registrar records at new nameservers, etc.) but it is a step in the right direction.

#Features

* Backs up Amazon Route53 DNS Zones/Records to JSON
* Restore Zones/Records safely by creating new zones and recreating the glue between sub-domains and parent domains
* Stores all DNS Zones/Records in the following JSON format:

#JSON Template

```
u'hosted_zone.com.': {  'Data':[  {  'Name': '',
                                     'TTL': '17800',
                                     'Type': 'NS',
                                     'Value': [   '',
                                                  '',
                                                  '',
                                                  '']},
                                  {   'Name': '',
                                      'TTL': '900',
                                      'Type': 'SOA',
                                      'Value': [   '']},
                                  {   'Name': '',
                                      'TTL': '300',
                                      'Type': 'CNAME',
                                      'Value': ['']}
                                ],
                        'Description': {   u'CallerReference': u'',
                                           u'Config': {   },
                                           u'Id': u'/hostedzone/ID',
                                           u'Name': u'',
                                           u'ResourceRecordSetCount': u'3'}}
```
#Configuration/Installation

###Warning###

This tool has the potential to cause damage to your Route53 zones/records if used improperly (restoring a backup by accident, restoring to the wrong account, etc.), Use at your own risk.

##Installation##

```sudo python setup.py install```


Ensure you have Boto configured properly (either with environment variables or .boto config). Be certain you are using the right account to backup and restore to as it can be dangerous.

```.boto``` contents
```
[Credentials]
aws_access_key_id = <AWS Access Key>
aws_secret_access_key = <AWS Secret>
```
#Usage
tests:
```
cd tests/
python tests.py
```

backup: 

```backup53 --action backup --location backup.json```

restore: 

```backup53 --action restore --location backup.json```


