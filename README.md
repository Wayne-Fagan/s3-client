# A Simple S3 Object Client

Although this S3 client can be used with AWS, the purpose of it's creation was to test Linode's Object Storage service.

### Purpose

This client enables you to `push`, `pull`, and `delete` objects to/from a given object.

### Issues using Linode's Object Storage:

    - Objects are not pushed directly to the bucket's root, instead a directory is automatically created using the bucket's name and all objects are pushed to this directory.
    
### Requirements

```
pipenv install boto3
```

### Environment variables

Create a `.env` file in the project root for the various expected Linode environment variables in `s3_client()`.