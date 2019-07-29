"""
Tests for the Flap class of shutthebox.
"""

from nose.tools import raises, assert_raises
import shutthebox

# pylint: disable=missing-docstring
# pylint: disable=no-self-use
# pylint: disable=attribute-defined-outside-init

class TestFlap:
    def setup(self):
        self.flap = shutthebox.Flap(1)

    def test_number(self):
        assert self.flap.number == 1

    @raises(ValueError)
    def test_number_too_small(self):
        shutthebox.Flap(0)

    @raises(ValueError)
    def test_number_non_int(self):
        shutthebox.Flap(1.5)

    def test_up_by_default(self):
        assert self.flap.is_down is False

    def test_lower(self):
        self.flap.lower()
        assert self.flap.is_down

    def test_lower_when_already_down(self):
        self.flap.lower()
        assert_raises(RuntimeError, self.flap.lower)
