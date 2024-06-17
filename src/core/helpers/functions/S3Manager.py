import boto3
import base64


class S3Manager:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3 = boto3.client("s3")

    def list_files(self):
        """
        This function is responsible for listing the files in the S3 bucket.
        """
        response = self.s3.list_objects(
            Bucket=self.bucket_name,
        )

        files = []
        if "Contents" in response:
            for file in response["Contents"]:
                file_name = file["Key"].split("/")[-1]
                file_type = file_name.split(".")[-1]
                file_timestamp = file["LastModified"].isoformat()
                url = self.__generate_presigned_url(file_name)
                files.append(
                    {
                        "name": file_name,
                        "type": file_type,
                        "url": url,
                        "timestamp": file_timestamp,
                    }
                )

        return files

    def upload_file(self, file_name, file_body, content_type):
        """
        This function is responsible for uploading a file to the S3 bucket.
        """
        
        file_body = file_body.split(",")[-1]

        self.s3.put_object(
            Bucket=self.bucket_name,
            Key=file_name,
            Body=base64.b64decode(file_body),
            ContentType=content_type,
        )

    def delete_file(self, file_name):
        """
        This function is responsible for deleting a file from the S3 bucket.
        """
        self.s3.delete_object(Bucket=self.bucket_name, Key=file_name)

    def __generate_presigned_url(self, file_name, expiration=3600):
        """
        This function is responsible for generating a presigned URL for the given file.
        """
        url = self.s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": self.bucket_name, "Key": file_name},
            ExpiresIn=expiration,
        )

        return url
