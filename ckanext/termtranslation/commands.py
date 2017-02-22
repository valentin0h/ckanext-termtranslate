import sys
import os
import json

from ckan import model
from ckan.logic import get_action, ValidationError

from ckan.lib.cli import CkanCommand

JSON_TRANSLAION_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'json'))


class TermTranslation(CkanCommand):
    '''Translate CKAN terms using simple json structure

    Usage:

      term-translate all
        - Update all terms found in json files in the json directory

      term-translate {file}
        - Update terms found in a given json file

    The commands should be run from the ckanext-termtranslation director.
    '''

    summary = __doc__.split('\n')[0]
    usage = __doc__

    def __init__(self, name):
        super(TermTranslation, self).__init__(name)

    def command(self):
        self._load_config()

        # We'll need a sysadmin user to perform most of the actions
        # We will use the sysadmin site user (named as the site_id)
        context = {'model': model, 'session': model.Session, 'ignore_auth': True}
        self.admin_user = get_action('get_site_user')(context, {})

        print ''

        if len(self.args) == 0:
            self.parser.print_usage()
            sys.exit(1)

        file = self.args[0]
        if file == 'all':
            self.update_all_terms()
        else:
            self.update_file_terms()

    def _load_config(self):
        super(TermTranslation, self)._load_config()

    def _update_term(self, data):
        data_dict = {"data": data}

        context = {
            'model': model,
            'session': model.Session,
            'user': self.admin_user['name'],
            'ignore_auth': True,
        }
        result = get_action('term_translation_update_many')(context, data_dict)
        return result

    def update_all_terms(self):
        try:
            dirs = os.listdir(JSON_TRANSLAION_DIR)
            for f in dirs:
                try:
                    terms_to_update = []
                    with open(JSON_TRANSLAION_DIR + '/' + f) as json_data:
                        d = json.load(json_data)
                        for term in d:
                            for lang_code in term['translation']:
                                data = dict()
                                data["term"] = term['term']
                                data["lang_code"] = lang_code
                                data["term_translation"] = term['translation'][lang_code]
                                terms_to_update.append(data)

                    result = self._update_term(terms_to_update)
                    print "Updated file : {}\t{}".format(f, result['success'].replace("row", "term"))
                except ValueError:
                    print "Failed to read file : {}".format(f)

        except Exception, e:
            print 'An error occurred:'
            print str(e.error_dict)
            raise e

    def update_file_terms(self):
        pass
