import os
import click
import requests
import logging
import boto3

logger = logging.getLogger(__name__)


@click.command()
@click.option("--in", "-i", "in_file",
              required=False,
              help="Path to the file to be processed.",
              )
@click.option("--gofile", "server_url", help="gofile server",
              flag_value='https://srv-store4.gofile.io',
              default=False
              )
@click.option("--s3bucket", "-s3", "bucket_name", help="s3 bucket name")
@click.option("--path", "-p", "path", help="multi file upload path")
@click.option('--verbose', is_flag=True, help="Verbose output for debugging")
def process(in_file: str,
            server_url: str,
            bucket_name: str,
            path: str,
            verbose: bool
            ):
    """This is the script to upload files to gofile & s3"""

    # if verbose:
    #     log_formatter = '%(asctime)s - %(levelname)s - %(message)s'
    #     logging.basicConfig(format=log_formatter, level=logging.DEBUG)

    # upload_to(in_file, server_url)
    if bucket_name:
        if path:
            upload_multi_s3(in_file, bucket_name, path)
        else: 
            upload_s3(in_file, bucket_name)


def upload_s3(in_file: str, bucket_name: str):
    s3 = boto3.client('s3')
    data = open(in_file, "rb")
    # response = s3.upload_file(in_file, bucket_name, in_file, ExtraArgs={'ACL': 'public-read'})
    response = s3.put_object(ACL='public-read',
                             Body=data,
                             Bucket=bucket_name,
                             Key=in_file,
                             ContentType='text/html')
    status_code = response['ResponseMetadata']['HTTPStatusCode']
    if status_code == 200:
        click.echo(f"The file download link is: https://{bucket_name}.s3.ap-southeast-2.amazonaws.com/{in_file}")
    else:
        logging.error("Error in uploading to S3! The status code is %s", status_code)


def upload_multi_s3(in_file: str, bucket_name: str, path: str):
    s3 = boto3.client('s3')
    for root,dirs,files in os.walk(path):
        for file in files:
            key="{path}/{file}".format(path=path, file=file)
            data = open(key, "rb")
            response = s3.put_object(ACL='public-read',
                                    Body=data,
                                    Bucket=bucket_name,
                                    Key=key.format(file=file),
                                    ContentType='text/html')
            status_code = response['ResponseMetadata']['HTTPStatusCode']
            if status_code == 200:
                click.echo(f"The file download link is: https://{bucket_name}.s3.ap-southeast-2.amazonaws.com/{key}")
            else:
                logging.error("Error in uploading to S3! The status code is %s", status_code)

def upload_to(in_file: str, server_url: str):
    url = server_url + "/uploadFile"
    file = {'file': open(in_file, 'rb')}

    logger.info("start uploading file: %s to server: %s", in_file, server_url)
    try:
        r = requests.post(url=url, files=file)

        logger.debug("This is the request url: %s", url)
        logger.debug("This is the response status code: %s", r.status_code)
        logger.debug("This is the response header: %s", r.headers)
        logger.debug("This is the response content %s ", r.content)

        if r.status_code != 200:
            logger.error(f"Error! The status code is {r.status_code}")
        else:
            code_link = "https://gofile.io/d/" + r.json()['data']['code']
            click.secho(f"File Download Link: {code_link}", fg="blue", bold=True)

            logger.info("The file download link is %s", code_link)
    except (requests.ConnectionError,
            requests.HTTPError,
            requests.Timeout,
            requests.TooManyRedirects,
            requests.RequestException) as e:
        logging.exception(f"Exception occurred during calling the server: {e}")


if __name__ == "__main__":
    process()

