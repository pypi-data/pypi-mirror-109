import logging
import json
import datetime

from django.utils import timezone

from cloudant import CouchDB
from cloudant.error import CloudantDatabaseException

from ...settings import COUCHDB_DATASTORE_USER, COUCHDB_DATASTORE_PASSWORD, COUCHDB_DATASTORE_URL, \
                        COUCHDB_DATASTORE_DATABASE_NAME, BACKUP_MODE

logger = logging.getLogger('django_project_backup.utils.couchdb.adapter')


def response_to_json_dict(response, **kwargs):
    """
    Standard place to convert responses to JSON.

    :param response: requests response object
    :param **kwargs: arguments accepted by json.loads

    :returns: dict of JSON response
    """
    if response.encoding is None:
        response.encoding = 'utf-8'
    return json.loads(response.text, **kwargs)


class DBAdapter:
    """
    CouchDB DBAdapter
    """

    def get_database_name(self):
        if BACKUP_MODE == 'full':
            now = timezone.now()
            return '{}__{}'.format(COUCHDB_DATASTORE_DATABASE_NAME,
                                   now.strftime("%Y_%m_%d"))
        else:
            return COUCHDB_DATASTORE_DATABASE_NAME

    def __init__(self):
        self.client = CouchDB(COUCHDB_DATASTORE_USER, COUCHDB_DATASTORE_PASSWORD,
                              url=COUCHDB_DATASTORE_URL,
                              connect=True,
                              auto_renew=True,
                              use_basic_auth=True)

        database_name = self.get_database_name()

        try:
            self.database = self.client[database_name]
        except KeyError:
            self.database = self.client.create_database(database_name)

    def __del__(self):
        self.client.disconnect()

    def get_documents_ids(self):
        database_name = self.get_database_name()
        url = '/'.join((self.client.server_url, database_name, '_all_docs'))

        resp = self.client.r_session.get(url)
        resp.raise_for_status()

        rows = response_to_json_dict(resp)['rows']

        return [row['id'] for row in rows]

    def put_documents(self, docs):
        return self.database.bulk_docs(docs)
        # cloudant should return [{'ok': True, 'id': '1', 'rev': 'n-xxxxxxx'}]

    def put_document(self, doc):
        try:
            _res = self.database.create_document(doc, throw_on_exists=True)
            return True

        except CloudantDatabaseException:
            updated = False

            while not updated:
                existing = self.database[doc['_id']]

                existing_rev = existing['_rev']
                doc['_rev'] = existing_rev

                _updated = self.put_documents([doc])
                logger.debug('Couchdb reponse: {}'.format(_updated))

                update_status = list(filter(lambda x: x['id'] == doc['_id'], _updated))[0]


                error_status = update_status.get('error', None)

                success_status = update_status.get('ok', error_status is not None and \
                                                         error_status == 'conflict')

                updated = success_status

            return updated

    def get_documents(self):
        return self.database.all_docs(include_docs=True)

    def delete_document(self, key):
        to_delete = self.database[key]
        to_delete.delete()

        return key
