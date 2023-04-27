"""
Simple script to request a quota increase
"""
import boto3

sq = boto3.client('service-quotas')
paginator = sq.get_paginator('list_service_quotas')
page_iterator = paginator.paginate(ServiceCode='ec2')

desired_quotas = {
    "Running On-Demand Standard (A, C, D, H, I, M, R, T, Z) instances": 1,
    "All Standard (A, C, D, H, I, M, R, T, Z) Spot Instance Requests": 1,
    "Running On-Demand G and VT instances": 1,
    "All G and VT Spot Instance Requests": 1,
}

for page in page_iterator:
    for quota in page['Quotas']:
        quota_name = quota['QuotaName']
        if desired_quotas.get(quota_name):
            try:
                sq.request_service_quota_increase(
                    ServiceCode='ec2',
                    QuotaCode=quota['QuotaCode'],
                    DesiredValue=desired_quotas[quota_name]
                )
                print(f"Logging quota increase request for {quota_name}")
            except sq.exceptions.ResourceAlreadyExistsException:
                print(f"Quota increase for {quota_name} already requested")
            except sq.exceptions.IllegalArgumentException as e:
                print(f"{quota_name}: {e}")
