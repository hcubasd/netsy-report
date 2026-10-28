"""Protect publication gates, especially accidental template publication."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('project', Path(__file__).parents[1] / 'scripts/project.py')
project = importlib.util.module_from_spec(spec)
spec.loader.exec_module(project)


class PublicationChecks(unittest.TestCase):
    def test_overfull_horizontal_and_vertical(self):
        for text in (r'Overfull \hbox (12.0pt too wide)', r'Overfull \vbox (3.0pt too high)'):
            self.assertTrue(project.log_problems(text))

    def test_unresolved_bibliography_and_references(self):
        for text in ("LaTeX Warning: Citation 'missing' on page 1 undefined",
                     'LaTeX Warning: There were undefined references.',
                     'Package biblatex Warning: Please (re)run Biber on the file:',
                     'LaTeX Warning: Label `a` multiply defined.',
                     'LaTeX Warning: There were multiply-defined labels.',
                     'LaTeX Warning: Rerun to get cross-references right.'):
            self.assertTrue(project.log_problems(text), text)

    def test_underfull_is_informational(self):
        self.assertEqual(project.log_problems(r'Underfull \hbox (badness 10000)'), [])

    def test_clean_log(self):
        self.assertEqual(project.log_problems('Output written on main.pdf (1 page).'), [])

    def test_template_cannot_publish_even_if_enabled(self):
        for enabled in (False, True):
            with self.assertRaises(ValueError):
                project.release_tag('v0.1.0', {'major': 0, 'publish_pdf': enabled})

    def test_publication_must_opt_in(self):
        with self.assertRaises(ValueError):
            project.release_tag('v1.0.0', {'major': 1, 'publish_pdf': False})

    def test_tag_major_and_format(self):
        config = {'major': 1, 'publish_pdf': True}
        for tag in ('v2.0.0', 'v1.0', 'v1.00.0', 'v1.0.0-extra', 'v1.0.0\n'):
            with self.assertRaises(ValueError):
                project.release_tag(tag, config)
        self.assertEqual(project.release_tag('v1.2.3', config), 'v1.2.3')


if __name__ == '__main__':
    unittest.main()
