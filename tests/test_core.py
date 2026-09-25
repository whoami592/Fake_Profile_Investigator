import copy
import tempfile
import unittest
from pathlib import Path
from PIL import Image
from core import compare, load_case, save_case, report_html, similarity

class Tests(unittest.TestCase):
    def setUp(self):
        self.case={'version':1,'reference':{},'candidate':{},'title':'Demo'}
    def test_missing_is_not_match(self):
        self.assertIsNone(similarity('',''))
        self.assertFalse(compare(self.case)['clues'])
    def test_normalized_username(self):
        self.case['reference']['username']='@Example'
        self.case['candidate']['username']='example'
        self.assertEqual(compare(self.case)['text_similarity_percent']['username'],100)
    def test_unicode(self):
        self.assertEqual(similarity('ＡＢＣ','abc'),100)
    def test_report_escapes_input(self):
        self.case['title']='<script>alert(1)</script>'
        report=report_html(self.case,compare(self.case))
        self.assertNotIn('<script>',report)
        self.assertIn('&lt;script&gt;',report)
    def test_save_load(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'case.json';save_case(p,self.case)
            self.assertEqual(load_case(p),self.case)
    def test_invalid_case(self):
        with self.assertRaises(ValueError):compare({'version':9})
    def test_bad_photo_does_not_abort_text(self):
        self.case['reference']['photo']='missing.jpg';self.case['candidate']['photo']='missing2.jpg'
        self.assertIn('unavailable',compare(self.case)['photos']['status'])
    def test_exact_photo_and_blank_warning(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'white.png';Image.new('RGB',(40,40),'white').save(p)
            for profile in ('reference','candidate'):self.case[profile]['photo']=str(p)
            result=compare(self.case)['photos']
            self.assertTrue(result['exact_same_file'])
            self.assertTrue(result['low_detail_warning'])
    def test_reencoded_image(self):
        with tempfile.TemporaryDirectory() as d:
            im=Image.new('RGB',(64,64));im.putdata([(x*4,y*4,(x+y)*2) for y in range(64) for x in range(64)])
            a,b=Path(d)/'a.png',Path(d)/'b.bmp';im.save(a);im.save(b)
            self.case['reference']['photo']=str(a);self.case['candidate']['photo']=str(b)
            result=compare(self.case)['photos']
            self.assertFalse(result['exact_same_file'])
            self.assertEqual(result['dhash_distance_out_of_64'],0)
            self.assertFalse(result['low_detail_warning'])

if __name__=='__main__':unittest.main()
