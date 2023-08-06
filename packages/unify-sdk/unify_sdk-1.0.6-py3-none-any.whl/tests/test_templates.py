import unittest
from unify.templates import Templates
import json
import os
import uuid
from tests import test_org, cluster_name, props


class TestTemplates(unittest.TestCase):
    templates = Templates(cluster_name, props)
    templates.upload_string_content_file(
        test_org,
        """Template Name,Attribute,Datatype,UoM,Attribute Type
        Conveyer,Vibration,Float4,hz,""")
    test_template = templates.list_asset_templates(test_org)[0]
    template_id = test_template['id']
    template_name = test_template['name']
    version = test_template['version']

    def test_category(self):
        categories = ['python sdk test']
        self.templates.category(test_org, self.template_id, self.template_name, self.version, categories)

        all_categories = self.templates.list_all_categories(test_org)
        self.assertListEqual(list(all_categories.keys()), categories)
        
        template_category_ids  =  self.templates.get_template(test_org, self.template_id)['categoryIds']
        self.assertListEqual(list(all_categories.values()), template_category_ids)

    def test_category_with_existing_category(self):
        categories = ['python sdk test']
        self.templates.category(test_org, self.template_id, self.template_name, self.version, categories)

        new_categories = ['python sdk test', 'antoher category']
        self.templates.category(test_org, self.template_id, self.template_name, self.version, new_categories)

        all_categories = self.templates.list_all_categories(test_org)
        self.assertListEqual(list(all_categories.keys()), new_categories)
        
        template_category_ids  =  self.templates.get_template(test_org, self.template_id)['categoryIds']
        self.assertListEqual(list(all_categories.values()), template_category_ids)
        

    