import subprocess
from datetime import datetime
from pprint import pprint

import openstack
from cloudmesh.abstractclass.ComputeNodeABC import ComputeNodeABC
from cloudmesh.common.Shell import Shell
from cloudmesh.common.console import Console
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.util import banner
from cloudmesh.common.util import path_expand
from cloudmesh.management.configuration.config import Config
from cloudmesh.provider import ComputeProviderPlugin
from cloudmesh.common.Printer import Printer
from cloudmesh.mongo.CmDatabase import CmDatabase
from cloudmesh.secgroup.Secgroup import Secgroup, SecgroupRule
from cloudmesh.secgroup.Secgroup import SecgroupExamples
from cloudmesh.common3.DictList import DictList

class Provider(ComputeNodeABC, ComputeProviderPlugin):

    kind = "openstack"

    output = {
        "status": {
            "sort_keys": ["cm.name"],
            "order": ["cm.name",
                      "cm.cloud",
                      "vm_state",
                      "status",
                      "task_state"],
            "header": ["Name",
                       "Cloud",
                       "State",
                       "Status",
                       "Task"]
        },
        "vm": {
            "sort_keys": ["cm.name"],
            "order": ["cm.name",
                      "cm.cloud",
                      "vm_state",
                      "status",
                      "task_state",
                      "image",
                      "public_ips",
                      "private_ips",
                      "project_id",
                      "launched_at",
                      "cm.kind"],
            "header": ["Name",
                       "Cloud",
                       "State",
                       "Status",
                       "Task",
                       "Image",
                       "Public IPs",
                       "Private IPs",
                       "Project ID",
                       "Started at",
                       "Kind"]
        },
        "image": {
            "sort_keys": ["cm.name",
                          "extra.minDisk"],
            "order": ["cm.name",
                      "size",
                      "min_disk",
                      "min_ram",
                      "status",
                      "cm.driver"],
            "header": ["Name",
                       "Size (Bytes)",
                       "MinDisk (GB)",
                       "MinRam (MB)",
                       "Status",
                       "Driver"]
        },
        "flavor": {
            "sort_keys": ["cm.name",
                          "vcpus",
                          "disk"],
            "order": ["cm.name",
                      "vcpus",
                      "ram",
                      "disk"],
            "header": ["Name",
                       "VCPUS",
                       "RAM",
                       "Disk"]
        },
        "key": {
            "sort_keys": ["name"],
            "order": ["name",
                      "type",
                      "format",
                      "fingerprint",
                      "comment"],
            "header": ["Name",
                       "Type",
                       "Format",
                       "Fingerprint",
                       "Comment"]
        },
        "secrule": {
            "sort_keys": ["name"],
            "order": ["name",
                      "tags",
                      "direction",
                      "ethertype",
                      "port_range_max",
                      "port_range_min",
                      "protocol",
                      "remote_ip_prefix",
                      "remote_group_id"
                      ],
            "header": ["Name",
                       "Tags",
                       "Direction",
                       "Ethertype",
                       "Port range max",
                       "Port range min",
                       "Protocol",
                       "Range",
                       "Remote group id"]
        },
        "secgroup": {
            "sort_keys": ["name"],
            "order": ["name",
                      "tags",
                      "description",
                      "rules"
                      ],
            "header": ["Name",
                       "Tags",
                       "Description",
                       "Rules"]
        },
    }


    def Print(self, output, kind, data):

        if output == "table":
            if kind == "secrule":

                result = []
                for group in data:
                    for rule in group['security_group_rules']:
                        rule['name'] = group['name']
                        result.append(rule)
                data = result


            order = self.output[kind]['order']  # not pretty
            header = self.output[kind]['header']  # not pretty

            print(Printer.flatwrite(data,
                                    sort_keys=["name"],
                                    order=order,
                                    header=header,
                                    output=output)
                  )
        else:
            print(Printer.write(data, output=output))

    @staticmethod
    def _get_credentials(config):
        """
        Internal function to create a dict for the openstacksdk credentials.

        :param config: The credentials from the cloudmesh yaml file
        :return: the dict for the openstacksdk
        """

        d = {'version': '2', 'username': config['OS_USERNAME'],
             'password': config['OS_PASSWORD'],
             'auth_url': config['OS_AUTH_URL'],
             'project_id': config['OS_TENANT_NAME'],
             'region_name': config['OS_REGION_NAME'],
             'tenant_id': config['OS_TENANT_ID']}
        # d['project_domain_name'] = config['OS_PROJECT_NAME']
        return d

    def __init__(self, name=None, configuration="~/.cloudmesh/cloudmesh4.yaml"):
        """
        Initializes the provider. The default parameters are read from the
        configurationfile that is defined in yaml format.

        :param name: The name of the provider as defined in the yaml file
        :param configuration: The location of the yaml configuration file
        """

        conf = Config(configuration)["cloudmesh"]
        super().__init__(name, conf)

        self.user = Config()["cloudmesh"]["profile"]["user"]
        self.spec = conf["cloud"][name]
        self.cloud = name

        self.default = self.spec["default"]
        self.cloudtype = self.spec["cm"]["kind"]

        self.cred = self.spec["credentials"]
        if self.cred["OS_PASSWORD"] == 'TBD':
            Console.error("The password TBD is not allowed")
        self.credential = self._get_credentials(self.cred)

        self.cloudman = openstack.connect(**self.credential)

        # self.default_image = deft["image"]
        # self.default_size = deft["size"]
        # self.default.location = cred["datacenter"]

        try:
            self.public_key_path = conf["profile"]["publickey"]
            self.key_path = path_expand(
                Config()["cloudmesh"]["profile"]["publickey"])
            f = open(self.key_path, 'r')
            self.key_val = f.read()
        except:
            raise ValueError("the public key location is not set in the "
                             "provile of the yaml file.")

    def update_dict(self, elements, kind=None):
        """
        THis function adds a cloudmesh cm dict to each dict in the list
        elements.
        Libcloud
        returns an object or list of objects With the dict method
        this object is converted to a dict. Typically this method is used
        internally.

        :param elements: the list of original dicts. If elements is a single
                         dict a list with a single element is returned.
        :param kind: for some kinds special attributes are added. This includes
                     key, vm, image, flavor.
        :return: The list with the modified dicts
        """

        if elements is None:
            return None
        elif type(elements) == list:
            _elements = elements
        else:
            _elements = [elements]
        d = []
        for entry in _elements:

            if kind == 'key':
                try:
                    entry['comment'] = entry['public_key'].split(" ",2)[2]
                except:
                    entry['comment'] = ""
                entry['format'] = \
                    entry['public_key'].split(" ", 1)[0].replace("ssh-","")

            entry["cm"] = {
                "kind": kind,
                "driver": self.cloudtype,
                "cloud": self.cloud,
                "name": entry['name']
            }
            if kind == 'vm':
                entry["cm"]["updated"] = str(datetime.utcnow())
                if "created_at" in entry:
                    entry["cm"]["created"] = str(entry["created_at"])
                    # del entry["created_at"]
                else:
                    entry["cm"]["created"] = entry["modified"]
            elif kind == 'flavor':
                entry["cm"]["created"] = entry["updated"] = str(
                    datetime.utcnow())

            elif kind == 'image':
                entry['cm']['created'] = str(datetime.utcnow())
                entry['cm']['updated'] = str(datetime.utcnow())
            # elif kind == 'secgroup':
            #    pass

            d.append(entry)
        return d

    def find(self, elements, name=None):
        """
        Finds an element in elements with the specified name.

        :param elements: The elements
        :param name: The name to be found
        :return:
        """

        for element in elements:
            if  element["name"] == name or element["cm"]["name"] == name:
                return element
        return None

    def keys(self):
        """
        Lists the keys on the cloud

        :return: dict
        """
        return self.get_list(self.cloudman.list_keypairs(),
                             kind="key")


    def key_upload(self, key=None):
        """
        uploads the key specified in the yaml configuration to the cloud
        :param key:
        :return:
        """

        name = key["name"]
        cloud = self.cloud
        Console.msg(f"upload the key: {name} -> {cloud}")
        try:
            r = self.cloudman.create_keypair(name,key['string'])
        except openstack.exceptions.ConflictException:
            raise ValueError(f"key already exists: {name}")

        return r

    def key_delete(self, name=None):
        """
        deletes the key with the given name
        :param name: The anme of the key
        :return:
        """

        cloud = self.cloud
        Console.msg(f"delete the key: {name} -> {cloud}")
        r = self.cloudman.delete_keypair(name)

        return r

    def list_secgroups(self, name=None):
        """
        List the named security group

        :param name: The name of the group, if None all will be returned
        :return:
        """
        groups =  self.cloudman.network.security_groups()

        if name is not None:
            for entry in groups:

                if entry['name'] == name:
                    groups = [entry]
                    break

        return self.get_list(
                groups,
                kind="secgroup")

    def list_secgroup_rules(self, name='default'):
        """
        List the named security group

        :param name: The name of the group, if None all will be returned
        :return:
        """
        return self.list_secgroups(name=name)

    def add_secgroup(self, name=None, description=None):
        """
        Adds the
        :param name: Name of the group
        :param description: The desciption
        :return:
        """
        if self.cloudman:
            if description is None:
                description = name
            self.cloudman.create_security_group(name,
                                                description)
        else:
            raise ValueError("cloud not initialized")

    def add_secgroup_rule(self,
                          name=None, #group name
                          port=None,
                          protocol=None,
                          ip_range=None):
        """
        Adds the
        :param name: Name of the group
        :param description: The desciption
        :return:
        """
        if self.cloudman:
            try:
                portmin, portmax = port.split(":")
            except:
                portmin = None
                portmax= None

            self.cloudman.create_security_group_rule(
                name,
                port_range_min=portmin,
                port_range_max=portmax,
                protocol=protocol,
                remote_ip_prefix=ip_range,
                remote_group_id=None,
                direction='ingress',
                ethertype='IPv4',
                project_id=None)

        else:
            raise ValueError("cloud not initialized")


    def remove_secgroup(self, name=None):
        """
        Delete the names security group

        :param name: The name
        :return:
        """
        if self.cloudman:
            self.cloudman.delete_security_group(name)
            g = self.list_secgroups(name=name)
            return len(g) == 0
        else:
            raise ValueError("cloud not initialized")

    def upload_secgroup(self, name=None):

        cgroups = self.list_secgroups(name)
        group_exists = False
        if len(cgroups) > 0:
            print("Warning group already exists")
            group_exists = True

        groups = Secgroup().list()
        rules = SecgroupRule().list()

        #pprint (rules)
        data = {}
        for rule in rules:
            data[rule['name']] = rule

        pprint (groups)

        for group in groups:
            if group['name'] == name:
                break
        print("upload group:", name)

        if not group_exists:
            self.add_secgroup(name=name, description=group['description'])

            for r in group['rules']:
                found = data[r]
                print ("    ", "rule:", found['name'])
                self.add_secgroup_rule(
                                  name=name,
                                  port=found["ports"],
                                  protocol=found["protocol"],
                                  ip_range=found["ip_range"])

        else:

            for r in group['rules']:
                found = data[r]
                print ("    ", "rule:", found['name'])
                self.add_rules_to_secgroup(
                                           name=name,
                                           rules=[found['name']])

    # ok
    def add_rules_to_secgroup(self, name=None, rules=None):
        if name is None and rules is None:
            raise ValueError("name or rules are None")

        cgroups = self.list_secgroups(name)
        if len(cgroups) == 0:
            raise ValueError("group does not exist")

        groups = DictList(Secgroup().list())
        rules_details = DictList(SecgroupRule().list())

        try:
            group = groups[name]
        except:
            raise ValueError("group does not exist")


        for rule in rules:
            try:
                found = rules_details[rule]
                self.add_secgroup_rule(name=name,
                                       port=found["ports"],
                                       protocol=found["protocol"],
                                       ip_range=found["ip_range"])
            except:
                ValueError("rule can not be found")


    # not tested
    def remove_rules_from_secgroup(self, name=None, rules=None):

        if name is None and rules is None:
            raise ValueError("name or rules are None")

        cgroups = self.list_secgroups(name)
        if len(cgroups) == 0:
            raise ValueError("group does not exist")

        groups = DictList(Secgroup().list())
        rules_details = DictList(SecgroupRule().list())

        try:
            group = groups[name]
        except:
            raise ValueError("group does not exist")

        for rule in rules:
            try:
                found = rules_details[rule]
                try:
                    pmin, pmax = rules['ports'].split(":")
                except:
                    pmin = None
                    pmax = None

            except:
                ValueError("rule can not be found")

            for r in cgroups['security_group_rules']:

                test = \
                    r["port_range_max"] == pmin and \
                    r["port_range_min"] == pmax and \
                    r["protocol"] == found["protocol"] and \
                    r["remote_ip_prefix"] == found["ports"]
                    #r["direction"] == "egress" \
                    #r["ethertype"] == "IPv6" \
                    #r["id"] == "1234e4e3-ba72-4e33-9844-..." \
                    # r["remote_group_id"]] == null \
                    #r["tenant_id"]] == "CH-12345"

                if test:
                    id = r["security_group_id"]
                    self.cloudman.delete_security_group_rule(id)


    def get_list(self, d, kind=None, debug=False, **kwargs):
        """
        Lists the dict d on the cloud
        :return: dict or libcloud object
        """

        if self.cloudman:
            entries = []
            for entry in d:
                entries.append(dict(entry))
            if debug:
                pprint(entries)

            return self.update_dict(entries, kind=kind)
        return None

    def images(self, **kwargs):
        """
        Lists the images on the cloud
        :return: dict or libcloud object
        """
        return self.get_list(self.cloudman.compute.images(),
                             kind="image")

    def image(self, name=None):
        """
        Gets the image with a given nmae
        :param name: The name of the image
        :return: the dict of the image
        """
        return self.find(self.images(**kwargs), name=name)

    def flavors(self):
        """
        Lists the flavors on the cloud

        :return: dict of flavors
        """
        return self.get_list(self.cloudman.compute.flavors(),
                             kind="flavor")

    def flavor(self, name=None):
        """
        Gest the flavor with a given name
        :param name: The name of the flavor
        :return: The dict of the flavor
        """
        return self.find(self.flavors(), name=name)

    def start(self, name=None):
        """
        Start a server with the given names

        :param names: A list of node names
        :return:  A list of dict representing the nodes
        """
        r = self.cloudman.suspend_server(name)

    def stop(self, name=None):
        """
        Stop a list of nodes with the given names

        :param names: A list of node names
        :return:  A list of dict representing the nodes
        """
        r = self.cloudman.suspend_server(name)
        return None

    def info(self, name=None):
        """
        Gets the information of a node with a given name

        :param name: The name of teh virtual machine
        :return: The dict representing the node including updated status
        """
        data = self.cloudman.get_server(name)
        return data

    def suspend(self, name=None):
        """
        NOT YET IMPLEMENTED.

        suspends the node with the given name.

        :param name: the name of the node
        :return: The dict representing the node
        """
        # UNTESTED
        r = self.cloudman.suspend_server(name)
        return None

        """
        raise NotImplementedError

        #
        # BUG THIS CODE DOES NOT WORK
        #
        nodes = self.list()
        for node in nodes:
            if node.name == name:
                r = self.cloudman.ex_stop_node(self._get_node(node.name),
                                               deallocate=False)
                # print(r)
                # BUG THIS IS NOT A DICT
                return(node, name=name)
                self.cloudman.destroy_node(node)

        #
        # should return the updated names dict, e.g. status and so on
        # the above specification is for one name
        #
        
        return None
        """

    def resume(self, name=None):
        """
        resume a stopped node.

        :param name: the name of the node
        :return: the dict of the node
        """
        raise NotImplementedError

    def list(self):
        """
        Lists the vms on the cloud

        :return: dict of vms
        """
        return self.get_list(self.cloudman.compute.servers(), kind="vm")

    def destroy(self, name=None):
        """
        Destroys the node
        :param names: the name of the node
        :return: the dict of the node
        """
        server = self.info(name=name)
        r = self.cloudman.delete_server(name)
        server['status'] = 'deleted'
        servers = [server]
        x = self.get_list(servers, kind="vm")
        return x

    def reboot(self, name=None):
        """
        Reboot a list of nodes with the given names

        :param names: A list of node names
        :return:  A list of dict representing the nodes
        """
        raise NotImplementedError
        return self.cloudman.reboot_node(name)

    def create(self,
               name=None,
               image=None,
               size=None,
               location=None,
               timeout=180,
               key=None,
               secgroup=None,
               ip=None,
               public=True,
               **kwargs):
        """
        creates a named node

        :param name: the name of the node
        :param image: the image used
        :param size: the size of the image
        :param timeout: a timeout in seconds that is invoked in case the image
                        does not boot. The default is set to 3 minutes.
        :param kwargs: additional arguments HEADING(c=".")ed along at time of boot
        :return:
        """
        image_use = None
        flavor_use = None

        # keyname = Config()["cloudmesh"]["profile"]["user"]
        # ex_keyname has to be the registered keypair name in cloud

        """
        https://docs.openstack.org/openstacksdk/latest/user/connection.html#openstack.connection.Connection.create_server

        images = self.images()
        for _image in images:
            if _image.name == image:
                image_use = _image
                break

        flavors = self.flavors()
        for _flavor in flavors:
            if _flavor.name == size:
                flavor_use = _flavor
                break
        """
        size = kwargs['flavor']

        print("Create Server:")
        print ("    Name:  ", name)
        print ("    Image: ", image)
        print ("    Size:  ", size)
        print ("    IP:    ", ip)
        print ("    Public:", public)
        print ("    Key:", key)
        print ("    location:", location)
        print ("    timeout:", timeout)
        print ("    secgroup:", secgroup)


        if not ip and public:
            entry = self.find_available_public_ip()
            ip = entry['floating_ip_address']
            pprint(entry)

        elif ip is not None:
            entry = self.list_public_ips(ip=ip, available=True)
            if len(entry) == 0:
                print("ip not available")
            return None


        banner("IP")
        print(ip)

        try:
            server = self.cloudman.create_server(name,
                                                 flavor=size,
                                                 image=image,
                                                 key_name=key,
                                                 security_groups=[secgroup],
                                                 timeout=timeout,
                                                 #wait=True
                                                 )
            self.cloudman.wait_for_server(server)
            self.cloudman.add_ips_to_server(server, ips=ip)


            # self.cloudman.add_security_group(security_group=secgroup)

            # server = self.cloudman.compute.wait_for_server(server)

            # print("ssh -i {key} root@{ip}".format(
            #    key=PRIVATE_KEYPAIR_FILE,
            #    ip=server.access_ipv4))

        except Exception as e:
            print (e)
            raise NotImplementedError

        return self.update_dict(server, kind="vm")[0]

    #ok
    def list_public_ips(self,
                        ip=None,
                        available=False):

        if ip is not None:
            ips = self.cloudman.list_floating_ips({'floating_ip_address':
                                                       ip})
        else:
            ips = self.cloudman.list_floating_ips()
            if available:
                found = []
                for entry in found:
                    if entry['fixed_ip_address'] is not None:
                        found.append(entry)
                ips = found

        return ips

    #ok
    def delete_public_ip(self, ip=None):
        try:
            if ip is None:
                ips = self.cloudman.list_floating_ips(available=True)
            else:
                ips = self.cloudman.list_floating_ips({'floating_ip_address' :
                                                       ip})
            for _ip in ips:
                r = self.cloudman.delete_floating_ip(_ip['id'])
        except:
            pass

    #ok
    def create_public_ip(self):
        return self.cloudman.create_floating_ip()

    #ok
    def find_available_public_ip(self):
        return self.cloudman.available_floating_ip()

    #broken
    def attach_publicIP(self, node, ip):
        raise NotImplementedError

    #broken
    def detach_publicIP(self, node, ip):
        raise NotImplementedError

    def rename(self, name=None, destination=None):
        """
        rename a node. NOT YET IMPLEMENTED.

        :param destinat
        :param name: the current name
        :return: the dict with the new name
        """
        raise NotImplementedError
        return None

    def ssh(self, name=None, command=None):
        raise NotImplementedError
        key = self.key_path.replace(".pub", "")
        nodes = self.list()
        for node in nodes:
            if node.name == name:
                break
        #
        # bug testnode is not defined
        #
        pubip = self.testnode.public_ips[0]
        location = self.user + '@' + pubip
        cmd = ['ssh',
               "-o", "StrictHostKeyChecking=no",
               "-o", "UserKnownHostsFile=/dev/null",
               '-i', key, location, command]
        VERBOSE(" ".join(cmd))

        ssh = subprocess.Popen(cmd,
                               shell=False,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        result = ssh.stdout.readlines()
        if result == []:
            error = ssh.stderr.readlines()
            print("ERROR: %s" % error)
        else:
            print("RESULT:")
            for line in result:
                line = line.decode("utf-8")
                print(line.strip("\n"))
