from typing import List

from util import RuleException
from model.target import Target
from model.input_file import InputFile

import pytest


class TestTarget(Target):
  def __init__(self, test_file: InputFile, file_deps: List[InputFile], cache: bool):
    super().__init__(sources=[test_file], file_deps=file_deps, deps=[], cache=cache)
    self.test_file = test_file


  def execute(self):
    return_value = pytest.main([str(self.test_file.file_name)])
    if return_value > 0:
      raise RuleException('Test failed.')
    return 'Test result: OK'
