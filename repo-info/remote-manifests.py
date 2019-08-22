#!/usr/bin/python3
from requests import get, codes
from sys import argv
from json import dumps
from argparse import ArgumentParser
from subprocess import run


class Manifest:
    def __init__(self):
        parser = ArgumentParser(prog='Remote Docker Manifest', description='')

        help_message = 'The docker image from which takes the manifest info. Format' \
                       ' <[namespace/]repository[:tag]> [<[namespace/]repository[:tag]>...'
        parser.add_argument('-i', '--image', default='flopez/fiware-management-scripts', help=help_message)

        args = parser.parse_args()
        image = args.image

        if ":" in image:
            self.image, self.tag = image.split(":")
        else:
            self.image, self.tag = image, "latest"

        if "/" not in self.image:
            self.image = "library/" + self.image

        self.login_template = "https://auth.docker.io/token?service=registry.docker.io&scope=repository:{repository}:pull"
        self.get_manifest_template = "https://registry.hub.docker.com/v2/{repository}/manifests/{tag}"
        self.accept_types = "application/vnd.docker.distribution.manifest.v2+json"
        self.accept_types_list = "application/vnd.docker.distribution.manifest.list.v2+json"

        self.data = dict()

        self.migrate_units = {'B': 'KB', 'KB': 'MB'}

    def output(self):
        txt_initial = """
## `{}`
    
-	Manifest MIME: \'{}\'
-	Platforms:
    -	{}
"""

        txt_info = """
### `{}` - {}
    
-	Docker Version: {}
-	Manifest MIME: \'{}\'
-	Total Size: {}
    (compressed transfer size, not on-disk size)
"""

        txt_layers = """
-	Layers: {}
"""

        txt_layer = """
    -   digest: {}
        Size: {}
        MIME: \'{}\'  
"""

        manifest_mime = self.accept_types_list
        # platform = 'linux; amd64'
        platform = self.data['architecture']
        name = self.data['name'] + ":" + self.data['tag']
        txt_initial = txt_initial.format(name, manifest_mime, platform)

        temp_layer = ''
        total_size = 0
        layers = self.data['layers']
        for i in range(0, len(layers)):
            media_type = layers[i]['mediaType']

            size = int(layers[i]['size'])
            total_size = total_size + size
            size = self.get_size(size)

            digest = layers[i]['digest']
            aux = txt_layer.format(digest, size, media_type)
            temp_layer = temp_layer + aux

        txt_layers = txt_layers.format(temp_layer)

        total_size = '**{}**'.format(self.get_size(total_size))
        docker_version = self.data['docker_version']
        # default_command = '["python", "/home/management/fiware-management-scripts/management.py"]'
        manifest_mime = self.accept_types
        txt_info = txt_info.format(name, platform, docker_version, manifest_mime, total_size)

        print(txt_initial + "\n" + txt_info + "\n" + txt_layers)

    def get_size(self, i, unit='B'):
        if int(i / 1000) > 0 and unit in self.migrate_units.keys():
            aux = self.get_size(i / 1000, self.migrate_units[unit])
        elif unit is 'B':
            aux = "{} {}".format(i, unit)
        else:
            aux = "{:.2f} {}".format(i, unit)

        return aux

    def get_data(self):
        # Get Docker version
        command = "docker --version | awk '{print $3\" \"$4\" \"$5}'"
        aux = run([command], shell=True, capture_output=True)
        self.data['docker_version'] = aux.stdout.decode().rstrip()

        # Get layers info
        self.data['layers'] = self.__get_manifest__()
        self.data['name'], self.data['tag'], self.data['architecture'] = self.__get_manifest_list__()

    def __get_manifest__(self):
        """
        repo: string, repository (e.g. 'library/fedora')
        tag:  string, tag of the repository (e.g. 'latest')
        """
        response = get(self.login_template.format(repository=self.image), json=True)
        response_json = response.json()
        token = response_json["token"]
        response = get(
            self.get_manifest_template.format(repository=self.image, tag=self.tag),
            headers={"Authorization": "Bearer {}".format(token), "accept": self.accept_types},
            json=True
        )
        manifest = response.json()

        if not response.status_code == codes.ok:
            print(dict(response.headers))
            exit()

        return manifest['layers']

    def __get_manifest_list__(self):
        """
        repo: string, repository (e.g. 'library/fedora')
        tag:  string, tag of the repository (e.g. 'latest')
        """
        response = get(self.login_template.format(repository=self.image), json=True)
        response_json = response.json()
        token = response_json["token"]
        response = get(
            self.get_manifest_template.format(repository=self.image, tag=self.tag),
            headers={"Authorization": "Bearer {}".format(token), "accept": self.accept_types_list},
            json=True
        )
        manifest = response.json()

        if not response.status_code == codes.ok:
            print(dict(response.headers))
            exit()

        return manifest['name'], manifest['tag'], manifest['architecture']


if __name__ == "__main__":
    manifest = Manifest()
    manifest.get_data()
    manifest.output()
