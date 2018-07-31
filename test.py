import unittest
import docker_cli
import os.path


class CommandFormulationTest(unittest.TestCase):
    def test_bwa_basic(self):
        filename = 'wildtype.fna'

        self.assertListEqual(
            docker_cli.formulate_command(['lh3lh3/bwa', 'index', filename], no_rm=True, random_tempdir=False),
            ['docker', 'run', '-v', '{}:/tmp/{}'.format(os.path.abspath(filename), filename), 'lh3lh3/bwa', 'index', f'/tmp/{filename}']
        )
