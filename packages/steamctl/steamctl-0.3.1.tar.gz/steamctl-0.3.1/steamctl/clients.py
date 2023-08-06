import gevent.monkey
gevent.monkey.patch_socket()
gevent.monkey.patch_ssl()

import os
import logging
from steam.enums import EResult
from steam.client import SteamClient
from steam.client.cdn import CDNClient, CDNDepotManifest, CDNDepotFile
from steam.exceptions import SteamError

from steamctl.utils.format import fmt_size
from steamctl.utils.storage import UserCacheFile, UserDataFile, UserDataDirectory, ensure_dir, sanitizerelpath

cred_dir = UserDataDirectory('client')

class CachingSteamClient(SteamClient):
    credential_location = cred_dir.path
    _LOG = logging.getLogger('CachingSteamClient')

    def __init__(self, *args, **kwargs):
        if not cred_dir.exists():
            cred_dir.mkdir()
        SteamClient.__init__(self, *args, **kwargs)
        self._bootstrap_cm_list_from_file()

    def _handle_login_key(self, message):
        SteamClient._handle_login_key(self, message)

        with UserDataFile('client/%s.key' % self.username).open('w') as fp:
            fp.write(self.login_key)

    def get_cdnclient(self):
        return CachingCDNClient(self)

    def login_from_args(self, args, print_status=True):
        result = None

        if not args.anonymous and not args.user:
            last = UserDataFile('client/lastuser')

            if last.exists():
                args.user = last.read_full()

        if args.anonymous or not args.user:
            print("Attempting anonymous login")
            return self.anonymous_login()

        if args.user:
            print("Attempting login as: %s" % args.user)
            self.username = args.user

            userkey =  UserDataFile('client/%s.key' % self.username)
            if userkey.exists():
                self.login_key = userkey.read_full()
                result = self.relogin()

                if result == EResult.InvalidPassword:
                    print("Remembered login has expired")
                    userkey.remove()

            if not self.logged_on:
                result = self.cli_login(self.user)

        return result


class CTLDepotFile(CDNDepotFile):
    def download_to(self, target, no_make_dirs=False, pbar=None):
        relpath = sanitizerelpath(self.filename)

        if no_make_dirs:
            relpath = os.path.basename(relpath)

        relpath = os.path.join(target, relpath)

        filepath = os.path.abspath(relpath)
        ensure_dir(filepath)

        checksum = self.file_mapping.sha_content.hex()

        with open(filepath, 'wb') as fp:
            if pbar:
                pbar.write('Downloading to {}  ({}, {})'.format(
                    relpath,
                    fmt_size(self.size),
                    checksum
                    ))

            for chunk in self.chunks:
                data = self.manifest.cdn_client.get_chunk(
                                self.manifest.app_id,
                                self.manifest.depot_id,
                                chunk.sha.hex(),
                                )

                fp.write(data)

                if pbar:
                    pbar.update(len(data))

class CTLDepotManifest(CDNDepotManifest):
    DepotFileClass = CTLDepotFile


class CachingCDNClient(CDNClient):
    DepotManifestClass = CTLDepotManifest
    _LOG = logging.getLogger('CachingCDNClient')

    def __init__(self, *args, **kwargs):
        CDNClient.__init__(self, *args, **kwargs)

        # load the cached depot decryption keys
        self.depot_keys.update(self.get_cached_depot_keys())

    def get_cached_depot_keys(self):
        return {int(depot_id): bytes.fromhex(key)
                for depot_id, key in (UserDataFile('depot_keys.json').read_json() or {}).items()
                }

    def save_cache(self):
        cached_depot_keys = self.get_cached_depot_keys()

        if cached_depot_keys == self.depot_keys:
            return

        self.depot_keys.update(cached_depot_keys)
        out = {str(depot_id): key.hex()
               for depot_id, key in self.depot_keys.items()
               }

        UserDataFile('depot_keys.json').write_json(out)

    def get_cached_manifest(self, app_id, depot_id, manifest_gid):
        key = (app_id, depot_id, manifest_gid)

        if key in self.manifests:
            return self.manifests[key]

        # if we don't have the manifest loaded, check cache
        cached_manifest = UserCacheFile("manifests/{}_{}_{}".format(app_id, depot_id, manifest_gid))

        # we have a cached manifest file, load it
        if cached_manifest.exists():
            with cached_manifest.open('rb') as fp:
                try:
                    manifest = self.DepotManifestClass(self, app_id, fp.read())
                except Exception as exp:
                    self._LOG.debug("Error parsing cached manifest: %s", exp)
                else:
                    # if its not empty, load it
                    if manifest.gid > 0:
                        self.manifests[key] = manifest
                        return manifest

            # empty manifest files shouldn't exist, handle it gracefully by removing the file
            if key not in self.manifests:
                self._LOG.debug("Found cached manifest, but encountered error or file is empty")
                cached_manifest.remove()

    def is_manifest_cached(self, app_id, depot_id, manifest_gid):
        return self.get_cached_manifest(app_id, depot_id, manifest_gid) is not None

    def get_manifest(self, app_id, depot_id, manifest_gid, decrypt=True):
        key = (app_id, depot_id, manifest_gid)
        cached_manifest = UserCacheFile("manifests/{}_{}_{}".format(*key))

        if key not in self.manifests:
            self.get_cached_manifest(*key)

        # if we still dont have a manifest, load it from CDN
        if key not in self.manifests:
            manifest = CDNClient.get_manifest(self, app_id, depot_id, manifest_gid, decrypt)

            # cache the manifest
            with cached_manifest.open('wb') as fp:
                fp.write(manifest.serialize(compress=False))

        return self.manifests[key]
