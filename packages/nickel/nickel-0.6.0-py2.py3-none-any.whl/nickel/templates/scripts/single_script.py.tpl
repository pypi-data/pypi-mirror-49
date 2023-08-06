# coding=utf8

import sys
import os

sys.path.insert(0, '.')
os.env.setdefault('DJANGO_SETTINGS_MODULE', '{{ settings_module_name }}')

import django

if hasattr(django, 'setup'):
    django.setup()


def {{function_name}}():
   pass

if __name__ == '__main__':
    {{ function_name }}()