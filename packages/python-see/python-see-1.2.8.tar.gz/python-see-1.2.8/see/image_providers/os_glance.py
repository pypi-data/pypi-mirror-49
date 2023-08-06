# Copyright 2015-2017 F-Secure

# Licensed under the Apache License, Version 2.0 (the "License"); you
# may not use this file except in compliance with the License.  You may
# obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.  See the License for the specific language governing
# permissions and limitations under the License.
"""Glance image provider.

This provider retrieves the requested image from an OpenStack Glance service if
it doesn't already exist on the configured target path. Images can be requested
by name or UUID; if name is requested the latest matching image is retrieved.

provider_parameters:
    target_path (str): Absolute path where to download the image. If target_path
                       is an existing file, it will be overwritten if the image
                       is newer. Otherwise target_path is understood to be a
                       directory and the image's UUID will be used as filename.
    os_auth (dict):    A dictionary with OpenStack authentication parameters as
                       needed by OpenStack's Keystone client.
    session (dict):    A dictionary with OpenStack Session parameters. Allows
                       authentication to Keystone over TLS.

"""

import os
import hashlib
import tempfile

from datetime import datetime
from see.interfaces import ImageProvider

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


def verify_checksum(path, checksum):
    hash_md5 = hashlib.md5()
    with open(path, 'rb') as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            hash_md5.update(chunk)
    return hash_md5.hexdigest() == checksum


class GlanceProvider(ImageProvider):

    def __init__(self, parameters):
        super(GlanceProvider, self).__init__(parameters)
        self._os_session = None
        self._glance_client = None

    @property
    def image(self):
        try:
            metadata = self._retrieve_metadata()
        except FileNotFoundError:
            if os.path.exists(self.configuration['target_path']):
                if os.path.isfile(os.path.realpath(
                        self.configuration['target_path'])):
                    return self.configuration['target_path']
                else:
                    for image in self._find_potentials():
                        tgt = os.path.join(self.configuration['target_path'],
                                           image.id)
                        if os.path.exists(tgt):
                            return tgt
            raise

        if (os.path.exists(self.configuration['target_path']) and
                os.path.isfile(os.path.realpath(
                    self.configuration['target_path'])) and
                datetime.fromtimestamp(os.path.getmtime(
                    self.configuration['target_path'])) >
                datetime.strptime(metadata.updated_at, "%Y-%m-%dT%H:%M:%SZ")):
            return self.configuration['target_path']

        target = (self.configuration['target_path']
                  if os.path.isfile(self.configuration['target_path'])
                  else '/'.join((self.configuration['target_path'].rstrip('/'),
                                 metadata.id)))
        os.makedirs(os.path.dirname(os.path.realpath(target)))

        self._download_image(metadata, target)
        return target

    @property
    def _token(self):
        return self.os_session.get_token()

    @property
    def os_session(self):
        if self._os_session is None:
            from keystoneauth1.identity import v3
            from keystoneauth1.session import Session

            self._os_session = Session(auth=v3.Password(**self.configuration['os_auth']),
                                       verify=self.configuration['session'].get('cacert', False),
                                       cert=self.configuration['session'].get('cert'))
        return self._os_session

    @property
    def glance_client(self):
        if self._glance_client is None:
            from glanceclient.v2.client import Client as Gclient
            glance_endpoints = self.os_session.get('/v3/users',
                                                   endpoint_filter={
                                                       'service_type': 'image',
                                                       'interface': 'public'
                                                   }).json()
            glance_current_version = next((version for version in glance_endpoints.get('versions')
                                           if version['status'] == 'CURRENT'), None)
            glance_url = glance_current_version.get('links')[0]['href']
            self._glance_client = Gclient(glance_url, token=self._token,
                                          **self.configuration['os_auth'])
        return self._glance_client

    def _find_potentials(self):
        return sorted([image for image in self.glance_client.images.list()
                       if (image.id == self.uri or image.name == self.uri)
                       and image.status != 'active'],
                      key=lambda x: x.updated_at, reverse=True)

    def _retrieve_metadata(self):
        try:
            return sorted([image for image in self.glance_client.images.list()
                           if (image.id == self.uri or image.name == self.uri)
                           and image.status == 'active'],
                          key=lambda x: x.updated_at, reverse=True)[0]
        except IndexError:
            raise FileNotFoundError(self.uri)

    def _download_image(self, img_metadata, target):
        img_downloader = self.glance_client.images.data(img_metadata.id)
        _, temp = tempfile.mkstemp(dir=os.path.dirname(target), suffix='.part')
        with open(temp, 'wb') as imagefile:
            for chunk in img_downloader:
                imagefile.write(chunk)
        if not verify_checksum(temp, img_metadata.checksum):
            os.remove(temp)
            raise RuntimeError('Checksum failure. File: %s' % target)
        os.rename(temp, target)
