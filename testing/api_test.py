import os
import subprocess
import unittest
import yaml
from commontest import RBBin
from rdiff_backup import Globals


class ApiVersionTest(unittest.TestCase):
    """Test api versioning functionality"""

    def test_runtime_info_calling(self):
        """make sure that the --version output can be read back as YAML when API is 201"""
        output = subprocess.check_output([RBBin, b'--version', b'--api-version', b'201'])
        out_info = yaml.safe_load(output)

        Globals.api_version['actual'] = 201
        info = Globals.get_runtime_info()

        # because the current test will have a different call than rdiff-backup itself
        # we can't compare certain keys
        self.assertIn('exec', out_info)
        self.assertIn('argv', out_info['exec'])
        out_info['exec'].pop('argv')
        info['exec'].pop('argv')
        # info['python']['executable'] could also be different but I think that our test
        # environments make sure that it doesn't happen
        self.assertEqual(info, out_info)

    def test_default_actual_api(self):
        """validate that the default version is the actual one or the one explicitly set"""
        output = subprocess.check_output([RBBin, b'--version', b'--api-version', b'201'])
        api_version = yaml.safe_load(output)['exec']['api_version']
        self.assertEqual(Globals.get_api_version(), api_version['default'])
        api_param = os.fsencode(str(api_version['max']))
        output = subprocess.check_output([RBBin, b'--version', b'--api-version', api_param])
        out_info = yaml.safe_load(output)
        self.assertEqual(out_info['exec']['api_version']['actual'], api_version['max'])


if __name__ == "__main__":
    unittest.main()
