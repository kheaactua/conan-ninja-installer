#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, tools
from conans.errors import ConanException


class NinjainstallerConan(ConanFile):
    name        = 'ninja_installer'
    version     = '1.8.2'
    license     = 'MIT'
    url         = 'https://github.com/kheaactua/conan-ninja-installer'
    description = 'Install Ninja from source'
    settings    = 'os', 'compiler', 'build_type', 'arch_build'

    def source(self):
        self.run('git clone https://github.com/ninja-build/ninja.git')
        self.run('cd ninja && git checkout v%s'%self.version)

    def build(self):

        with tools.chdir('ninja'):
            self.run('./configure.py --bootstrap')

    def package(self):
        self.copy(pattern='*', dst='misc', src=os.path.join('ninja', 'misc'))
        self.copy(pattern='ninja', dst='bin', src=os.path.join('ninja'))

    def package_info(self):
        self.env_info.path.append(os.path.join(self.package_folder, 'bin'))

# vim: ts=4 sw=4 expandtab ffs=unix ft=python foldmethod=marker :
