import os
import click
import requests
import logging
import boto3
import asyncio

async def main():
     print('hello')
     await asyncio.sleep(3)
     print('world')

if __name__ == "__main__":
   asyncio.run(main())