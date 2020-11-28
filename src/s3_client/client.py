import os

import boto3
import sys
from botocore.config import Config
from botocore.exceptions import ClientError


class S3ObjectClient:
    @staticmethod
    def s3_client():
        """
        Create s3 client
        """
        return boto3.resource(
            service_name=os.environ.get("LINODE_SERVICE_NAME_S3"),
            endpoint_url=os.environ.get("LINODE_ENDPOINT"),
            region_name=os.environ.get("LINODE_REGION"),
            aws_access_key_id=os.environ.get("LINODE_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("LINODE_SECRET_ACCESS_KEY"),
            config=Config(
                retries={
                    "max_attempts": int(os.environ.get("LINODE_MAX_RETRIES")),
                },
            ),
        )

    def push_object_to_bucket(self, file_path: str, key: str, file_name: str):
        """
        Push object to bucket
        """
        client = self.s3_client()

        try:
            # Key - s3 object's full path
            s3_path = f"{key}/{file_name}"
            target_path = f"{file_path}/{file_name}"
            client.Bucket(
                name=os.environ.get("LINODE_STORAGE_BUCKET_NAME")
            ).upload_file(
                Filename=target_path,
                Key=s3_path,
            )

            sys.stdout.write(f"{file_name} has been successfully pushed")

        except ClientError as e:
            sys.stdout.write(f"Pushing object {file_name} has failed: {e}")

    def pull_object_from_bucket(self, file_path: str, key: str, file_name: str):
        """
        Pull object from bucket.
        """
        client = self.s3_client()

        try:
            # Key - s3 object's full path
            s3_path = f"{key}/{file_name}"
            target_path = f"{file_path}/{file_name}"
            client.Bucket(
                name=os.environ.get("LINODE_STORAGE_BUCKET_NAME")
            ).download_file(Filename=target_path, Key=s3_path)

            sys.stdout.write(f"{file_name} has been successfully pulled")

        except ClientError as e:
            sys.stdout.write(f"Pulling object {file_name} has failed: {e}")

    def delete_object_from_bucket(self, key: str, file_name: str):
        """
        Delete object from bucket
        """
        client = self.s3_client()

        try:
            # Key - s3 object's full path.
            s3_path = f"{key}/{file_name}"
            client.Bucket(
                name=os.environ.get("LINODE_STORAGE_BUCKET_NAME"),
            ).Object(s3_path).delete()

            sys.stdout.write(f"{file_name} has been successfully deleted")

        except ClientError as e:
            sys.stdout.write(f"Deleting object {file_name} has failed: {e}")
