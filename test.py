import unittest
import docker_cli
from pathlib import Path


class CommandFormulationTest(unittest.TestCase):
    def test_bwa_basic(self):
        here = Path().resolve()

        self.assertListEqual(
            docker_cli.formulate_command(['lh3lh3/bwa', 'index', 'wildtype.fna'], no_rm=True, random_tempdir=False),
            ['docker', 'run', '-v', f'{here}/wildtype.fna:/tmp/wildtype.fna', 'lh3lh3/bwa', 'index', f'/tmp/wildtype.fna']
        )

    def test_bwa_parent(self):
        here = Path().resolve()

        self.assertListEqual(
            docker_cli.formulate_command(['lh3lh3/bwa', 'index', 'wildtype.fna'], no_rm=True, random_tempdir=False, mount_parent=True),
            ['docker', 'run', '-v', f'{here}:/tmp/{here.name}', 'lh3lh3/bwa', 'index', f'/tmp/{here.name}/wildtype.fna']
        )

