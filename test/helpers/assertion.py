import pandas.testing as pdt


def assert_dict_df(expected: dict, out: dict):
    for (ek, ev) , (ok, ov) in zip(expected.items(), out.items()):
        assert ek == ok
        pdt.assert_frame_equal(ov, ev)