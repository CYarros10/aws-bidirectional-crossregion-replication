# bidirectional-cross-region-replication

## Deploying a Highly Available Data Storage Solution

Use CloudFormation to deploy two S3 buckets in two separate regions that are
synced via bidirectional cross region replication.

### Why

Cross-Region replication can help you do the following:

**Meet compliance requirements** — Although Amazon S3 stores your data across
multiple geographically distant Availability Zones by default, compliance
requirements might dictate that you store data at even greater distances.
Cross-Region replication allows you to replicate data between distant AWS
Regions to satisfy these requirements.

**Minimize latency** — If your customers are in two geographic locations, you can
minimize latency in accessing objects by maintaining object copies in AWS
Regions that are geographically closer to your users.

**Increase operational efficiency** — If you have compute clusters in two different
AWS Regions that analyze the same set of objects, you might choose to maintain
object copies in those Regions.

### About

This solution deploys two S3 buckets equipped with bi-directional cross region
replication. This means that any object action in region/bucket 1 will be
replicated to region/bucket 2. Any object action in region/bucket 2 will be
replicated to region/bucket 1.  The two buckets will remain synced.

### Audience

200-300 level. Customers and architects looking to deploy a highly available,
fault tolerant, cross-region data storage solution via Infrastructure as code.

----

## Deploy the Solution

1. Upload deploy_bidirectional_crr.zip to an existing S3 bucket. CloudFormation
will reference this code when deploying the solution.

2. Go to [Cloudformation Console](https://console.aws.amazon.com/cloudformation/).

3. Upload master.yaml template.

## Test the Solution

1. Go to [S3 Console](https://console.aws.amazon.com/s3).

2. You will see two buckets. prefix-region-1 and prefix-region-2.  Upload a file
 to bucket 1 and then go to bucket 2 to see the replication occur.

3. replication also occurs on deletes. Delete the object in bucket 2 and go back
 to bucket 1. the object will be gone.

4. Replication utilized Object Versioning. On the S3 Console for Bucket 1,
select Show Versions. You'll see the deleted object is not actually gone, it is
hidden and has a delete marker associated with it.

## Infrastucture Clean Up

1. Once you are done and would like to tear down the infrastructure, ensure that
 you delete all objects and versions from the primary bucket, bucket 1.

2. Then, go to the CloudFormation console to delete the stack.  The Stack will
delete all objects and versions in bucket 2, and then will remove the bucket 2
itself.
