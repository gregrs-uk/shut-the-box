from nose.tools import raises, assert_raises
import shutthebox

class TestBox:
    def setUp(self):
        self.box = shutthebox.Box()
        self.big_box = shutthebox.Box(12)

    def test_default_number_of_flaps(self):
        assert self.box.num_flaps == 9
        assert len(self.box.flaps) == 9

    def test_number_of_specified_flap(self):
        assert self.box.flaps[9].number == 9

    def test_non_default_number_of_flaps(self):
        new_box = shutthebox.Box(3)
        assert new_box.num_flaps == 3
        assert len(new_box.flaps) == 3

    @raises(ValueError)
    def test_number_of_flaps_too_small(self):
        shutthebox.Box(0)

    @raises(ValueError)
    def test_number_of_flaps_non_int(self):
        shutthebox.Box(1.5)

    def test_get_available_flaps_returns_dict_of_flap_objects(self):
        assert isinstance(self.box.get_available_flaps(), dict)
        assert isinstance(self.box.get_available_flaps()[1], shutthebox.Flap)

    def test_get_available_flaps_returns_correct_flaps(self):
        small_box = shutthebox.Box(3)
        assert list(small_box.get_available_flaps().keys()) == [1, 2, 3]
        small_box.flaps[2].lower()
        assert list(small_box.get_available_flaps().keys()) == [1, 3]

    def test_sum_available_flaps_default(self):
        assert self.box.sum_available_flaps() == 45 # 9 + 8 + 7 + ... + 1

    def test_sum_available_flaps_none(self):
        # lower all flaps
        for this_flap_num in list(self.box.flaps.keys()):
            self.box.flaps[this_flap_num].lower()
        assert self.box.sum_available_flaps() == 0

    def test_str_flaps_all_up(self):
        assert str(self.big_box) == ('  UP: 1 2 3 4 5 6 7 8 9 10 11 12\n' +
                                     'DOWN:                           ')

    def test_str_flaps_all_down(self):
        for this_flap_num, this_flap in self.big_box.flaps.items():
            this_flap.lower()
        assert str(self.big_box) == ('  UP:                           \n' +
                                     'DOWN: 1 2 3 4 5 6 7 8 9 10 11 12')

    def test_str_flaps_some_up_some_down(self):
        self.big_box.flaps[7].lower()
        self.big_box.flaps[11].lower()
        assert str(self.big_box) == ('  UP: 1 2 3 4 5 6   8 9 10    12\n' +
                                     'DOWN:             7        11   ')
