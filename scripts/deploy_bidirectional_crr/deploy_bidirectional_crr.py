import os
import logging
import boto3
import cfnresponse

# Initialize Logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Initialize environment variables / variables
BUCKET_1 = str(os.environ['S3_BUCKET_1'])
ROLE_ARN_1 = str(os.environ['ROLE_ARN_1'])
REGION_1 = str(os.environ['REGION_1'])

BUCKET_2 = str(os.environ['S3_BUCKET_2'])
ROLE_ARN_2 = str(os.environ['ROLE_ARN_2'])
REGION_2 = str(os.environ['REGION_2'])

# Initialize S3 Client
S3_CLIENT_1 = boto3.client('s3', region_name=REGION_1)
S3_CLIENT_2 = boto3.client('s3', region_name=REGION_2)

def bidirectional_crr_deployer():
    """
    Creates a secondary bucket in second region
    enables versioning, encryption on secondary bucket
    put bucket replication on primary and secondary buckets
    """

    # create s3 bucket in second region
    S3_CLIENT_2.create_bucket(
        Bucket=BUCKET_2,
        CreateBucketConfiguration={
            'LocationConstraint': REGION_2
        }
    )

    # enable versioning
    S3_CLIENT_2.put_bucket_versioning(
        Bucket=BUCKET_2,
        VersioningConfiguration={
            'Status': 'Enabled'
        }
    )

    #enable encryption
    S3_CLIENT_2.put_bucket_encryption(
        Bucket=BUCKET_2,
        ServerSideEncryptionConfiguration={
            'Rules': [
                {
                    'ApplyServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'AES256'
                    }
                }
            ]
        }
    )

    # Put Bucket Replication on Bucket 1 -> Bucket 2
    S3_CLIENT_1.put_bucket_replication(
        Bucket=BUCKET_1,
        ReplicationConfiguration={
            'Role': ROLE_ARN_1,
            'Rules': [
                {
                    "ID": "test",
                    "Prefix": "",
                    "Status": "Enabled",
                    "Destination": {
                        "Bucket": "arn:aws:s3:::"+BUCKET_2
                    }
                }
            ]
        }
    )

    # Put Bucket Replication on Bucket 2 -> Bucket 1
    S3_CLIENT_2.put_bucket_replication(
        Bucket=BUCKET_2,
        ReplicationConfiguration={
            'Role': ROLE_ARN_2,
            'Rules': [
                {
                    "ID": "test",
                    "Prefix": "",
                    "Status": "Enabled",
                    "Destination": {
                        "Bucket": "arn:aws:s3:::"+BUCKET_1
                    }
                }
            ]
        }
    )

def delete_secondary_bucket():
    """
    Removes all objects, object versions from secondary bucket
    Deletes secondary bucket
    """

    s3_resource_2 = boto3.resource('s3', region_name=REGION_2)
    bucket = s3_resource_2.Bucket(BUCKET_2)
    bucket.objects.delete()
    bucket.object_versions.delete()
    bucket.delete()
    bucket.wait_until_not_exists()


def lambda_handler(event, context):
    """
    On CloudFormation CREATE/UPDATE events,
    deploy the bidirectional cross region replication solution

    On CloudFormation DELETE event,
    delete all objects, versions and secondary bucket itself.
    """

    if event['RequestType'] in ['Create', 'Update']:
        try:
            bidirectional_crr_deployer()
        except:
            cfnresponse.send(event, context, cfnresponse.FAILED, {})
        else:
            cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
    elif event['RequestType'] == 'Delete':
        try:
            delete_secondary_bucket()
        except:
            cfnresponse.send(event, context, cfnresponse.FAILED, {})
        else:
            cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
