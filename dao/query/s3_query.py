import os
import logging
from typing import List
from dao.dao_factory import DaoFactory
from dao.models.sql.doc_store import DocStoreMetadata
from dao.query.sql.doc_store import DocStoreQuery
from rag.structures.file_category import FileCategory
from aiengine.models import async_s3_session, s3_sync_client, aws_creds

def get_doc_object_by_doc_id_sync(doc_id: str):
    BUCKET_NAME = os.getenv('BUCKET_NAME')
    existing_doc:List[DocStoreMetadata] = DaoFactory.query_data(DocStoreQuery().by_doc_id(doc_id))
    if len(existing_doc) == 0:
        raise Exception(f"report for {doc_id} not found")
    s3_key = existing_doc[0].s3_key

    logging.info(f"s3_key: {s3_key} for doc_id: {doc_id}")
    return query_from_s3_sync(s3_key,BUCKET_NAME)

async def get_doc_object(doc_id: str):
    BUCKET_NAME = os.getenv('BUCKET_NAME')
    existing_doc:List[DocStoreMetadata] = DaoFactory.query_data(DocStoreQuery().by_doc_id(doc_id))
    if len(existing_doc) == 0:
        raise Exception(f"report for {doc_id} not found")
    s3_key = existing_doc[0].s3_key
    logging.info(f"s3_key: {s3_key} for doc_id: {doc_id}")
    return await query_from_s3(s3_key,BUCKET_NAME)



async def get_doc_object_by_s3_key(s3_key: str):
    BUCKET_NAME = os.getenv('BUCKET_NAME')
    return await query_from_s3(s3_key,BUCKET_NAME)


def get_doc_object_by_s3_key_sync(s3_key: str):
    BUCKET_NAME = os.getenv('BUCKET_NAME')
    return query_from_s3_sync(s3_key,BUCKET_NAME)

def query_from_s3_sync(s3_key: str, BUCKET_NAME: str):
    s3 = s3_sync_client
    response = s3.get_object(Bucket=BUCKET_NAME, Key=s3_key)
    body = response['Body'].read()
    return body

async def query_from_s3(s3_key: str, BUCKET_NAME: str):
    # Use aioboto3 for asynchronous S3 query
    try:
        async with async_s3_session.client('s3',**aws_creds) as s3:
            response = await s3.get_object(Bucket=BUCKET_NAME, Key=s3_key)
            body = await response['Body'].read()
            return body
    except Exception as e:
        logging.error(f"Error querying from s3: {e}")
        raise e

def insert_in_s3(s3_key,BUCKET_NAME,file_path):
    s3 = s3_sync_client
    s3.upload_file(file_path, BUCKET_NAME, s3_key)
    logging.info(f"Uploaded {file_path} to s3://{BUCKET_NAME}/{s3_key}")

def upload_object_to_s3(s3_key,BUCKET_NAME,file_object):
    s3 = s3_sync_client
    s3.put_object(Bucket=BUCKET_NAME, Key=s3_key, Body=file_object)
    logging.info(f"Uploaded object to s3://{BUCKET_NAME}/{s3_key}")


def delete_object_from_s3(s3_key,BUCKET_NAME):
    s3 = s3_sync_client
    s3.delete_object(Bucket=BUCKET_NAME, Key=s3_key)
    logging.info(f"Deleted {s3_key} from s3://{BUCKET_NAME}")


