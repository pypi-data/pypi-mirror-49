#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from __future__ import absolute_import

import os

from gabbi import fixture
import os_resource_classes as orc
from oslo_config import cfg
from oslo_config import fixture as config_fixture
from oslo_log.fixture import logging_error
from oslo_middleware import cors
from oslo_policy import opts as policy_opts
from oslo_utils.fixture import uuidsentinel as uuids
from oslo_utils import uuidutils
from oslotest import output

from placement import conf
from placement import context
from placement import deploy
from placement.objects import project as project_obj
from placement.objects import resource_class as rc_obj
from placement.objects import user as user_obj
from placement import policies
from placement.tests import fixtures
from placement.tests.functional.db import test_base as tb
from placement.tests.functional.fixtures import capture
from placement.tests.unit import policy_fixture


# This global conf is not a global olso_config.cfg.CONF. It's a global
# used locally to work around a limitation in the way that gabbi instantiates
# the WSGI application being tested.
CONF = None


def setup_app():
    global CONF
    return deploy.loadapp(CONF)


class APIFixture(fixture.GabbiFixture):
    """Setup the required backend fixtures for a basic placement service."""

    def start_fixture(self):
        global CONF
        # Set up stderr and stdout captures by directly driving the
        # existing nova fixtures that do that. This captures the
        # output that happens outside individual tests (for
        # example database migrations).
        self.standard_logging_fixture = capture.Logging()
        self.standard_logging_fixture.setUp()
        self.output_stream_fixture = output.CaptureOutput()
        self.output_stream_fixture.setUp()
        self.logging_error_fixture = (
            logging_error.get_logging_handle_error_fixture())
        self.logging_error_fixture.setUp()
        # Filter ignorable warnings during test runs.
        self.warnings_fixture = capture.WarningsFixture()
        self.warnings_fixture.setUp()

        # Do not use global CONF
        self.conf_fixture = config_fixture.Config(cfg.ConfigOpts())
        self.conf_fixture.setUp()
        conf.register_opts(self.conf_fixture.conf)
        self.conf_fixture.config(group='api', auth_strategy='noauth2')

        self.placement_db_fixture = fixtures.Database(
            self.conf_fixture, set_config=True)
        self.placement_db_fixture.setUp()

        self.context = context.RequestContext()

        # Register CORS opts, but do not set config. This has the
        # effect of exercising the "don't use cors" path in
        # deploy.py. Without setting some config the group will not
        # be present.
        self.conf_fixture.register_opts(cors.CORS_OPTS, 'cors')
        # Set default policy opts, otherwise the deploy module can
        # NoSuchOptError.
        policy_opts.set_defaults(self.conf_fixture.conf)

        # Make sure default_config_files is an empty list, not None.
        # If None /etc/placement/placement.conf is read and confuses results.
        self.conf_fixture.conf([], default_config_files=[])

        # Turn on a policy fixture.
        self.policy_fixture = policy_fixture.PolicyFixture(
            self.conf_fixture)
        self.policy_fixture.setUp()

        os.environ['RP_UUID'] = uuidutils.generate_uuid()
        os.environ['RP_NAME'] = uuidutils.generate_uuid()
        os.environ['CUSTOM_RES_CLASS'] = 'CUSTOM_IRON_NFV'
        os.environ['PROJECT_ID'] = uuidutils.generate_uuid()
        os.environ['USER_ID'] = uuidutils.generate_uuid()
        os.environ['PROJECT_ID_ALT'] = uuidutils.generate_uuid()
        os.environ['USER_ID_ALT'] = uuidutils.generate_uuid()
        os.environ['INSTANCE_UUID'] = uuidutils.generate_uuid()
        os.environ['MIGRATION_UUID'] = uuidutils.generate_uuid()
        os.environ['CONSUMER_UUID'] = uuidutils.generate_uuid()
        os.environ['PARENT_PROVIDER_UUID'] = uuidutils.generate_uuid()
        os.environ['ALT_PARENT_PROVIDER_UUID'] = uuidutils.generate_uuid()
        CONF = self.conf_fixture.conf

    def stop_fixture(self):
        global CONF
        self.placement_db_fixture.cleanUp()
        self.warnings_fixture.cleanUp()
        self.output_stream_fixture.cleanUp()
        self.standard_logging_fixture.cleanUp()
        self.logging_error_fixture.cleanUp()
        self.policy_fixture.cleanUp()
        self.conf_fixture.cleanUp()
        CONF = None


class AllocationFixture(APIFixture):
    """An APIFixture that has some pre-made Allocations.

         +----- same user----+          alt_user
         |                   |             |
    +----+----------+ +------+-----+ +-----+---------+
    | consumer1     | | consumer2  | | alt_consumer  |
    |  DISK_GB:1000 | |   VCPU: 6  | |  VCPU: 1      |
    |               | |            | |  DISK_GB:20   |
    +-------------+-+ +------+-----+ +-+-------------+
                  |          |         |
                +-+----------+---------+-+
                |     rp                 |
                |      VCPU: 10          |
                |      DISK_GB:2048      |
                +------------------------+
    """
    def start_fixture(self):
        super(AllocationFixture, self).start_fixture()

        # For use creating and querying allocations/usages
        os.environ['ALT_USER_ID'] = uuidutils.generate_uuid()
        project_id = os.environ['PROJECT_ID']
        user_id = os.environ['USER_ID']
        alt_user_id = os.environ['ALT_USER_ID']

        user = user_obj.User(self.context, external_id=user_id)
        user.create()
        alt_user = user_obj.User(self.context, external_id=alt_user_id)
        alt_user.create()
        project = project_obj.Project(self.context, external_id=project_id)
        project.create()

        # Stealing from the super
        rp_name = os.environ['RP_NAME']
        rp_uuid = os.environ['RP_UUID']
        # Create the rp with VCPU and DISK_GB inventory
        rp = tb.create_provider(self.context, rp_name, uuid=rp_uuid)
        tb.add_inventory(rp, 'DISK_GB', 2048,
                         step_size=10, min_unit=10, max_unit=1000)
        tb.add_inventory(rp, 'VCPU', 10, max_unit=10)

        # Create a first consumer for the DISK_GB allocations
        consumer1 = tb.ensure_consumer(self.context, user, project)
        tb.set_allocation(self.context, rp, consumer1, {'DISK_GB': 1000})
        os.environ['CONSUMER_0'] = consumer1.uuid

        # Create a second consumer for the VCPU allocations
        consumer2 = tb.ensure_consumer(self.context, user, project)
        tb.set_allocation(self.context, rp, consumer2, {'VCPU': 6})
        os.environ['CONSUMER_ID'] = consumer2.uuid

        # Create a consumer object for a different user
        alt_consumer = tb.ensure_consumer(self.context, alt_user, project)
        os.environ['ALT_CONSUMER_ID'] = alt_consumer.uuid

        # Create a couple of allocations for a different user.
        tb.set_allocation(self.context, rp, alt_consumer,
                          {'DISK_GB': 20, 'VCPU': 1})

        # The ALT_RP_XXX variables are for a resource provider that has
        # not been created in the Allocation fixture
        os.environ['ALT_RP_UUID'] = uuidutils.generate_uuid()
        os.environ['ALT_RP_NAME'] = uuidutils.generate_uuid()


class SharedStorageFixture(APIFixture):
    """An APIFixture that has two compute nodes, one with local storage and one
    without, both associated by aggregate to two providers of shared storage.
    Both compute nodes have respectively two numa node resource providers, each
    of which has a pf resource provider.

        +-------------------------+        +-------------------------+
        | sharing storage (ss)    |        | sharing storage (ss2)   |
        |  DISK_GB:2000           |----+---|  DISK_GB:2000           |
        |  traits: MISC_SHARES... |    |   |  traits: MISC_SHARES... |
        +-------------------------+    |   +-------------------------+
                                       | aggregate
        +--------------------------+   |   +------------------------+
        | compute node (cn1)       |---+---| compute node (cn2)     |
        |  CPU: 24                 |       |  CPU: 24               |
        |  MEMORY_MB: 128*1024     |       |  MEMORY_MB: 128*1024   |
        |  traits: HW_CPU_X86_SSE, |       |  DISK_GB: 2000         |
        |          HW_CPU_X86_SSE2 |       |                        |
        +--------------------------+       +------------------------+
             |               |                 |                |
        +---------+      +---------+      +---------+      +---------+
        | numa1_1 |      | numa1_2 |      | numa2_1 |      | numa2_2 |
        +---------+      +---------+      +---------+      +---------+
             |                |                |                |
     +---------------++---------------++---------------++----------------+
     | pf1_1         || pf1_2         || pf2_1         || pf2_2          |
     | SRIOV_NET_VF:8|| SRIOV_NET_VF:8|| SRIOV_NET_VF:8|| SRIOV_NET_VF:8 |
     +---------------++---------------++---------------++----------------+
    """

    def start_fixture(self):
        super(SharedStorageFixture, self).start_fixture()

        agg_uuid = uuidutils.generate_uuid()

        cn1 = tb.create_provider(self.context, 'cn1', agg_uuid)
        cn2 = tb.create_provider(self.context, 'cn2', agg_uuid)
        ss = tb.create_provider(self.context, 'ss', agg_uuid)
        ss2 = tb.create_provider(self.context, 'ss2', agg_uuid)

        numa1_1 = tb.create_provider(self.context, 'numa1_1', parent=cn1.uuid)
        numa1_2 = tb.create_provider(self.context, 'numa1_2', parent=cn1.uuid)
        numa2_1 = tb.create_provider(self.context, 'numa2_1', parent=cn2.uuid)
        numa2_2 = tb.create_provider(self.context, 'numa2_2', parent=cn2.uuid)

        pf1_1 = tb.create_provider(self.context, 'pf1_1', parent=numa1_1.uuid)
        pf1_2 = tb.create_provider(self.context, 'pf1_2', parent=numa1_2.uuid)
        pf2_1 = tb.create_provider(self.context, 'pf2_1', parent=numa2_1.uuid)
        pf2_2 = tb.create_provider(self.context, 'pf2_2', parent=numa2_2.uuid)

        os.environ['AGG_UUID'] = agg_uuid

        os.environ['CN1_UUID'] = cn1.uuid
        os.environ['CN2_UUID'] = cn2.uuid
        os.environ['SS_UUID'] = ss.uuid
        os.environ['SS2_UUID'] = ss2.uuid

        os.environ['NUMA1_1_UUID'] = numa1_1.uuid
        os.environ['NUMA1_2_UUID'] = numa1_2.uuid
        os.environ['NUMA2_1_UUID'] = numa2_1.uuid
        os.environ['NUMA2_2_UUID'] = numa2_2.uuid

        os.environ['PF1_1_UUID'] = pf1_1.uuid
        os.environ['PF1_2_UUID'] = pf1_2.uuid
        os.environ['PF2_1_UUID'] = pf2_1.uuid
        os.environ['PF2_2_UUID'] = pf2_2.uuid

        # Populate compute node inventory for VCPU and RAM
        for cn in (cn1, cn2):
            tb.add_inventory(cn, orc.VCPU, 24,
                             allocation_ratio=16.0)
            tb.add_inventory(cn, orc.MEMORY_MB, 128 * 1024,
                             allocation_ratio=1.5)

        tb.set_traits(cn1, 'HW_CPU_X86_SSE', 'HW_CPU_X86_SSE2')
        tb.add_inventory(cn2, orc.DISK_GB, 2000,
                         reserved=100, allocation_ratio=1.0)

        for shared in (ss, ss2):
            # Populate shared storage provider with DISK_GB inventory and
            # mark it shared among any provider associated via aggregate
            tb.add_inventory(shared, orc.DISK_GB, 2000,
                             reserved=100, allocation_ratio=1.0)
            tb.set_traits(shared, 'MISC_SHARES_VIA_AGGREGATE')

        # Populate PF inventory for VF
        for pf in (pf1_1, pf1_2, pf2_1, pf2_2):
            tb.add_inventory(pf, orc.SRIOV_NET_VF,
                             8, allocation_ratio=1.0)


class NUMAAggregateFixture(APIFixture):
    """An APIFixture that has two compute nodes without a resource themselves.
    They are associated by aggregate to a provider of shared storage and both
    compute nodes have two numa node resource providers with CPUs. One of the
    numa node is associated to another sharing storage by a different
    aggregate.

                          +-----------------------+
                          | sharing storage (ss1) |
                          |   DISK_GB:2000        |
                          |   agg: [aggA]         |
                          +-----------+-----------+
                                      |
                      +---------------+----------------+
      +---------------|--------------+  +--------------|--------------+
      | +-------------+------------+ |  | +------------+------------+ |
      | | compute node (cn1)       | |  | |compute node (cn2)       | |
      | |   agg: [aggA]            | |  | |  agg: [aggA, aggB]      | |
      | +-----+-------------+------+ |  | +----+-------------+------+ |
      |       | nested      | nested |  |      | nested      | nested |
      | +-----+------+ +----+------+ |  | +----+------+ +----+------+ |
      | | numa1_1    | | numa1_2   | |  | | numa2_1   | | numa2_2   | |
      | |  CPU: 24   | |   CPU: 24 | |  | |   CPU: 24 | |   CPU: 24 | |
      | |  agg:[aggC]| |           | |  | |           | |           | |
      | +-----+------+ +-----------+ |  | +-----------+ +-----------+ |
      +-------|----------------------+  +-----------------------------+
              | aggC
        +-----+-----------------+
        | sharing storage (ss2) |
        |   DISK_GB:2000        |
        |   agg: [aggC]         |
        +-----------------------+
    """

    def start_fixture(self):
        super(NUMAAggregateFixture, self).start_fixture()

        aggA_uuid = uuidutils.generate_uuid()
        aggB_uuid = uuidutils.generate_uuid()
        aggC_uuid = uuidutils.generate_uuid()

        cn1 = tb.create_provider(self.context, 'cn1', aggA_uuid)
        cn2 = tb.create_provider(self.context, 'cn2', aggA_uuid, aggB_uuid)
        ss1 = tb.create_provider(self.context, 'ss1', aggA_uuid)
        ss2 = tb.create_provider(self.context, 'ss2', aggC_uuid)

        numa1_1 = tb.create_provider(
            self.context, 'numa1_1', aggC_uuid, parent=cn1.uuid)
        numa1_2 = tb.create_provider(self.context, 'numa1_2', parent=cn1.uuid)
        numa2_1 = tb.create_provider(self.context, 'numa2_1', parent=cn2.uuid)
        numa2_2 = tb.create_provider(self.context, 'numa2_2', parent=cn2.uuid)

        os.environ['AGGA_UUID'] = aggA_uuid
        os.environ['AGGB_UUID'] = aggB_uuid
        os.environ['AGGC_UUID'] = aggC_uuid

        os.environ['CN1_UUID'] = cn1.uuid
        os.environ['CN2_UUID'] = cn2.uuid
        os.environ['SS1_UUID'] = ss1.uuid
        os.environ['SS2_UUID'] = ss2.uuid

        os.environ['NUMA1_1_UUID'] = numa1_1.uuid
        os.environ['NUMA1_2_UUID'] = numa1_2.uuid
        os.environ['NUMA2_1_UUID'] = numa2_1.uuid
        os.environ['NUMA2_2_UUID'] = numa2_2.uuid

        # Populate compute node inventory for VCPU and RAM
        for numa in (numa1_1, numa1_2, numa2_1, numa2_2):
            tb.add_inventory(numa, orc.VCPU, 24,
                             allocation_ratio=16.0)

        # Populate shared storage provider with DISK_GB inventory and
        # mark it shared among any provider associated via aggregate
        for ss in (ss1, ss2):
            tb.add_inventory(ss, orc.DISK_GB, 2000,
                             reserved=100, allocation_ratio=1.0)
            tb.set_traits(ss, 'MISC_SHARES_VIA_AGGREGATE')


class NonSharedStorageFixture(APIFixture):
    """An APIFixture that has two compute nodes with local storage that do not
    use shared storage.
    """
    def start_fixture(self):
        super(NonSharedStorageFixture, self).start_fixture()

        aggA_uuid = uuidutils.generate_uuid()
        aggB_uuid = uuidutils.generate_uuid()
        aggC_uuid = uuidutils.generate_uuid()
        os.environ['AGGA_UUID'] = aggA_uuid
        os.environ['AGGB_UUID'] = aggB_uuid
        os.environ['AGGC_UUID'] = aggC_uuid

        cn1 = tb.create_provider(self.context, 'cn1')
        cn2 = tb.create_provider(self.context, 'cn2')

        os.environ['CN1_UUID'] = cn1.uuid
        os.environ['CN2_UUID'] = cn2.uuid

        # Populate compute node inventory for VCPU, RAM and DISK
        for cn in (cn1, cn2):
            tb.add_inventory(cn, 'VCPU', 24)
            tb.add_inventory(cn, 'MEMORY_MB', 128 * 1024)
            tb.add_inventory(cn, 'DISK_GB', 2000)


class CORSFixture(APIFixture):
    """An APIFixture that turns on CORS."""

    def start_fixture(self):
        super(CORSFixture, self).start_fixture()
        # NOTE(cdent): If we remove this override, then the cors
        # group ends up not existing in the conf, so when deploy.py
        # wants to load the CORS middleware, it will not.
        self.conf_fixture.config(
            group='cors',
            allowed_origin='http://valid.example.com')


class GranularFixture(APIFixture):
    """An APIFixture that sets up the following provider environment for
    testing granular resource requests.

+========================++========================++========================+
|cn_left                 ||cn_middle               ||cn_right                |
|VCPU: 8                 ||VCPU: 8                 ||VCPU: 8                 |
|MEMORY_MB: 4096         ||MEMORY_MB: 4096         ||MEMORY_MB: 4096         |
|DISK_GB: 500            ||SRIOV_NET_VF: 8         ||DISK_GB: 500            |
|VGPU: 8                 ||CUSTOM_NET_MBPS: 4000   ||VGPU: 8                 |
|SRIOV_NET_VF: 8         ||traits: HW_CPU_X86_AVX, ||  - max_unit: 2         |
|CUSTOM_NET_MBPS: 4000   ||        HW_CPU_X86_AVX2,||traits: HW_CPU_X86_MMX, |
|traits: HW_CPU_X86_AVX, ||        HW_CPU_X86_SSE, ||        HW_GPU_API_DXVA,|
|        HW_CPU_X86_AVX2,||        HW_NIC_ACCEL_TLS||        CUSTOM_DISK_SSD,|
|        HW_GPU_API_DXVA,|+=+=====+================++==+========+============+
|        HW_NIC_DCB_PFC, |  :     :                    :        : a
|        CUSTOM_FOO      +..+     +--------------------+        : g
+========================+  : a   :                             : g
                            : g   :                             : C
+========================+  : g   :             +===============+======+
|shr_disk_1              |  : A   :             |shr_net               |
|DISK_GB: 1000           +..+     :             |SRIOV_NET_VF: 16      |
|traits: CUSTOM_DISK_SSD,|  :     : a           |CUSTOM_NET_MBPS: 40000|
|  MISC_SHARES_VIA_AGG...|  :     : g           |traits: MISC_SHARES...|
+========================+  :     : g           +======================+
+=======================+   :     : B
|shr_disk_2             +...+     :
|DISK_GB: 1000          |         :
|traits: MISC_SHARES... +.........+
+=======================+
    """
    def start_fixture(self):
        super(GranularFixture, self).start_fixture()

        rc_obj.ResourceClass(
            context=self.context, name='CUSTOM_NET_MBPS').create()

        os.environ['AGGA'] = uuids.aggA
        os.environ['AGGB'] = uuids.aggB
        os.environ['AGGC'] = uuids.aggC

        cn_left = tb.create_provider(self.context, 'cn_left', uuids.aggA)
        os.environ['CN_LEFT'] = cn_left.uuid
        tb.add_inventory(cn_left, 'VCPU', 8)
        tb.add_inventory(cn_left, 'MEMORY_MB', 4096)
        tb.add_inventory(cn_left, 'DISK_GB', 500)
        tb.add_inventory(cn_left, 'VGPU', 8)
        tb.add_inventory(cn_left, 'SRIOV_NET_VF', 8)
        tb.add_inventory(cn_left, 'CUSTOM_NET_MBPS', 4000)
        tb.set_traits(cn_left, 'HW_CPU_X86_AVX', 'HW_CPU_X86_AVX2',
                      'HW_GPU_API_DXVA', 'HW_NIC_DCB_PFC', 'CUSTOM_FOO')

        cn_middle = tb.create_provider(
            self.context, 'cn_middle', uuids.aggA, uuids.aggB)
        os.environ['CN_MIDDLE'] = cn_middle.uuid
        tb.add_inventory(cn_middle, 'VCPU', 8)
        tb.add_inventory(cn_middle, 'MEMORY_MB', 4096)
        tb.add_inventory(cn_middle, 'SRIOV_NET_VF', 8)
        tb.add_inventory(cn_middle, 'CUSTOM_NET_MBPS', 4000)
        tb.set_traits(cn_middle, 'HW_CPU_X86_AVX', 'HW_CPU_X86_AVX2',
                      'HW_CPU_X86_SSE', 'HW_NIC_ACCEL_TLS')

        cn_right = tb.create_provider(
            self.context, 'cn_right', uuids.aggB, uuids.aggC)
        os.environ['CN_RIGHT'] = cn_right.uuid
        tb.add_inventory(cn_right, 'VCPU', 8)
        tb.add_inventory(cn_right, 'MEMORY_MB', 4096)
        tb.add_inventory(cn_right, 'DISK_GB', 500)
        tb.add_inventory(cn_right, 'VGPU', 8, max_unit=2)
        tb.set_traits(cn_right, 'HW_CPU_X86_MMX', 'HW_GPU_API_DXVA',
                      'CUSTOM_DISK_SSD')

        shr_disk_1 = tb.create_provider(self.context, 'shr_disk_1', uuids.aggA)
        os.environ['SHR_DISK_1'] = shr_disk_1.uuid
        tb.add_inventory(shr_disk_1, 'DISK_GB', 1000)
        tb.set_traits(shr_disk_1, 'MISC_SHARES_VIA_AGGREGATE',
                      'CUSTOM_DISK_SSD')

        shr_disk_2 = tb.create_provider(
            self.context, 'shr_disk_2', uuids.aggA, uuids.aggB)
        os.environ['SHR_DISK_2'] = shr_disk_2.uuid
        tb.add_inventory(shr_disk_2, 'DISK_GB', 1000)
        tb.set_traits(shr_disk_2, 'MISC_SHARES_VIA_AGGREGATE')

        shr_net = tb.create_provider(self.context, 'shr_net', uuids.aggC)
        os.environ['SHR_NET'] = shr_net.uuid
        tb.add_inventory(shr_net, 'SRIOV_NET_VF', 16)
        tb.add_inventory(shr_net, 'CUSTOM_NET_MBPS', 40000)
        tb.set_traits(shr_net, 'MISC_SHARES_VIA_AGGREGATE')


class OpenPolicyFixture(APIFixture):
    """An APIFixture that changes all policy rules to allow non-admins."""

    def start_fixture(self):
        super(OpenPolicyFixture, self).start_fixture()
        # Get all of the registered rules and set them to '@' to allow any
        # user to have access. The nova policy "admin_or_owner" concept does
        # not really apply to most of placement resources since they do not
        # have a user_id/project_id attribute.
        rules = {}
        for rule in policies.list_rules():
            name = rule.name
            # Ignore "base" rules for role:admin.
            if name in ['placement', 'admin_api']:
                continue
            rules[name] = '@'
        self.policy_fixture.set_rules(rules)

    def stop_fixture(self):
        super(OpenPolicyFixture, self).stop_fixture()
