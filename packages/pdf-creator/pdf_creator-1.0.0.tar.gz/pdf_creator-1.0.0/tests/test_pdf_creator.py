import unittest
from pdf_creator.creator import pdf_creator
import os


class test_pdf_creator(unittest.TestCase):

    def test_save(self):
        test = pdf_creator('new.pdf')
        test.save()
        self.assertTrue(os.path.exists('new.pdf'))
        os.remove('new.pdf')

    def test_table(self):
        test = pdf_creator('new.pdf')
        data = [
            ['a', 'b'],
            ['a2', 'b2']
        ]
        test.table(data, 100, 100)
        test.save()
        self.assertTrue(os.path.exists('new.pdf'))
        os.remove('new.pdf')

    def test_text(self):
        test = pdf_creator('new.pdf')
        test.text('test', 100, 100)
        test.save()
        self.assertTrue(os.path.exists('new.pdf'))
        os.remove('new.pdf')

    def test_image(self):
        test = pdf_creator('new.pdf')
        test.image('tests/test.jpg', 100, 100)
        test.save()
        self.assertTrue(os.path.exists('new.pdf'))
        os.remove('new.pdf')
