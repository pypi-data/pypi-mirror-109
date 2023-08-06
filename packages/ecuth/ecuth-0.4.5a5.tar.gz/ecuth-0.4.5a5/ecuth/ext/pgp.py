# standard imports
import logging
import tempfile
import urllib.request
import os

# third-party imports
import gnupg

# local imports
from ecuth.challenge import ChallengeRetriever
from ecuth.error import AlienMatterError

logg = logging.getLogger()


class PGPRetriever(ChallengeRetriever):


    def __init__(self, fetcher, parser, trusted_keys, gnupg_home=None):
        super(PGPRetriever, self).__init__(fetcher, parser, self._fingerprint_from_challenge_response)
        self.gpg = gnupg.GPG(gnupghome=gnupg_home)
        self.trusted = trusted_keys
        self.auth_keys = []
           

    def verify_import(self, export, signature):
        (h, tmp_signature) = tempfile.mkstemp()
        f = open(tmp_signature, 'w')
        f.write(signature)
        f.close()

        r = self.gpg.verify_data(tmp_signature, export.encode('utf-8'))
        os.unlink(tmp_signature)
        logg.debug('r {}'.format(r.status))
        if r.status != 'signature valid':
            return False
        return r.fingerprint in self.trusted


    def import_keys(self, export, signature):
        r = self.gpg.import_keys(export)
        if not self.verify_import(export, signature):
            raise AlienMatterError('pgp public key bundle')
        for k in r.results:
            if k['fingerprint'] == None:
                logg.debug('skipping invalid auth key')
                continue
            logg.info('imported auth pgp key {}'.format(k['fingerprint']))
            self.auth_keys.append(k['fingerprint'])


    def _fingerprint_from_challenge_response(self, challenge, signature):
        fn = tempfile.mkstemp()
        f = open(fn[1], 'wb')
        f.write(signature)
        f.close()

        v = None
        try: 
            v = self.gpg.verify_data(fn[1], challenge)
        except Exception as e:
            logg.error('error verifying {}'.format(e))
            return None

        if not v.valid:
            logg.error('signature not valid {}'.format(v.fingerprint))
            return None

        logg.debug('signature valid!')
        return bytes.fromhex(v.fingerprint)
