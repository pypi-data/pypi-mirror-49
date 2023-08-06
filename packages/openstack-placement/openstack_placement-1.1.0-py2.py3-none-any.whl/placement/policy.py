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
"""Policy Enforcement for placement API."""

from oslo_config import cfg
from oslo_log import log as logging
from oslo_policy import policy
from oslo_utils import excutils

from placement import exception
from placement import policies


LOG = logging.getLogger(__name__)
_ENFORCER = None


def reset():
    """Used to reset the global _ENFORCER between test runs."""
    global _ENFORCER
    if _ENFORCER:
        _ENFORCER.clear()
        _ENFORCER = None


def init(conf):
    """Init an Enforcer class. Sets the _ENFORCER global."""
    global _ENFORCER
    if not _ENFORCER:
        # NOTE(mriedem): We have to explicitly pass in the
        # [placement]/policy_file path because otherwise oslo_policy defaults
        # to read the policy file from config option [oslo_policy]/policy_file
        # which is used by nova. In other words, to have separate policy files
        # for placement and nova, we have to use separate policy_file options.
        _enforcer = policy.Enforcer(
            conf, policy_file=conf.placement.policy_file)
        _enforcer.register_defaults(policies.list_rules())
        _enforcer.load_rules()
        _ENFORCER = _enforcer


def get_enforcer():
    # This method is used by oslopolicy CLI scripts in order to generate policy
    # files from overrides on disk and defaults in code. We can just pass an
    # empty list and let oslo do the config lifting for us.
    cfg.CONF([], project='placement')
    return _get_enforcer(cfg.CONF)


def _get_enforcer(conf):
    init(conf)
    return _ENFORCER


def authorize(context, action, target, do_raise=True):
    """Verifies that the action is valid on the target in this context.

    :param context: instance of placement.context.RequestContext
    :param action: string representing the action to be checked
        this should be colon separated for clarity, i.e.
        ``placement:resource_providers:list``
    :param target: dictionary representing the object of the action;
        for object creation this should be a dictionary representing the
        owner of the object e.g. ``{'project_id': context.project_id}``.
    :param do_raise: if True (the default), raises PolicyNotAuthorized;
        if False, returns False
    :raises placement.exception.PolicyNotAuthorized: if verification fails and
        do_raise is True.
    :returns: non-False value (not necessarily "True") if authorized, and the
        exact value False if not authorized and do_raise is False.
    """
    credentials = context.to_policy_values()
    try:
        # NOTE(mriedem): The "action" kwarg is for the PolicyNotAuthorized exc.
        return _ENFORCER.authorize(
            action, target, credentials, do_raise=do_raise,
            exc=exception.PolicyNotAuthorized, action=action)
    except policy.PolicyNotRegistered:
        with excutils.save_and_reraise_exception():
            LOG.exception('Policy not registered')
    except Exception:
        with excutils.save_and_reraise_exception():
            LOG.debug('Policy check for %(action)s failed with credentials '
                      '%(credentials)s',
                      {'action': action, 'credentials': credentials})
