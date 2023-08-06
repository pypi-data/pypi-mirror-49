#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ######################################################################
# Copyright (C) 2016-2018  Fridolin Pokorny, fridolin.pokorny@gmail.com
# This file is part of Selinon project.
# ######################################################################

import os
import pytest
from selinon import Config
from selinon import Trace
from selinon_test_case import SelinonTestCase


class TestTrace(SelinonTestCase):
    def test_trace_setup(self):
        assert len(Trace._trace_functions) == 0

        test_file = os.path.join(self.DATA_DIR, 'test_trace_setup.yaml')
        Config.set_config_yaml(test_file, flow_definition_files=[test_file])

        # logging, sentry, storage and a custom function - 3 callbacks registered
        # By default there is configured logging module to be used with Sentry.
        assert len(Trace._trace_functions) == 3
        assert Trace._logger is not None

    @pytest.mark.skip(reason="trace calls are currently not tested")
    def test_trace_call(self):
        # TODO: add tests for actual trace call
        pass
