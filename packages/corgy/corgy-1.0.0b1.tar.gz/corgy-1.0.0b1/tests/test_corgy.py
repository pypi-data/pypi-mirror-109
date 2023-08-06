import argparse
import unittest
from typing import Annotated, Literal, Optional
from unittest.case import expectedFailure
from unittest.mock import MagicMock

from corgy import Corgy


class TestCorgyClass(unittest.TestCase):

    """Tests to check validity of classes inheriting from Corgy."""

    class _CorgyCls(Corgy):
        x1: list[int]
        x2: Annotated[int, "x2 docstr"]
        x3: int = 3
        x4: Annotated[str, "x4 docstr"] = "4"

    def test_corgy_cls_generated_properties(self):
        for _x in ["x1", "x2", "x3", "x4"]:
            with self.subTest(var=_x):
                self.assertTrue(hasattr(self._CorgyCls, _x))
                self.assertIsInstance(getattr(self._CorgyCls, _x), property)

    def test_corgy_cls_default_values(self):
        corgy_inst = self._CorgyCls()
        for _x, _d in zip(["x3", "x4"], [3, "4"]):
            with self.subTest(var=_x):
                _x_default = getattr(corgy_inst, _x)
                self.assertEqual(_x_default, _d, "incorrect default value")

        for _x in ["x1", "x2"]:
            with self.subTest(var=_x):
                with self.assertRaises(AttributeError):
                    _x_default = getattr(corgy_inst, _x)

    def test_corgy_cls_property_docstrings(self):
        for _x in ["x1", "x2", "x3", "x4"]:
            with self.subTest(var=_x):
                _x_prop = getattr(self._CorgyCls, _x)
                if _x in ["x1", "x3"]:
                    self.assertIsNone(_x_prop.__doc__)
                else:
                    self.assertEqual(_x_prop.__doc__, f"{_x} docstr")

    def test_corgy_cls_property_annotations(self):
        for _x, _type in zip(["x1", "x2", "x3", "x4"], [list[int], int, int, str]):
            with self.subTest(var=_x):
                _x_prop = getattr(self._CorgyCls, _x)
                self.assertEqual(_x_prop.fget.__annotations__["return"], _type)

                self.assertEqual(
                    len(_x_prop.fget.__annotations__),
                    1,
                    f"spurious annotations: {_x_prop.fget.__annotations__}",
                )

                self.assertEqual(_x_prop.fset.__annotations__["val"], _type)
                self.assertEqual(
                    len(_x_prop.fset.__annotations__),
                    1,
                    f"spurious annotations: {_x_prop.fset.__annotations__}",
                )

    def test_corgy_cls_bad_help(self):
        with self.assertRaises(TypeError):

            # pylint: disable=unused-variable
            class C1(Corgy):
                x: Annotated[int, 1]

        class C2(Corgy):
            x: Annotated[int, "x help", "blah", 3]

        self.assertEqual(C2.x.__doc__, "x help")

    def test_corgy_cls_param_name_default(self):
        class C(Corgy):
            __defaults: int
            x: int = 0

        self.assertTrue(hasattr(C, "__defaults"))
        self.assertIsInstance(getattr(C, "__defaults"), dict)
        self.assertTrue(hasattr(C, "_C__defaults"))
        self.assertIsInstance(C._C__defaults, property)
        self.assertEqual(C().x, 0)

    def test_corgy_cls_dunder_var(self):
        class C(Corgy):
            x: int = 0
            __x = 2

        c = C()
        self.assertEqual(c.x, 0)
        c.x = 1
        self.assertEqual(c.x, 1)
        self.assertEqual(c._C__x, 2)


class TestCorgyParserGeneration(unittest.TestCase):
    # pylint: disable=too-many-public-methods

    """Tests to check that Corgy properly adds arguments to ArgumentParsers."""

    def setUp(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument = MagicMock()
        self.parser.add_argument_group = MagicMock()

    def test_parsing_multi_word_name(self):
        class C(Corgy):
            the_x_arg: int

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--the-x-arg", type=int, required=True
        )

    def test_parsing_name_with_prefix(self):
        class C(Corgy):
            x: int

        C.add_args_to_parser(self.parser, "prefix")
        self.parser.add_argument.assert_called_once_with(
            "--prefix:x", type=int, required=True
        )

    def test_parsing_required_int(self):
        class C(Corgy):
            x: int

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with("--x", type=int, required=True)

    def test_parsing_optional_int_with_default(self):
        class C(Corgy):
            x: int = 0

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with("--x", type=int, default=0)

    @expectedFailure
    def test_parsing_optional_int_with_bad_default(self):
        class C(Corgy):
            x: int = "0"

        with self.assertRaises(TypeError):
            C.add_args_to_parser(self.parser)

    def test_parsing_optional_int_without_default(self):
        class C(Corgy):
            x: Optional[int]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with("--x", type=int)

    def test_parsing_explicit_optional_int_with_default(self):
        class C(Corgy):
            x: Optional[int] = 0

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with("--x", type=int, default=0)

    def test_parsing_optional_int_with_none_default(self):
        class C(Corgy):
            x: int = None

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with("--x", type=int, default=None)

    def test_parsing_required_int_with_docstring(self):
        class C(Corgy):
            x: Annotated[int, "x docstring"]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=int, required=True, help="x docstring"
        )

    def test_parsing_optional_int_with_docstring(self):
        class C(Corgy):
            x: Annotated[Optional[int], "x docstring"]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=int, help="x docstring"
        )

    def test_parsing_required_int_with_choices(self):
        class C(Corgy):
            x: Literal[1, 2, 3]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=int, required=True, choices=(1, 2, 3)
        )

    def test_parsing_int_with_choices_bad_type(self):
        class C(Corgy):
            x: Literal[1, 2, "3"]

        with self.assertRaises(TypeError):
            C.add_args_to_parser(self.parser)

    def test_parsing_required_custom_type(self):
        class T:
            pass

        class C(Corgy):
            x: T

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with("--x", type=T, required=True)

    def test_parsing_optional_custom_type_with_default(self):
        class T:
            pass

        t = T()

        class C(Corgy):
            x: T = t

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with("--x", type=T, default=t)

    def test_parsing_bool(self):
        class C(Corgy):
            x: bool

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=bool, action=argparse.BooleanOptionalAction
        )

    def test_parsing_bool_with_default(self):
        class C(Corgy):
            x: bool = False

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=bool, action=argparse.BooleanOptionalAction, default=False
        )

    def test_parsing_required_int_list(self):
        class C(Corgy):
            x: list[int]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=int, nargs="*", required=True
        )

    def test_parsing_optional_int_list(self):
        class C(Corgy):
            x: Optional[list[int]]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with("--x", type=int, nargs="*")

    def test_parsing_non_empty_required_list(self):
        class C(Corgy):
            x: list[int, ...]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=int, nargs="+", required=True
        )

    def test_parsing_int_list_with_default(self):
        class C(Corgy):
            x: list[int] = [1, 2, 3]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=int, nargs="*", default=[1, 2, 3]
        )

    def test_parsing_required_int_list_with_choices(self):
        class C(Corgy):
            x: list[Literal[1, 2, 3]]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=int, nargs="*", required=True, choices=(1, 2, 3)
        )

    def test_parsing_fixed_length_required_int_list(self):
        class C(Corgy):
            x: list[int, int, int]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=int, nargs=3, required=True
        )

    def test_parsing_length_2_required_int_list(self):
        class C(Corgy):
            x: list[int, int]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=int, nargs=2, required=True
        )

    def test_parsing_fixed_length_required_multi_type_list(self):
        class C(Corgy):
            x: list[int, str, int]

        with self.assertRaises(TypeError):
            C.add_args_to_parser(self.parser)

    def test_parsing_required_int_tuple(self):
        class C(Corgy):
            x: tuple[int]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with(
            "--x", type=int, required=True, nargs="*"
        )

    def test_parsing_argument_group(self):
        class G(Corgy):
            x: int

        G.add_args_to_parser = MagicMock()

        class C(Corgy):
            g: Annotated[G, "group G"]

        C.add_args_to_parser(self.parser)
        self.parser.add_argument_group.assert_called_once_with("g", "group G")
        G.add_args_to_parser.assert_called_once_with(
            self.parser.add_argument_group.return_value, "g"
        )

    def test_parsing_argument_group_with_other_param(self):
        class G(Corgy):
            x: int

        class C(Corgy):
            x: int
            g: G

        C.add_args_to_parser(self.parser)
        self.parser.add_argument.assert_called_once_with("--x", type=int, required=True)
        self.parser.add_argument_group.assert_called_once_with("g", None)


class TestCorgyParsing(unittest.TestCase):

    """Test cases to check parsing of command line arguments by Corgy."""

    def setUp(self):
        self.parser = argparse.ArgumentParser()
        self.orig_parse_args = argparse.ArgumentParser.parse_args

    def test_corgy_property_retrieval_after_parse(self):
        class C(Corgy):
            x: int
            y: str
            z: list[int]

        self.parser.parse_args = lambda: self.orig_parse_args(
            self.parser, ["--x", "1", "--y", "2", "--z", "3", "4"]
        )
        c = C.parse_from_cmdline(self.parser)
        self.assertEqual(c.x, 1)
        self.assertEqual(c.y, "2")
        self.assertListEqual(c.z, [3, 4])

    def test_corgy_sequence_type_conversion_after_parse(self):
        class C(Corgy):
            x: list[int]
            y: set[int]
            z: tuple[int]

        self.parser.parse_args = lambda: self.orig_parse_args(
            self.parser, ["--x", "1", "2", "--y", "3", "4", "5", "--z", "6", "7"]
        )
        c = C.parse_from_cmdline(self.parser)
        self.assertIs(type(c.x), list)
        self.assertIs(type(c.y), set)
        self.assertIs(type(c.z), tuple)

    def test_corgy_argument_group_retrieval(self):
        class G(Corgy):
            x: int
            y: str

        class C(Corgy):
            x: int
            y: int
            g: G

        self.parser.parse_args = lambda: self.orig_parse_args(
            self.parser, ["--x", "1", "--y", "2", "--g:x", "3", "--g:y", "four"]
        )
        c = C.parse_from_cmdline(self.parser)
        self.assertEqual(c.x, 1)
        self.assertEqual(c.y, 2)
        self.assertEqual(c.g.x, 3)
        self.assertEqual(c.g.y, "four")

    def test_corgy_nested_argument_group_retrieval(self):
        class G1(Corgy):
            x: int

        class G2(Corgy):
            x: int
            g: G1

        class C(Corgy):
            x: int
            g1: G1
            g2: G2

        self.parser.parse_args = lambda: self.orig_parse_args(
            self.parser, ["--x", "1", "--g1:x", "2", "--g2:x", "3", "--g2:g:x", "4"]
        )
        c = C.parse_from_cmdline(self.parser)
        self.assertEqual(c.x, 1)
        self.assertEqual(c.g1.x, 2)
        self.assertEqual(c.g2.x, 3)
        self.assertEqual(c.g2.g.x, 4)
