## SWA Secure S3 Storage Bucket Stack Library

Define a S3 bucket that security will be proud of.

`S3StorageBucketStack` exposes the following deploy-time attributes from the underlying `bucket` construct:

* `bucketArn` - the ARN of the bucket (i.e. `arn:aws:s3:::bucket_name`)
* `bucketName` - the name of the bucket (i.e. `bucket_name`)
* `arnForObjects(pattern)` - the ARN of an object or objects within the bucket (i.e.
  `arn:aws:s3:::bucket_name/exampleobject.png` or
  `arn:aws:s3:::bucket_name/Development/*`)
* `urlForObject(key)` - the URL of an object within the bucket (i.e.
  `https://s3.cn-north-1.amazonaws.com.cn/china-bucket/mykey`)

`S3StorageBucketStack` exposes the following deploy-time methods from the underlying `bucket` construct:

* `add_lifecycle_rule`
* `add_metric`
* `add_object_created_notification`
* `add_object_removed_notificationself`
* `add_event_notification`
* `add_to_resource_policy`
* `arn_for_objects`
* `on_cloud_trail_event`
* `on_cloud_trail_put_object`
* `url_for_object`
