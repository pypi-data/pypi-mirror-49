# coding=utf-8
"""Tests that CRUD remotes."""
from random import choice
import unittest

from requests.exceptions import HTTPError

from pulp_smash import api, config, utils
from pulp_smash.pulp3.constants import ON_DEMAND_DOWNLOAD_POLICIES

from pulp_file.tests.functional.constants import (
    FILE_FIXTURE_MANIFEST_URL,
    FILE2_FIXTURE_MANIFEST_URL,
    FILE_REMOTE_PATH,
)
from pulp_file.tests.functional.utils import skip_if, gen_file_remote
from pulp_file.tests.functional.utils import set_up_module as setUpModule  # noqa:F401


class CRUDRemotesTestCase(unittest.TestCase):
    """CRUD remotes."""

    @classmethod
    def setUpClass(cls):
        """Create class-wide variables."""
        cls.cfg = config.get_config()
        cls.client = api.Client(cls.cfg, api.json_handler)

    def test_01_create_remote(self):
        """Create a remote."""
        body = _gen_verbose_remote()
        type(self).remote = self.client.post(FILE_REMOTE_PATH, body)
        for key in ("username", "password"):
            del body[key]
        for key, val in body.items():
            with self.subTest(key=key):
                self.assertEqual(self.remote[key], val)

    @skip_if(bool, "remote", False)
    def test_02_create_same_name(self):
        """Try to create a second remote with an identical name.

        See: `Pulp Smash #1055
        <https://github.com/PulpQE/pulp-smash/issues/1055>`_.
        """
        body = gen_file_remote()
        body["name"] = self.remote["name"]
        with self.assertRaises(HTTPError):
            self.client.post(FILE_REMOTE_PATH, body)

    @skip_if(bool, "remote", False)
    def test_02_read_remote(self):
        """Read a remote by its href."""
        remote = self.client.get(self.remote["_href"])
        for key, val in self.remote.items():
            with self.subTest(key=key):
                self.assertEqual(remote[key], val)

    @skip_if(bool, "remote", False)
    def test_02_read_remotes(self):
        """Read a remote by its name."""
        page = self.client.get(FILE_REMOTE_PATH, params={"name": self.remote["name"]})
        self.assertEqual(len(page["results"]), 1)
        for key, val in self.remote.items():
            with self.subTest(key=key):
                self.assertEqual(page["results"][0][key], val)

    @skip_if(bool, "remote", False)
    def test_03_partially_update(self):
        """Update a remote using HTTP PATCH."""
        body = _gen_verbose_remote()
        self.client.patch(self.remote["_href"], body)
        for key in ("username", "password"):
            del body[key]
        type(self).remote = self.client.get(self.remote["_href"])
        for key, val in body.items():
            with self.subTest(key=key):
                self.assertEqual(self.remote[key], val)

    @skip_if(bool, "remote", False)
    def test_04_fully_update(self):
        """Update a remote using HTTP PUT."""
        body = _gen_verbose_remote()
        self.client.put(self.remote["_href"], body)
        for key in ("username", "password"):
            del body[key]
        type(self).remote = self.client.get(self.remote["_href"])
        for key, val in body.items():
            with self.subTest(key=key):
                self.assertEqual(self.remote[key], val)

    @skip_if(bool, "remote", False)
    def test_05_delete(self):
        """Delete a remote."""
        self.client.delete(self.remote["_href"])
        with self.assertRaises(HTTPError):
            self.client.get(self.remote["_href"])

    def test_negative_create_file_remote_with_invalid_parameter(self):
        """Attempt to create file remote passing invalid parameter.

        Assert response returns an error 400 including ["Unexpected field"].

        This test targets the following issue:

        * `Pulp Smash #1085 <https://github.com/PulpQE/pulp-smash/issues/1085>`_
        """
        response = api.Client(self.cfg, api.echo_handler).post(
            FILE_REMOTE_PATH, gen_file_remote(foo="bar")
        )
        assert response.status_code == 400
        assert response.json()["foo"] == ["Unexpected field"]


class CreateRemoteNoURLTestCase(unittest.TestCase):
    """Verify whether is possible to create a remote without a URL."""

    def test_all(self):
        """Verify whether is possible to create a remote without a URL.

        This test targets the following issues:

        * `Pulp #3395 <https://pulp.plan.io/issues/3395>`_
        * `Pulp Smash #984 <https://github.com/PulpQE/pulp-smash/issues/984>`_
        """
        body = gen_file_remote()
        del body["url"]
        with self.assertRaises(HTTPError):
            api.Client(config.get_config()).post(FILE_REMOTE_PATH, body)


class RemoteDownloadPolicyTestCase(unittest.TestCase):
    """Verify download policy behavior for valid and invalid values.

    In Pulp 3, there are are different download policies.

    This test targets the following testing scenarios:

    1. Creating a remote without a download policy.
       Verify the creation is successful and immediate it is policy applied.
    2. Change the remote policy from default.
       Verify the change is successful.
    3. Attempt to change the remote policy to an invalid string.
       Verify an HTTPError is given for the invalid policy as well
       as the policy remaining unchanged.

    For more information on the remote policies, see the Pulp3
    API on an installed server:

    * /pulp/api/v3/docs/#operation`

    This test targets the following issues:

    * `Pulp #4420 <https://pulp.plan.io/issues/4420>`_
    * `Pulp #3763 <https://pulp.plan.io/issues/3763>`_
    """

    @classmethod
    def setUpClass(cls):
        """Create class-wide variables."""
        cls.cfg = config.get_config()
        cls.client = api.Client(cls.cfg, api.json_handler)
        cls.remote = {}
        cls.body = _gen_verbose_remote()

    @classmethod
    def tearDownClass(cls):
        """Clean class-wide variable."""
        cls.client.delete(cls.remote["_href"])

    def test_01_no_defined_policy(self):
        """Verify the default policy `immediate`.

        When no policy is defined, the default policy of `immediate`
        is applied.
        """
        del self.body["policy"]
        self.remote.update(self.client.post(FILE_REMOTE_PATH, self.body))
        self.assertEqual(self.remote["policy"], "immediate", self.remote)

    @skip_if(bool, "remote", False)
    def test_02_change_policy(self):
        """Verify ability to change policy to value other than the default.

        Update the remote policy to a valid value other than `immedaite`
        and verify the new set value.
        """
        changed_policy = choice(
            [item for item in ON_DEMAND_DOWNLOAD_POLICIES if item != "immediate"]
        )
        self.client.patch(self.remote["_href"], {"policy": changed_policy})
        self.remote.update(self.client.get(self.remote["_href"]))
        self.assertEqual(self.remote["policy"], changed_policy, self.remote)

    @skip_if(bool, "remote", False)
    def test_03_invalid_policy(self):
        """Verify an invalid policy does not update the remote policy.

        Get the current remote policy.
        Attempt to update the remote policy to an invalid value.
        Verify the policy remains the same.
        """
        remote = self.client.get(self.remote["_href"])
        with self.assertRaises(HTTPError):
            self.client.patch(self.remote["_href"], {"policy": utils.uuid4()})
        self.remote.update(self.client.get(self.remote["_href"]))
        self.assertEqual(remote["policy"], self.remote["policy"], self.remote)


def _gen_verbose_remote():
    """Return a semi-random dict for use in defining a remote.

    For most tests, it's desirable to create remotes with as few attributes
    as possible, so that the tests can specifically target and attempt to break
    specific features. This module specifically targets remotes, so it makes
    sense to provide as many attributes as possible.

    Note that 'username' and 'password' are write-only attributes.
    """
    attrs = gen_file_remote(url=choice((FILE_FIXTURE_MANIFEST_URL, FILE2_FIXTURE_MANIFEST_URL)))
    attrs.update(
        {
            "password": utils.uuid4(),
            "username": utils.uuid4(),
            "policy": choice(ON_DEMAND_DOWNLOAD_POLICIES),
        }
    )
    return attrs
