import boto3
from botocore.exceptions import ClientError
import os
import logging


'''
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-examples.html 
'''
class S3Util:
    def __init__(self):
        self.region_name = 'us-east-1'

        self.s3_client = boto3.client(
            "s3",
            region_name=self.region_name
        )
        
        self.bucket_name = 'general-eval-240411'

        self.directory_name = 'cooking-recipe'

        self.logger = logging.getLogger(__name__)

    def get_credential_information(self):
        session = boto3.Session()
        credentials = session.get_credentials()
        
        # Fetch and log the credentials
        if credentials:
            self.logger.info("AWS Access Key ID: %s", credentials.access_key)
            self.logger.info("AWS Secret Access Key: %s", credentials.secret_key[:5] + '*' * 15)  # Only show first 5 characters for security
            if credentials.token:
                self.logger.info("AWS Session Token: %s", credentials.token[:10] + '*' * 20)  # Only show first 10 characters for security
        else:
            self.logger.warning("No AWS credentials found")

        # Fetch and log the caller identity
        sts_client = boto3.client('sts')
        try:
            caller_identity = sts_client.get_caller_identity()
            self.logger.info("AWS Account ID: %s", caller_identity['Account'])
            self.logger.info("AWS ARN: %s", caller_identity['Arn'])
            self.logger.info("AWS User ID: %s", caller_identity['UserId'])
        except Exception as e:
            self.logger.error("Error fetching caller identity: %s", str(e))

    def list_all_bucket(self):
        """列出所有存储桶"""
        try:
            response = self.s3_client.list_buckets()

            self.logger.info('Existing buckets:')

            for bucket in response['Buckets']:
                self.logger.info(f"  {bucket['Name']}")
            
            return response['Buckets']
        except ClientError as e:
            self.logger.error(f"Error listing buckets: {e}")
            return []

    def create_bucket(self, bucket_name, region=None):
        """Create an S3 bucket in a specified region

        If a region is not specified, the bucket is created in the S3 default
        region (us-east-1).

        :param bucket_name: Bucket to create
        :param region: String region to create bucket in, e.g., 'us-west-2'
        :return: True if bucket created, else False
        """

        # Create bucket
        try:
            if region is None:
                self.s3_client.create_bucket(Bucket=bucket_name)
            else:
                location = {'LocationConstraint': region}
                self.s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration=location
                )
            print(f"Bucket {bucket_name} created successfully")
            return True
        except ClientError as e:
            logging.error(e)
            print(f"Error creating bucket {bucket_name}: {e}")
            return False


    def upload_file(self, file_name, object_name=None):
        """Upload a file to the S3 bucket
        
        Args:
            file_name: File to upload
            object_name: S3 object name. If not specified then file_name is used
        
        Returns:
            str: The uploaded object name if successful, else None
        """
        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)

        # 确保对象名称包含目录
        if self.directory_name not in object_name:
            object_name = f"{self.directory_name}/{object_name}"

        try:
            self.s3_client.upload_file(file_name, self.bucket_name, object_name)
            self.logger.info(f"File {file_name} uploaded successfully to {self.bucket_name}/{object_name}")
            return object_name
        except ClientError as e:
            self.logger.error(f"Error uploading file {file_name} to {self.bucket_name}/{object_name}: {e}")
            return None


    def download_file(self, file_path, object_name=None):
        """从 S3 存储桶下载文件到本地文件系统
        
        Args:
            file_path: 本地文件保存路径
            object_name: S3对象名称，如果为None则使用file_path的基础名称
        
        Returns:
            str: 下载的对象名称，如果失败则返回None
        """
        if object_name is None:
            object_name = os.path.basename(file_path)

        # 确保对象名称包含目录
        if self.directory_name not in object_name:
            object_name = f"{self.directory_name}/{object_name}"

        try:
            # 确保目标目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            self.s3_client.download_file(self.bucket_name, object_name, file_path)
            self.logger.info(f"File {object_name} downloaded from {self.bucket_name} to {file_path}")
            return object_name
        except ClientError as e:
            self.logger.error(f"Error downloading file {object_name} from {self.bucket_name}: {e}")
            return None
        

    def get_presigned_url(self, object_name, expiration=3600):
        """
        生成一个预签名的URL来共享S3对象

        :param object_name: S3对象名称
        :param expiration: 签名的有效期（秒），默认1小时
        :return: 预签名的URL作为字符串。如果出错则返回None。
        """
        # 确保对象名称包含目录
        if self.directory_name not in object_name:
            object_name = f"{self.directory_name}/{object_name}"

        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': object_name
                },
                ExpiresIn=expiration
            )
            self.logger.info(f"Generated presigned URL for {object_name}")
            return url
        except ClientError as e:
            self.logger.error(f"Error generating presigned URL for {object_name}: {e}")
            return None

    

