#!/usr/bin/env python

import os
import sys

from bert import factory, utils

if __name__ in ['__main__']:
  sys.path.append(os.getcwd())
  options = factory.capture_options()
  if options.how:
    utils.show_how(options)
    sys.exit(0)

  if options.new_module:
    utils.new_module(options)
    sys.exit(0)

  factory.setup(options)
  factory.scan_jobs(options)
  factory.validate_jobs(options)
  factory.start_jobs(options)

