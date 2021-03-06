#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, tools


class NinjainstallerConan(ConanFile):
    name        = 'ninja_installer'
    version     = '1.8.2'
    license     = 'MIT'
    url         = 'https://github.com/kheaactua/conan-ninja-installer'
    description = 'Install Ninja from source'

    settings = {
        'os_build':   ['Windows', 'Linux', 'Macos'],
        'arch_build': ['x86', 'x86_64', 'armv7'],
    }

    # Using the os_version here so 14.04x86 ninja doesn't clobber 11.10x86 ninja
    options = {'os_version': 'ANY'}
    default_options = 'os_version=' + str(tools.os_info.os_version)

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
        # Note: If this recipe is in the profile, this will cause CMake to
        # always try to use Ninja, which can be problematic for some recipes
        # (e.g. MRPT)
        self.env_info.CONAN_CMAKE_GENERATOR = 'Ninja'

        ninja_path = os.path.join(self.package_folder, 'bin')
        if str(self.settings.os_build) in ['Linux', 'Macosx']:
            ninja_exe  = os.path.join(ninja_path, 'ninja')
            os.chmod(ninja_exe, os.stat(ninja_exe).st_mode | 0o111)
        self.env_info.path.append(ninja_path)

# vim: ts=4 sw=4 expandtab ffs=unix ft=python foldmethod=marker :
