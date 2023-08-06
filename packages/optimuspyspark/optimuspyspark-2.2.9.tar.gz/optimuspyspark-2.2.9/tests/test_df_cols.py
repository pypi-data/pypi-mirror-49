from pyspark.sql.types import *
from optimus import Optimus
from optimus.helpers.json import json_enconding
from pyspark.ml.linalg import Vectors, VectorUDT, DenseVector
import numpy as np

nan = np.nan
import datetime
from pyspark.sql import functions as F

op = Optimus(master='local')
source_df = op.create.df(
    [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
     ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
     ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
     ('date arrival', StringType(), True), ('last date seen', StringType(), True),
     ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
     ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
     ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [(
                                                                                 "Optim'us", -28, 'Leader', 10, 5000000,
                                                                                 4.300000190734863,
                                                                                 ['Inochi', 'Convoy'],
                                                                                 '19.442735,-99.201111', '1980/04/10',
                                                                                 '2016/09/10',
                                                                                 [8.53439998626709, 4300.0],
                                                                                 datetime.date(2016, 9, 10),
                                                                                 datetime.datetime(2014, 6, 24, 0, 0),
                                                                                 True, bytearray(b'Leader'), None), (
                                                                                 'bumbl#ebéé  ', 17, 'Espionage', 7,
                                                                                 5000000, 2.0, ['Bumble', 'Goldback'],
                                                                                 '10.642707,-71.612534', '1980/04/10',
                                                                                 '2015/08/10',
                                                                                 [5.334000110626221, 2000.0],
                                                                                 datetime.date(2015, 8, 10),
                                                                                 datetime.datetime(2014, 6, 24, 0, 0),
                                                                                 True, bytearray(b'Espionage'), None), (
                                                                                 'ironhide&', 26, 'Security', 7,
                                                                                 5000000, 4.0, ['Roadbuster'],
                                                                                 '37.789563,-122.400356', '1980/04/10',
                                                                                 '2014/07/10',
                                                                                 [7.924799919128418, 4000.0],
                                                                                 datetime.date(2014, 6, 24),
                                                                                 datetime.datetime(2014, 6, 24, 0, 0),
                                                                                 True, bytearray(b'Security'), None), (
                                                                                 'Jazz', 13, 'First Lieutenant', 8,
                                                                                 5000000, 1.7999999523162842,
                                                                                 ['Meister'], '33.670666,-117.841553',
                                                                                 '1980/04/10', '2013/06/10',
                                                                                 [3.962399959564209, 1800.0],
                                                                                 datetime.date(2013, 6, 24),
                                                                                 datetime.datetime(2014, 6, 24, 0, 0),
                                                                                 True, bytearray(b'First Lieutenant'),
                                                                                 None), (
                                                                                 'Megatron', None, 'None', 10, 5000000,
                                                                                 5.699999809265137, ['Megatron'], None,
                                                                                 '1980/04/10', '2012/05/10',
                                                                                 [None, 5700.0],
                                                                                 datetime.date(2012, 5, 10),
                                                                                 datetime.datetime(2014, 6, 24, 0, 0),
                                                                                 True, bytearray(b'None'), None), (
                                                                                 'Metroplex_)^$', 300, 'Battle Station',
                                                                                 8, 5000000, None, ['Metroflex'], None,
                                                                                 '1980/04/10', '2011/04/10',
                                                                                 [91.44000244140625, None],
                                                                                 datetime.date(2011, 4, 10),
                                                                                 datetime.datetime(2014, 6, 24, 0, 0),
                                                                                 True, bytearray(b'Battle Station'),
                                                                                 None), (
                                                                                 None, None, None, None, None, None,
                                                                                 None, None, None, None, None, None,
                                                                                 None, None, None, None)])


class Testdf_cols(object):
    @staticmethod
    def test_cols_abs():
        actual_df = source_df.cols.abs('height(ft)')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("Optim'us", 28, 'Leader', 10,
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         'bumbl#ebéé  ', 17,
                                                                                         'Espionage', 7, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         (
                                                                                         'ironhide&', 26, 'Security', 7,
                                                                                         5000000, 4.0, ['Roadbuster'],
                                                                                         '37.789563,-122.400356',
                                                                                         '1980/04/10', '2014/07/10',
                                                                                         [7.924799919128418, 4000.0],
                                                                                         datetime.date(2014, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Security'), None),
                                                                                         (
                                                                                         'Jazz', 13, 'First Lieutenant',
                                                                                         8, 5000000, 1.7999999523162842,
                                                                                         ['Meister'],
                                                                                         '33.670666,-117.841553',
                                                                                         '1980/04/10', '2013/06/10',
                                                                                         [3.962399959564209, 1800.0],
                                                                                         datetime.date(2013, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'First Lieutenant'),
                                                                                         None), (
                                                                                         'Megatron', None, 'None', 10,
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$', 300,
                                                                                         'Battle Station', 8, 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '1980/04/10', '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_abs_all_columns():
        actual_df = source_df.cols.abs('*')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("Optim'us", 28, 'Leader', 10,
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         'bumbl#ebéé  ', 17,
                                                                                         'Espionage', 7, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         (
                                                                                         'ironhide&', 26, 'Security', 7,
                                                                                         5000000, 4.0, ['Roadbuster'],
                                                                                         '37.789563,-122.400356',
                                                                                         '1980/04/10', '2014/07/10',
                                                                                         [7.924799919128418, 4000.0],
                                                                                         datetime.date(2014, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Security'), None),
                                                                                         (
                                                                                         'Jazz', 13, 'First Lieutenant',
                                                                                         8, 5000000, 1.7999999523162842,
                                                                                         ['Meister'],
                                                                                         '33.670666,-117.841553',
                                                                                         '1980/04/10', '2013/06/10',
                                                                                         [3.962399959564209, 1800.0],
                                                                                         datetime.date(2013, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'First Lieutenant'),
                                                                                         None), (
                                                                                         'Megatron', None, 'None', 10,
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$', 300,
                                                                                         'Battle Station', 8, 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '1980/04/10', '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_add():
        actual_df = source_df.cols.add(['height(ft)', 'rank'])
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', FloatType(), True), ('function', StringType(), True),
             ('rank', FloatType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True), ('sum', FloatType(), True)], [(
                                                                                                                     "Optim'us",
                                                                                                                     -28.0,
                                                                                                                     'Leader',
                                                                                                                     10.0,
                                                                                                                     5000000,
                                                                                                                     4.300000190734863,
                                                                                                                     [
                                                                                                                         'Inochi',
                                                                                                                         'Convoy'],
                                                                                                                     '19.442735,-99.201111',
                                                                                                                     '1980/04/10',
                                                                                                                     '2016/09/10',
                                                                                                                     [
                                                                                                                         8.53439998626709,
                                                                                                                         4300.0],
                                                                                                                     datetime.date(
                                                                                                                         2016,
                                                                                                                         9,
                                                                                                                         10),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'Leader'),
                                                                                                                     None,
                                                                                                                     -18.0),
                                                                                                                     (
                                                                                                                     'bumbl#ebéé  ',
                                                                                                                     17.0,
                                                                                                                     'Espionage',
                                                                                                                     7.0,
                                                                                                                     5000000,
                                                                                                                     2.0,
                                                                                                                     [
                                                                                                                         'Bumble',
                                                                                                                         'Goldback'],
                                                                                                                     '10.642707,-71.612534',
                                                                                                                     '1980/04/10',
                                                                                                                     '2015/08/10',
                                                                                                                     [
                                                                                                                         5.334000110626221,
                                                                                                                         2000.0],
                                                                                                                     datetime.date(
                                                                                                                         2015,
                                                                                                                         8,
                                                                                                                         10),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'Espionage'),
                                                                                                                     None,
                                                                                                                     24.0),
                                                                                                                     (
                                                                                                                     'ironhide&',
                                                                                                                     26.0,
                                                                                                                     'Security',
                                                                                                                     7.0,
                                                                                                                     5000000,
                                                                                                                     4.0,
                                                                                                                     [
                                                                                                                         'Roadbuster'],
                                                                                                                     '37.789563,-122.400356',
                                                                                                                     '1980/04/10',
                                                                                                                     '2014/07/10',
                                                                                                                     [
                                                                                                                         7.924799919128418,
                                                                                                                         4000.0],
                                                                                                                     datetime.date(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'Security'),
                                                                                                                     None,
                                                                                                                     33.0),
                                                                                                                     (
                                                                                                                     'Jazz',
                                                                                                                     13.0,
                                                                                                                     'First Lieutenant',
                                                                                                                     8.0,
                                                                                                                     5000000,
                                                                                                                     1.7999999523162842,
                                                                                                                     [
                                                                                                                         'Meister'],
                                                                                                                     '33.670666,-117.841553',
                                                                                                                     '1980/04/10',
                                                                                                                     '2013/06/10',
                                                                                                                     [
                                                                                                                         3.962399959564209,
                                                                                                                         1800.0],
                                                                                                                     datetime.date(
                                                                                                                         2013,
                                                                                                                         6,
                                                                                                                         24),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'First Lieutenant'),
                                                                                                                     None,
                                                                                                                     21.0),
                                                                                                                     (
                                                                                                                     'Megatron',
                                                                                                                     None,
                                                                                                                     'None',
                                                                                                                     10.0,
                                                                                                                     5000000,
                                                                                                                     5.699999809265137,
                                                                                                                     [
                                                                                                                         'Megatron'],
                                                                                                                     None,
                                                                                                                     '1980/04/10',
                                                                                                                     '2012/05/10',
                                                                                                                     [
                                                                                                                         None,
                                                                                                                         5700.0],
                                                                                                                     datetime.date(
                                                                                                                         2012,
                                                                                                                         5,
                                                                                                                         10),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'None'),
                                                                                                                     None,
                                                                                                                     None),
                                                                                                                     (
                                                                                                                     'Metroplex_)^$',
                                                                                                                     300.0,
                                                                                                                     'Battle Station',
                                                                                                                     8.0,
                                                                                                                     5000000,
                                                                                                                     None,
                                                                                                                     [
                                                                                                                         'Metroflex'],
                                                                                                                     None,
                                                                                                                     '1980/04/10',
                                                                                                                     '2011/04/10',
                                                                                                                     [
                                                                                                                         91.44000244140625,
                                                                                                                         None],
                                                                                                                     datetime.date(
                                                                                                                         2011,
                                                                                                                         4,
                                                                                                                         10),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'Battle Station'),
                                                                                                                     None,
                                                                                                                     308.0),
                                                                                                                     (
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_add_all_columns():
        actual_df = source_df.cols.add('*')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', FloatType(), True), ('function', StringType(), True),
             ('rank', FloatType(), True), ('age', FloatType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True), ('sum', FloatType(), True)], [(
                                                                                                                     "Optim'us",
                                                                                                                     -28.0,
                                                                                                                     'Leader',
                                                                                                                     10.0,
                                                                                                                     5000000.0,
                                                                                                                     4.300000190734863,
                                                                                                                     [
                                                                                                                         'Inochi',
                                                                                                                         'Convoy'],
                                                                                                                     '19.442735,-99.201111',
                                                                                                                     '1980/04/10',
                                                                                                                     '2016/09/10',
                                                                                                                     [
                                                                                                                         8.53439998626709,
                                                                                                                         4300.0],
                                                                                                                     datetime.date(
                                                                                                                         2016,
                                                                                                                         9,
                                                                                                                         10),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'Leader'),
                                                                                                                     None,
                                                                                                                     4999986.5),
                                                                                                                     (
                                                                                                                     'bumbl#ebéé  ',
                                                                                                                     17.0,
                                                                                                                     'Espionage',
                                                                                                                     7.0,
                                                                                                                     5000000.0,
                                                                                                                     2.0,
                                                                                                                     [
                                                                                                                         'Bumble',
                                                                                                                         'Goldback'],
                                                                                                                     '10.642707,-71.612534',
                                                                                                                     '1980/04/10',
                                                                                                                     '2015/08/10',
                                                                                                                     [
                                                                                                                         5.334000110626221,
                                                                                                                         2000.0],
                                                                                                                     datetime.date(
                                                                                                                         2015,
                                                                                                                         8,
                                                                                                                         10),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'Espionage'),
                                                                                                                     None,
                                                                                                                     5000026.0),
                                                                                                                     (
                                                                                                                     'ironhide&',
                                                                                                                     26.0,
                                                                                                                     'Security',
                                                                                                                     7.0,
                                                                                                                     5000000.0,
                                                                                                                     4.0,
                                                                                                                     [
                                                                                                                         'Roadbuster'],
                                                                                                                     '37.789563,-122.400356',
                                                                                                                     '1980/04/10',
                                                                                                                     '2014/07/10',
                                                                                                                     [
                                                                                                                         7.924799919128418,
                                                                                                                         4000.0],
                                                                                                                     datetime.date(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'Security'),
                                                                                                                     None,
                                                                                                                     5000037.0),
                                                                                                                     (
                                                                                                                     'Jazz',
                                                                                                                     13.0,
                                                                                                                     'First Lieutenant',
                                                                                                                     8.0,
                                                                                                                     5000000.0,
                                                                                                                     1.7999999523162842,
                                                                                                                     [
                                                                                                                         'Meister'],
                                                                                                                     '33.670666,-117.841553',
                                                                                                                     '1980/04/10',
                                                                                                                     '2013/06/10',
                                                                                                                     [
                                                                                                                         3.962399959564209,
                                                                                                                         1800.0],
                                                                                                                     datetime.date(
                                                                                                                         2013,
                                                                                                                         6,
                                                                                                                         24),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'First Lieutenant'),
                                                                                                                     None,
                                                                                                                     5000023.0),
                                                                                                                     (
                                                                                                                     'Megatron',
                                                                                                                     None,
                                                                                                                     'None',
                                                                                                                     10.0,
                                                                                                                     5000000.0,
                                                                                                                     5.699999809265137,
                                                                                                                     [
                                                                                                                         'Megatron'],
                                                                                                                     None,
                                                                                                                     '1980/04/10',
                                                                                                                     '2012/05/10',
                                                                                                                     [
                                                                                                                         None,
                                                                                                                         5700.0],
                                                                                                                     datetime.date(
                                                                                                                         2012,
                                                                                                                         5,
                                                                                                                         10),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'None'),
                                                                                                                     None,
                                                                                                                     None),
                                                                                                                     (
                                                                                                                     'Metroplex_)^$',
                                                                                                                     300.0,
                                                                                                                     'Battle Station',
                                                                                                                     8.0,
                                                                                                                     5000000.0,
                                                                                                                     None,
                                                                                                                     [
                                                                                                                         'Metroflex'],
                                                                                                                     None,
                                                                                                                     '1980/04/10',
                                                                                                                     '2011/04/10',
                                                                                                                     [
                                                                                                                         91.44000244140625,
                                                                                                                         None],
                                                                                                                     datetime.date(
                                                                                                                         2011,
                                                                                                                         4,
                                                                                                                         10),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'Battle Station'),
                                                                                                                     None,
                                                                                                                     None),
                                                                                                                     (
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_append_number():
        actual_df = source_df.cols.append('new col', 1)
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True),
             ('new col', IntegerType(), False)], [("Optim'us", -28, 'Leader', 10, 5000000, 4.300000190734863,
                                                   ['Inochi', 'Convoy'], '19.442735,-99.201111', '1980/04/10',
                                                   '2016/09/10', [8.53439998626709, 4300.0], datetime.date(2016, 9, 10),
                                                   datetime.datetime(2014, 6, 24, 0, 0), True, bytearray(b'Leader'),
                                                   None, 1), ('bumbl#ebéé  ', 17, 'Espionage', 7, 5000000, 2.0,
                                                              ['Bumble', 'Goldback'], '10.642707,-71.612534',
                                                              '1980/04/10', '2015/08/10', [5.334000110626221, 2000.0],
                                                              datetime.date(2015, 8, 10),
                                                              datetime.datetime(2014, 6, 24, 0, 0), True,
                                                              bytearray(b'Espionage'), None, 1), (
                                                  'ironhide&', 26, 'Security', 7, 5000000, 4.0, ['Roadbuster'],
                                                  '37.789563,-122.400356', '1980/04/10', '2014/07/10',
                                                  [7.924799919128418, 4000.0], datetime.date(2014, 6, 24),
                                                  datetime.datetime(2014, 6, 24, 0, 0), True, bytearray(b'Security'),
                                                  None, 1), (
                                                  'Jazz', 13, 'First Lieutenant', 8, 5000000, 1.7999999523162842,
                                                  ['Meister'], '33.670666,-117.841553', '1980/04/10', '2013/06/10',
                                                  [3.962399959564209, 1800.0], datetime.date(2013, 6, 24),
                                                  datetime.datetime(2014, 6, 24, 0, 0), True,
                                                  bytearray(b'First Lieutenant'), None, 1), (
                                                  'Megatron', None, 'None', 10, 5000000, 5.699999809265137,
                                                  ['Megatron'], None, '1980/04/10', '2012/05/10', [None, 5700.0],
                                                  datetime.date(2012, 5, 10), datetime.datetime(2014, 6, 24, 0, 0),
                                                  True, bytearray(b'None'), None, 1), (
                                                  'Metroplex_)^$', 300, 'Battle Station', 8, 5000000, None,
                                                  ['Metroflex'], None, '1980/04/10', '2011/04/10',
                                                  [91.44000244140625, None], datetime.date(2011, 4, 10),
                                                  datetime.datetime(2014, 6, 24, 0, 0), True,
                                                  bytearray(b'Battle Station'), None, 1), (
                                                  None, None, None, None, None, None, None, None, None, None, None,
                                                  None, None, None, None, None, 1)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_cast():
        actual_df = source_df.cols.cast('function', 'string')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("Optim'us", -28, 'Leader', 10,
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         'bumbl#ebéé  ', 17,
                                                                                         'Espionage', 7, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         (
                                                                                         'ironhide&', 26, 'Security', 7,
                                                                                         5000000, 4.0, ['Roadbuster'],
                                                                                         '37.789563,-122.400356',
                                                                                         '1980/04/10', '2014/07/10',
                                                                                         [7.924799919128418, 4000.0],
                                                                                         datetime.date(2014, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Security'), None),
                                                                                         (
                                                                                         'Jazz', 13, 'First Lieutenant',
                                                                                         8, 5000000, 1.7999999523162842,
                                                                                         ['Meister'],
                                                                                         '33.670666,-117.841553',
                                                                                         '1980/04/10', '2013/06/10',
                                                                                         [3.962399959564209, 1800.0],
                                                                                         datetime.date(2013, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'First Lieutenant'),
                                                                                         None), (
                                                                                         'Megatron', None, 'None', 10,
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$', 300,
                                                                                         'Battle Station', 8, 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '1980/04/10', '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_cast_all_columns():
        actual_df = source_df.cols.cast('*', 'string')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', StringType(), True), ('function', StringType(), True),
             ('rank', StringType(), True), ('age', StringType(), True), ('weight(t)', StringType(), True),
             ('japanese name', StringType(), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', StringType(), True), ('Date Type', StringType(), True), ('Tiemstamp', StringType(), True),
             ('Cybertronian', StringType(), True), ('function(binary)', StringType(), True),
             ('NullType', StringType(), True)], [("Optim'us", '-28', 'Leader', '10', '5000000', '4.3',
                                                  '[Inochi, Convoy]', '19.442735,-99.201111', '1980/04/10',
                                                  '2016/09/10', '[8.5344, 4300.0]', '2016-09-10', '2014-06-24 00:00:00',
                                                  'true', 'Leader', None), (
                                                 'bumbl#ebéé  ', '17', 'Espionage', '7', '5000000', '2.0',
                                                 '[Bumble, Goldback]', '10.642707,-71.612534', '1980/04/10',
                                                 '2015/08/10', '[5.334, 2000.0]', '2015-08-10', '2014-06-24 00:00:00',
                                                 'true', 'Espionage', None), (
                                                 'ironhide&', '26', 'Security', '7', '5000000', '4.0', '[Roadbuster]',
                                                 '37.789563,-122.400356', '1980/04/10', '2014/07/10',
                                                 '[7.9248, 4000.0]', '2014-06-24', '2014-06-24 00:00:00', 'true',
                                                 'Security', None), (
                                                 'Jazz', '13', 'First Lieutenant', '8', '5000000', '1.8', '[Meister]',
                                                 '33.670666,-117.841553', '1980/04/10', '2013/06/10',
                                                 '[3.9624, 1800.0]', '2013-06-24', '2014-06-24 00:00:00', 'true',
                                                 'First Lieutenant', None), (
                                                 'Megatron', None, 'None', '10', '5000000', '5.7', '[Megatron]', None,
                                                 '1980/04/10', '2012/05/10', '[, 5700.0]', '2012-05-10',
                                                 '2014-06-24 00:00:00', 'true', 'None', None), (
                                                 'Metroplex_)^$', '300', 'Battle Station', '8', '5000000', None,
                                                 '[Metroflex]', None, '1980/04/10', '2011/04/10', '[91.44,]',
                                                 '2011-04-10', '2014-06-24 00:00:00', 'true', 'Battle Station', None), (
                                                 None, None, None, None, None, None, None, None, None, None, None, None,
                                                 None, None, None, None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_clip():
        actual_df = source_df.cols.clip('rank', 3, 5)
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', IntegerType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("Optim'us", -28, 'Leader', 5,
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         'bumbl#ebéé  ', 17,
                                                                                         'Espionage', 5, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         (
                                                                                         'ironhide&', 26, 'Security', 5,
                                                                                         5000000, 4.0, ['Roadbuster'],
                                                                                         '37.789563,-122.400356',
                                                                                         '1980/04/10', '2014/07/10',
                                                                                         [7.924799919128418, 4000.0],
                                                                                         datetime.date(2014, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Security'), None),
                                                                                         (
                                                                                         'Jazz', 13, 'First Lieutenant',
                                                                                         5, 5000000, 1.7999999523162842,
                                                                                         ['Meister'],
                                                                                         '33.670666,-117.841553',
                                                                                         '1980/04/10', '2013/06/10',
                                                                                         [3.962399959564209, 1800.0],
                                                                                         datetime.date(2013, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'First Lieutenant'),
                                                                                         None), (
                                                                                         'Megatron', None, 'None', 5,
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$', 300,
                                                                                         'Battle Station', 5, 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '1980/04/10', '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_clip_all_columns():
        actual_df = source_df.cols.clip('*', 3, 5)
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', IntegerType(), True), ('function', StringType(), True),
             ('rank', IntegerType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("Optim'us", 3, 'Leader', 5, 5,
                                                                                          4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         'bumbl#ebéé  ', 5, 'Espionage',
                                                                                         5, 5, 3.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         ('ironhide&', 5, 'Security', 5,
                                                                                          5, 4.0, ['Roadbuster'],
                                                                                          '37.789563,-122.400356',
                                                                                          '1980/04/10', '2014/07/10',
                                                                                          [7.924799919128418, 4000.0],
                                                                                          datetime.date(2014, 6, 24),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Security'), None),
                                                                                         ('Jazz', 5, 'First Lieutenant',
                                                                                          5, 5, 3.0, ['Meister'],
                                                                                          '33.670666,-117.841553',
                                                                                          '1980/04/10', '2013/06/10',
                                                                                          [3.962399959564209, 1800.0],
                                                                                          datetime.date(2013, 6, 24),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(
                                                                                              b'First Lieutenant'),
                                                                                          None), (
                                                                                         'Megatron', None, 'None', 5, 5,
                                                                                         5.0, ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$', 5,
                                                                                         'Battle Station', 5, 5, None,
                                                                                         ['Metroflex'], None,
                                                                                         '1980/04/10', '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_count():
        actual_df = source_df.cols.count()
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding(16)
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_count_na():
        actual_df = source_df.cols.count_na('height(ft)')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding(2)
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_count_na_all_columns():
        actual_df = source_df.cols.count_na('*')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding(
            {'names': 1, 'height(ft)': 2, 'function': 1, 'rank': 1, 'age': 1, 'weight(t)': 2, 'japanese name': 1,
             'last position seen': 3, 'date arrival': 1, 'last date seen': 1, 'attributes': 1, 'Date Type': 1,
             'Tiemstamp': 1, 'Cybertronian': 1, 'function(binary)': 1, 'NullType': 7})
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_count_uniques():
        actual_df = source_df.cols.count_uniques('height(ft)')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding(5)
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_count_uniques_all_columns():
        actual_df = source_df.cols.count_uniques('*')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding(
            {'names': 5, 'height(ft)': 5, 'function': 6, 'rank': 3, 'age': 1, 'weight(t)': 5, 'japanese name': 6,
             'last position seen': 4, 'date arrival': 1, 'last date seen': 6, 'attributes': 6, 'Date Type': 6,
             'Tiemstamp': 1, 'Cybertronian': 1, 'function(binary)': 6, 'NullType': 0})
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_count_zeros():
        actual_df = source_df.cols.count_zeros('height(ft)')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding(0)
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_count_zeros_all_columns():
        actual_df = source_df.cols.count_zeros('*')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding({'height(ft)': 0, 'rank': 0, 'age': 0, 'weight(t)': 0})
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_date_transform():
        actual_df = source_df.cols.date_transform('date arrival', 'yyyy/MM/dd', 'dd-MM-YYYY')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("Optim'us", -28, 'Leader', 10,
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '10-04-1980', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         'bumbl#ebéé  ', 17,
                                                                                         'Espionage', 7, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '10-04-1980', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         (
                                                                                         'ironhide&', 26, 'Security', 7,
                                                                                         5000000, 4.0, ['Roadbuster'],
                                                                                         '37.789563,-122.400356',
                                                                                         '10-04-1980', '2014/07/10',
                                                                                         [7.924799919128418, 4000.0],
                                                                                         datetime.date(2014, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Security'), None),
                                                                                         (
                                                                                         'Jazz', 13, 'First Lieutenant',
                                                                                         8, 5000000, 1.7999999523162842,
                                                                                         ['Meister'],
                                                                                         '33.670666,-117.841553',
                                                                                         '10-04-1980', '2013/06/10',
                                                                                         [3.962399959564209, 1800.0],
                                                                                         datetime.date(2013, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'First Lieutenant'),
                                                                                         None), (
                                                                                         'Megatron', None, 'None', 10,
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '10-04-1980', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$', 300,
                                                                                         'Battle Station', 8, 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '10-04-1980', '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_date_transform_all_columns():
        actual_df = source_df.cols.date_transform(['date arrival', 'last date seen'], 'yyyy/MM/dd', 'dd-MM-YYYY')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("Optim'us", -28, 'Leader', 10,
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '10-04-1980', '10-09-2016',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         'bumbl#ebéé  ', 17,
                                                                                         'Espionage', 7, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '10-04-1980', '10-08-2015',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         (
                                                                                         'ironhide&', 26, 'Security', 7,
                                                                                         5000000, 4.0, ['Roadbuster'],
                                                                                         '37.789563,-122.400356',
                                                                                         '10-04-1980', '10-07-2014',
                                                                                         [7.924799919128418, 4000.0],
                                                                                         datetime.date(2014, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Security'), None),
                                                                                         (
                                                                                         'Jazz', 13, 'First Lieutenant',
                                                                                         8, 5000000, 1.7999999523162842,
                                                                                         ['Meister'],
                                                                                         '33.670666,-117.841553',
                                                                                         '10-04-1980', '10-06-2013',
                                                                                         [3.962399959564209, 1800.0],
                                                                                         datetime.date(2013, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'First Lieutenant'),
                                                                                         None), (
                                                                                         'Megatron', None, 'None', 10,
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '10-04-1980', '10-05-2012',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$', 300,
                                                                                         'Battle Station', 8, 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '10-04-1980', '10-04-2011',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_div():
        actual_df = source_df.cols.div(['height(ft)', 'rank'])
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', FloatType(), True), ('function', StringType(), True),
             ('rank', FloatType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True), ('div', DoubleType(), True)], [(
                                                                                                                      "Optim'us",
                                                                                                                      -28.0,
                                                                                                                      'Leader',
                                                                                                                      10.0,
                                                                                                                      5000000,
                                                                                                                      4.300000190734863,
                                                                                                                      [
                                                                                                                          'Inochi',
                                                                                                                          'Convoy'],
                                                                                                                      '19.442735,-99.201111',
                                                                                                                      '1980/04/10',
                                                                                                                      '2016/09/10',
                                                                                                                      [
                                                                                                                          8.53439998626709,
                                                                                                                          4300.0],
                                                                                                                      datetime.date(
                                                                                                                          2016,
                                                                                                                          9,
                                                                                                                          10),
                                                                                                                      datetime.datetime(
                                                                                                                          2014,
                                                                                                                          6,
                                                                                                                          24,
                                                                                                                          0,
                                                                                                                          0),
                                                                                                                      True,
                                                                                                                      bytearray(
                                                                                                                          b'Leader'),
                                                                                                                      None,
                                                                                                                      -2.8),
                                                                                                                      (
                                                                                                                      'bumbl#ebéé  ',
                                                                                                                      17.0,
                                                                                                                      'Espionage',
                                                                                                                      7.0,
                                                                                                                      5000000,
                                                                                                                      2.0,
                                                                                                                      [
                                                                                                                          'Bumble',
                                                                                                                          'Goldback'],
                                                                                                                      '10.642707,-71.612534',
                                                                                                                      '1980/04/10',
                                                                                                                      '2015/08/10',
                                                                                                                      [
                                                                                                                          5.334000110626221,
                                                                                                                          2000.0],
                                                                                                                      datetime.date(
                                                                                                                          2015,
                                                                                                                          8,
                                                                                                                          10),
                                                                                                                      datetime.datetime(
                                                                                                                          2014,
                                                                                                                          6,
                                                                                                                          24,
                                                                                                                          0,
                                                                                                                          0),
                                                                                                                      True,
                                                                                                                      bytearray(
                                                                                                                          b'Espionage'),
                                                                                                                      None,
                                                                                                                      2.4285714285714284),
                                                                                                                      (
                                                                                                                      'ironhide&',
                                                                                                                      26.0,
                                                                                                                      'Security',
                                                                                                                      7.0,
                                                                                                                      5000000,
                                                                                                                      4.0,
                                                                                                                      [
                                                                                                                          'Roadbuster'],
                                                                                                                      '37.789563,-122.400356',
                                                                                                                      '1980/04/10',
                                                                                                                      '2014/07/10',
                                                                                                                      [
                                                                                                                          7.924799919128418,
                                                                                                                          4000.0],
                                                                                                                      datetime.date(
                                                                                                                          2014,
                                                                                                                          6,
                                                                                                                          24),
                                                                                                                      datetime.datetime(
                                                                                                                          2014,
                                                                                                                          6,
                                                                                                                          24,
                                                                                                                          0,
                                                                                                                          0),
                                                                                                                      True,
                                                                                                                      bytearray(
                                                                                                                          b'Security'),
                                                                                                                      None,
                                                                                                                      3.7142857142857144),
                                                                                                                      (
                                                                                                                      'Jazz',
                                                                                                                      13.0,
                                                                                                                      'First Lieutenant',
                                                                                                                      8.0,
                                                                                                                      5000000,
                                                                                                                      1.7999999523162842,
                                                                                                                      [
                                                                                                                          'Meister'],
                                                                                                                      '33.670666,-117.841553',
                                                                                                                      '1980/04/10',
                                                                                                                      '2013/06/10',
                                                                                                                      [
                                                                                                                          3.962399959564209,
                                                                                                                          1800.0],
                                                                                                                      datetime.date(
                                                                                                                          2013,
                                                                                                                          6,
                                                                                                                          24),
                                                                                                                      datetime.datetime(
                                                                                                                          2014,
                                                                                                                          6,
                                                                                                                          24,
                                                                                                                          0,
                                                                                                                          0),
                                                                                                                      True,
                                                                                                                      bytearray(
                                                                                                                          b'First Lieutenant'),
                                                                                                                      None,
                                                                                                                      1.625),
                                                                                                                      (
                                                                                                                      'Megatron',
                                                                                                                      None,
                                                                                                                      'None',
                                                                                                                      10.0,
                                                                                                                      5000000,
                                                                                                                      5.699999809265137,
                                                                                                                      [
                                                                                                                          'Megatron'],
                                                                                                                      None,
                                                                                                                      '1980/04/10',
                                                                                                                      '2012/05/10',
                                                                                                                      [
                                                                                                                          None,
                                                                                                                          5700.0],
                                                                                                                      datetime.date(
                                                                                                                          2012,
                                                                                                                          5,
                                                                                                                          10),
                                                                                                                      datetime.datetime(
                                                                                                                          2014,
                                                                                                                          6,
                                                                                                                          24,
                                                                                                                          0,
                                                                                                                          0),
                                                                                                                      True,
                                                                                                                      bytearray(
                                                                                                                          b'None'),
                                                                                                                      None,
                                                                                                                      None),
                                                                                                                      (
                                                                                                                      'Metroplex_)^$',
                                                                                                                      300.0,
                                                                                                                      'Battle Station',
                                                                                                                      8.0,
                                                                                                                      5000000,
                                                                                                                      None,
                                                                                                                      [
                                                                                                                          'Metroflex'],
                                                                                                                      None,
                                                                                                                      '1980/04/10',
                                                                                                                      '2011/04/10',
                                                                                                                      [
                                                                                                                          91.44000244140625,
                                                                                                                          None],
                                                                                                                      datetime.date(
                                                                                                                          2011,
                                                                                                                          4,
                                                                                                                          10),
                                                                                                                      datetime.datetime(
                                                                                                                          2014,
                                                                                                                          6,
                                                                                                                          24,
                                                                                                                          0,
                                                                                                                          0),
                                                                                                                      True,
                                                                                                                      bytearray(
                                                                                                                          b'Battle Station'),
                                                                                                                      None,
                                                                                                                      37.5),
                                                                                                                      (
                                                                                                                      None,
                                                                                                                      None,
                                                                                                                      None,
                                                                                                                      None,
                                                                                                                      None,
                                                                                                                      None,
                                                                                                                      None,
                                                                                                                      None,
                                                                                                                      None,
                                                                                                                      None,
                                                                                                                      None,
                                                                                                                      None,
                                                                                                                      None,
                                                                                                                      None,
                                                                                                                      None,
                                                                                                                      None,
                                                                                                                      None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_div_all_columns():
        actual_df = source_df.cols.div('*')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', FloatType(), True), ('function', StringType(), True),
             ('rank', FloatType(), True), ('age', FloatType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True), ('div', DoubleType(), True)], [(
                                                                                                                      "Optim'us",
                                                                                                                      -28.0,
                                                                                                                      'Leader',
                                                                                                                      10.0,
                                                                                                                      5000000.0,
                                                                                                                      4.300000190734863,
                                                                                                                      [
                                                                                                                          'Inochi',
                                                                                                                          'Convoy'],
                                                                                                                      '19.442735,-99.201111',
                                                                                                                      '1980/04/10',
                                                                                                                      '2016/09/10',
                                                                                                                      [
                                                                                                                          8.53439998626709,
                                                                                                                          4300.0],
                                                                                                                      datetime.date(
                                                                                                                          2016,
                                                                                                                          9,
                                                                                                                          10),
                                                                                                                      datetime.datetime(
                                                                                                                          2014,
                                                                                                                          6,
                                                                                                                          24,
                                                                                                                          0,
                                                                                                                          0),
                                                                                                                      True,
                                                                                                                      bytearray(
                                                                                                                          b'Leader'),
                                                                                                                      None,
                                                                                                                      -1.302325523628167e-07),
                                                                                                                      (
                                                                                                                      'bumbl#ebéé  ',
                                                                                                                      17.0,
                                                                                                                      'Espionage',
                                                                                                                      7.0,
                                                                                                                      5000000.0,
                                                                                                                      2.0,
                                                                                                                      [
                                                                                                                          'Bumble',
                                                                                                                          'Goldback'],
                                                                                                                      '10.642707,-71.612534',
                                                                                                                      '1980/04/10',
                                                                                                                      '2015/08/10',
                                                                                                                      [
                                                                                                                          5.334000110626221,
                                                                                                                          2000.0],
                                                                                                                      datetime.date(
                                                                                                                          2015,
                                                                                                                          8,
                                                                                                                          10),
                                                                                                                      datetime.datetime(
                                                                                                                          2014,
                                                                                                                          6,
                                                                                                                          24,
                                                                                                                          0,
                                                                                                                          0),
                                                                                                                      True,
                                                                                                                      bytearray(
                                                                                                                          b'Espionage'),
                                                                                                                      None,
                                                                                                                      2.428571428571428e-07),
                                                                                                                      (
                                                                                                                      'ironhide&',
                                                                                                                      26.0,
                                                                                                                      'Security',
                                                                                                                      7.0,
                                                                                                                      5000000.0,
                                                                                                                      4.0,
                                                                                                                      [
                                                                                                                          'Roadbuster'],
                                                                                                                      '37.789563,-122.400356',
                                                                                                                      '1980/04/10',
                                                                                                                      '2014/07/10',
                                                                                                                      [
                                                                                                                          7.924799919128418,
                                                                                                                          4000.0],
                                                                                                                      datetime.date(
                                                                                                                          2014,
                                                                                                                          6,
                                                                                                                          24),
                                                                                                                      datetime.datetime(
                                                                                                                          2014,
                                                                                                                          6,
                                                                                                                          24,
                                                                                                                          0,
                                                                                                                          0),
                                                                                                                      True,
                                                                                                                      bytearray(
                                                                                                                          b'Security'),
                                                                                                                      None,
                                                                                                                      1.8571428571428572e-07),
                                                                                                                      (
                                                                                                                      'Jazz',
                                                                                                                      13.0,
                                                                                                                      'First Lieutenant',
                                                                                                                      8.0,
                                                                                                                      5000000.0,
                                                                                                                      1.7999999523162842,
                                                                                                                      [
                                                                                                                          'Meister'],
                                                                                                                      '33.670666,-117.841553',
                                                                                                                      '1980/04/10',
                                                                                                                      '2013/06/10',
                                                                                                                      [
                                                                                                                          3.962399959564209,
                                                                                                                          1800.0],
                                                                                                                      datetime.date(
                                                                                                                          2013,
                                                                                                                          6,
                                                                                                                          24),
                                                                                                                      datetime.datetime(
                                                                                                                          2014,
                                                                                                                          6,
                                                                                                                          24,
                                                                                                                          0,
                                                                                                                          0),
                                                                                                                      True,
                                                                                                                      bytearray(
                                                                                                                          b'First Lieutenant'),
                                                                                                                      None,
                                                                                                                      1.8055556033864447e-07),
                                                                                                                      (
                                                                                                                      'Megatron',
                                                                                                                      None,
                                                                                                                      'None',
                                                                                                                      10.0,
                                                                                                                      5000000.0,
                                                                                                                      5.699999809265137,
                                                                                                                      [
                                                                                                                          'Megatron'],
                                                                                                                      None,
                                                                                                                      '1980/04/10',
                                                                                                                      '2012/05/10',
                                                                                                                      [
                                                                                                                          None,
                                                                                                                          5700.0],
                                                                                                                      datetime.date(
                                                                                                                          2012,
                                                                                                                          5,
                                                                                                                          10),
                                                                                                                      datetime.datetime(
                                                                                                                          2014,
                                                                                                                          6,
                                                                                                                          24,
                                                                                                                          0,
                                                                                                                          0),
                                                                                                                      True,
                                                                                                                      bytearray(
                                                                                                                          b'None'),
                                                                                                                      None,
                                                                                                                      None),
                                                                                                                      (
                                                                                                                      'Metroplex_)^$',
                                                                                                                      300.0,
                                                                                                                      'Battle Station',
                                                                                                                      8.0,
                                                                                                                      5000000.0,
                                                                                                                      None,
                                                                                                                      [
                                                                                                                          'Metroflex'],
                                                                                                                      None,
                                                                                                                      '1980/04/10',
                                                                                                                      '2011/04/10',
                                                                                                                      [
                                                                                                                          91.44000244140625,
                                                                                                                          None],
                                                                                                                      datetime.date(
                                                                                                                          2011,
                                                                                                                          4,
                                                                                                                          10),
                                                                                                                      datetime.datetime(
                                                                                                                          2014,
                                                                                                                          6,
                                                                                                                          24,
                                                                                                                          0,
                                                                                                                          0),
                                                                                                                      True,
                                                                                                                      bytearray(
                                                                                                                          b'Battle Station'),
                                                                                                                      None,
                                                                                                                      None),
                                                                                                                      (
                                                                                                                      None,
                                                                                                                      None,
                                                                                                                      None,
                                                                                                                      None,
                                                                                                                      None,
                                                                                                                      None,
                                                                                                                      None,
                                                                                                                      None,
                                                                                                                      None,
                                                                                                                      None,
                                                                                                                      None,
                                                                                                                      None,
                                                                                                                      None,
                                                                                                                      None,
                                                                                                                      None,
                                                                                                                      None,
                                                                                                                      None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_drop():
        actual_df = source_df.cols.drop('rank')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("Optim'us", -28, 'Leader',
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         'bumbl#ebéé  ', 17,
                                                                                         'Espionage', 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         ('ironhide&', 26, 'Security',
                                                                                          5000000, 4.0, ['Roadbuster'],
                                                                                          '37.789563,-122.400356',
                                                                                          '1980/04/10', '2014/07/10',
                                                                                          [7.924799919128418, 4000.0],
                                                                                          datetime.date(2014, 6, 24),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Security'), None),
                                                                                         (
                                                                                         'Jazz', 13, 'First Lieutenant',
                                                                                         5000000, 1.7999999523162842,
                                                                                         ['Meister'],
                                                                                         '33.670666,-117.841553',
                                                                                         '1980/04/10', '2013/06/10',
                                                                                         [3.962399959564209, 1800.0],
                                                                                         datetime.date(2013, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'First Lieutenant'),
                                                                                         None), (
                                                                                         'Megatron', None, 'None',
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$', 300,
                                                                                         'Battle Station', 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '1980/04/10', '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_dtypes():
        actual_df = source_df.cols.dtypes('rank')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding('tinyint')
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_dtypes_all_columns():
        actual_df = source_df.cols.dtypes('*')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding(
            {'names': 'string', 'height(ft)': 'smallint', 'function': 'string', 'rank': 'tinyint', 'age': 'int',
             'weight(t)': 'float', 'japanese name': 'array<string>', 'last position seen': 'string',
             'date arrival': 'string', 'last date seen': 'string', 'attributes': 'array<float>', 'Date Type': 'date',
             'Tiemstamp': 'timestamp', 'Cybertronian': 'boolean', 'function(binary)': 'binary', 'NullType': 'null'})
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_fill_na():
        actual_df = source_df.cols.fill_na('height(ft)', '1')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', DoubleType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("Optim'us", -28.0, 'Leader',
                                                                                          10, 5000000,
                                                                                          4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         'bumbl#ebéé  ', 17.0,
                                                                                         'Espionage', 7, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         ('ironhide&', 26.0, 'Security',
                                                                                          7, 5000000, 4.0,
                                                                                          ['Roadbuster'],
                                                                                          '37.789563,-122.400356',
                                                                                          '1980/04/10', '2014/07/10',
                                                                                          [7.924799919128418, 4000.0],
                                                                                          datetime.date(2014, 6, 24),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Security'), None),
                                                                                         ('Jazz', 13.0,
                                                                                          'First Lieutenant', 8,
                                                                                          5000000, 1.7999999523162842,
                                                                                          ['Meister'],
                                                                                          '33.670666,-117.841553',
                                                                                          '1980/04/10', '2013/06/10',
                                                                                          [3.962399959564209, 1800.0],
                                                                                          datetime.date(2013, 6, 24),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(
                                                                                              b'First Lieutenant'),
                                                                                          None), (
                                                                                         'Megatron', 1.0, 'None', 10,
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$', 300.0,
                                                                                         'Battle Station', 8, 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '1980/04/10', '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, 1.0, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_fill_na_all_columns():
        actual_df = source_df.cols.fill_na(['names', 'height(ft)', 'function', 'rank', 'age'], '2')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', DoubleType(), True), ('function', StringType(), True),
             ('rank', DoubleType(), True), ('age', DoubleType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("Optim'us", -28.0, 'Leader',
                                                                                          10.0, 5000000.0,
                                                                                          4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         'bumbl#ebéé  ', 17.0,
                                                                                         'Espionage', 7.0, 5000000.0,
                                                                                         2.0, ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         ('ironhide&', 26.0, 'Security',
                                                                                          7.0, 5000000.0, 4.0,
                                                                                          ['Roadbuster'],
                                                                                          '37.789563,-122.400356',
                                                                                          '1980/04/10', '2014/07/10',
                                                                                          [7.924799919128418, 4000.0],
                                                                                          datetime.date(2014, 6, 24),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Security'), None),
                                                                                         ('Jazz', 13.0,
                                                                                          'First Lieutenant', 8.0,
                                                                                          5000000.0, 1.7999999523162842,
                                                                                          ['Meister'],
                                                                                          '33.670666,-117.841553',
                                                                                          '1980/04/10', '2013/06/10',
                                                                                          [3.962399959564209, 1800.0],
                                                                                          datetime.date(2013, 6, 24),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(
                                                                                              b'First Lieutenant'),
                                                                                          None), (
                                                                                         'Megatron', 2.0, 'None', 10.0,
                                                                                         5000000.0, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$', 300.0,
                                                                                         'Battle Station', 8.0,
                                                                                         5000000.0, None, ['Metroflex'],
                                                                                         None, '1980/04/10',
                                                                                         '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         '2', 2.0, '2', 2.0, 2.0, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_fill_na_array():
        actual_df = source_df.cols.fill_na('Cybertronian', True)
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("Optim'us", -28, 'Leader', 10,
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         'bumbl#ebéé  ', 17,
                                                                                         'Espionage', 7, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         (
                                                                                         'ironhide&', 26, 'Security', 7,
                                                                                         5000000, 4.0, ['Roadbuster'],
                                                                                         '37.789563,-122.400356',
                                                                                         '1980/04/10', '2014/07/10',
                                                                                         [7.924799919128418, 4000.0],
                                                                                         datetime.date(2014, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Security'), None),
                                                                                         (
                                                                                         'Jazz', 13, 'First Lieutenant',
                                                                                         8, 5000000, 1.7999999523162842,
                                                                                         ['Meister'],
                                                                                         '33.670666,-117.841553',
                                                                                         '1980/04/10', '2013/06/10',
                                                                                         [3.962399959564209, 1800.0],
                                                                                         datetime.date(2013, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'First Lieutenant'),
                                                                                         None), (
                                                                                         'Megatron', None, 'None', 10,
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$', 300,
                                                                                         'Battle Station', 8, 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '1980/04/10', '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, True, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_fill_na_bool():
        actual_df = source_df.cols.fill_na('Cybertronian', False)
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("Optim'us", -28, 'Leader', 10,
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         'bumbl#ebéé  ', 17,
                                                                                         'Espionage', 7, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         (
                                                                                         'ironhide&', 26, 'Security', 7,
                                                                                         5000000, 4.0, ['Roadbuster'],
                                                                                         '37.789563,-122.400356',
                                                                                         '1980/04/10', '2014/07/10',
                                                                                         [7.924799919128418, 4000.0],
                                                                                         datetime.date(2014, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Security'), None),
                                                                                         (
                                                                                         'Jazz', 13, 'First Lieutenant',
                                                                                         8, 5000000, 1.7999999523162842,
                                                                                         ['Meister'],
                                                                                         '33.670666,-117.841553',
                                                                                         '1980/04/10', '2013/06/10',
                                                                                         [3.962399959564209, 1800.0],
                                                                                         datetime.date(2013, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'First Lieutenant'),
                                                                                         None), (
                                                                                         'Megatron', None, 'None', 10,
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$', 300,
                                                                                         'Battle Station', 8, 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '1980/04/10', '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, False, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_frequency():
        actual_df = source_df.cols.frequency('rank', 4)
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding({'rank': [{'value': 10, 'count': 2}, {'value': 8, 'count': 2},
                                                  {'value': 7, 'count': 2}, {'value': None, 'count': 1}]})
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_frequency_all_columns():
        actual_df = source_df.cols.frequency('*', 4)
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding({'names': [{'value': 'ironhide&', 'count': 1},
                                                   {'value': 'bumbl#ebéé  ', 'count': 1},
                                                   {'value': "Optim'us", 'count': 1},
                                                   {'value': 'Metroplex_)^$', 'count': 1}],
                                         'height(ft)': [{'value': None, 'count': 2}, {'value': 300, 'count': 1},
                                                        {'value': 26, 'count': 1}, {'value': 17, 'count': 1}],
                                         'function': [{'value': 'Security', 'count': 1}, {'value': 'None', 'count': 1},
                                                      {'value': 'Leader', 'count': 1},
                                                      {'value': 'First Lieutenant', 'count': 1}],
                                         'rank': [{'value': 10, 'count': 2}, {'value': 8, 'count': 2},
                                                  {'value': 7, 'count': 2}, {'value': None, 'count': 1}],
                                         'age': [{'value': 5000000, 'count': 6}, {'value': None, 'count': 1}],
                                         'weight(t)': [{'value': None, 'count': 2},
                                                       {'value': 5.699999809265137, 'count': 1},
                                                       {'value': 4.300000190734863, 'count': 1},
                                                       {'value': 4.0, 'count': 1}],
                                         'japanese name': [{'value': ['Roadbuster'], 'count': 1},
                                                           {'value': ['Metroflex'], 'count': 1},
                                                           {'value': ['Meister'], 'count': 1},
                                                           {'value': ['Megatron'], 'count': 1}],
                                         'last position seen': [{'value': None, 'count': 3},
                                                                {'value': '37.789563,-122.400356', 'count': 1},
                                                                {'value': '33.670666,-117.841553', 'count': 1},
                                                                {'value': '19.442735,-99.201111', 'count': 1}],
                                         'date arrival': [{'value': '1980/04/10', 'count': 6},
                                                          {'value': None, 'count': 1}],
                                         'last date seen': [{'value': '2016/09/10', 'count': 1},
                                                            {'value': '2015/08/10', 'count': 1},
                                                            {'value': '2014/07/10', 'count': 1},
                                                            {'value': '2013/06/10', 'count': 1}],
                                         'attributes': [{'value': [91.44000244140625, None], 'count': 1},
                                                        {'value': [8.53439998626709, 4300.0], 'count': 1},
                                                        {'value': [7.924799919128418, 4000.0], 'count': 1},
                                                        {'value': [5.334000110626221, 2000.0], 'count': 1}],
                                         'Date Type': [{'value': '2016-09-10', 'count': 1},
                                                       {'value': '2015-08-10', 'count': 1},
                                                       {'value': '2014-06-24', 'count': 1},
                                                       {'value': '2013-06-24', 'count': 1}],
                                         'Tiemstamp': [{'value': '2014-06-24 00:00:00', 'count': 6},
                                                       {'value': None, 'count': 1}],
                                         'Cybertronian': [{'value': True, 'count': 6}, {'value': None, 'count': 1}],
                                         'function(binary)': [{'value': None, 'count': 1}, {'value': None, 'count': 1},
                                                              {'value': None, 'count': 1}, {'value': None, 'count': 1}],
                                         'NullType': [{'value': None, 'count': 7}]})
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_hist():
        actual_df = source_df.cols.hist('rank', 4)
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding(
            [{'count': 2, 'lower': 7.0, 'upper': 7.75}, {'count': 2, 'lower': 7.75, 'upper': 8.5},
             {'count': 0, 'lower': 8.5, 'upper': 9.25}, {'count': 2, 'lower': 9.25, 'upper': 10.0}])
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_impute():
        actual_df = source_df.cols.impute('rank')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', FloatType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("Optim'us", -28, 'Leader',
                                                                                          10.0, 5000000,
                                                                                          4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         'bumbl#ebéé  ', 17,
                                                                                         'Espionage', 7.0, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         ('ironhide&', 26, 'Security',
                                                                                          7.0, 5000000, 4.0,
                                                                                          ['Roadbuster'],
                                                                                          '37.789563,-122.400356',
                                                                                          '1980/04/10', '2014/07/10',
                                                                                          [7.924799919128418, 4000.0],
                                                                                          datetime.date(2014, 6, 24),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Security'), None),
                                                                                         (
                                                                                         'Jazz', 13, 'First Lieutenant',
                                                                                         8.0, 5000000,
                                                                                         1.7999999523162842,
                                                                                         ['Meister'],
                                                                                         '33.670666,-117.841553',
                                                                                         '1980/04/10', '2013/06/10',
                                                                                         [3.962399959564209, 1800.0],
                                                                                         datetime.date(2013, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'First Lieutenant'),
                                                                                         None), (
                                                                                         'Megatron', None, 'None', 10.0,
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$', 300,
                                                                                         'Battle Station', 8.0, 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '1980/04/10', '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (None, None, None,
                                                                                                 8.333333015441895,
                                                                                                 None, None, None, None,
                                                                                                 None, None, None, None,
                                                                                                 None, None, None,
                                                                                                 None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_impute_all_columns():
        actual_df = source_df.cols.impute('names', 'categorical')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("Optim'us", -28, 'Leader', 10,
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         'bumbl#ebéé  ', 17,
                                                                                         'Espionage', 7, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         (
                                                                                         'ironhide&', 26, 'Security', 7,
                                                                                         5000000, 4.0, ['Roadbuster'],
                                                                                         '37.789563,-122.400356',
                                                                                         '1980/04/10', '2014/07/10',
                                                                                         [7.924799919128418, 4000.0],
                                                                                         datetime.date(2014, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Security'), None),
                                                                                         (
                                                                                         'Jazz', 13, 'First Lieutenant',
                                                                                         8, 5000000, 1.7999999523162842,
                                                                                         ['Meister'],
                                                                                         '33.670666,-117.841553',
                                                                                         '1980/04/10', '2013/06/10',
                                                                                         [3.962399959564209, 1800.0],
                                                                                         datetime.date(2013, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'First Lieutenant'),
                                                                                         None), (
                                                                                         'Megatron', None, 'None', 10,
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$', 300,
                                                                                         'Battle Station', 8, 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '1980/04/10', '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         'None', None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_iqr():
        actual_df = source_df.cols.iqr('height(ft)')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding(13.0)
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_iqr_all_columns():
        actual_df = source_df.cols.iqr('*')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding({'height(ft)': 13.0, 'rank': 3.0, 'age': 0.0, 'weight(t)': 2.3000001907348633})
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_is_na():
        actual_df = source_df.cols.is_na('height(ft)')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', BooleanType(), False), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("Optim'us", False, 'Leader',
                                                                                          10, 5000000,
                                                                                          4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         'bumbl#ebéé  ', False,
                                                                                         'Espionage', 7, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         (
                                                                                         'ironhide&', False, 'Security',
                                                                                         7, 5000000, 4.0,
                                                                                         ['Roadbuster'],
                                                                                         '37.789563,-122.400356',
                                                                                         '1980/04/10', '2014/07/10',
                                                                                         [7.924799919128418, 4000.0],
                                                                                         datetime.date(2014, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Security'), None),
                                                                                         ('Jazz', False,
                                                                                          'First Lieutenant', 8,
                                                                                          5000000, 1.7999999523162842,
                                                                                          ['Meister'],
                                                                                          '33.670666,-117.841553',
                                                                                          '1980/04/10', '2013/06/10',
                                                                                          [3.962399959564209, 1800.0],
                                                                                          datetime.date(2013, 6, 24),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(
                                                                                              b'First Lieutenant'),
                                                                                          None), (
                                                                                         'Megatron', True, 'None', 10,
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$', False,
                                                                                         'Battle Station', 8, 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '1980/04/10', '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, True, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_is_na_all_columns():
        actual_df = source_df.cols.is_na('*')
        expected_df = op.create.df(
            [('names', BooleanType(), False), ('height(ft)', BooleanType(), False), ('function', BooleanType(), False),
             ('rank', BooleanType(), False), ('age', BooleanType(), False), ('weight(t)', BooleanType(), False),
             ('japanese name', BooleanType(), False), ('last position seen', BooleanType(), False),
             ('date arrival', BooleanType(), False), ('last date seen', BooleanType(), False),
             ('attributes', BooleanType(), False), ('Date Type', BooleanType(), False),
             ('Tiemstamp', BooleanType(), False), ('Cybertronian', BooleanType(), False),
             ('function(binary)', BooleanType(), False), ('NullType', BooleanType(), False)], [(False, False, False,
                                                                                                False, False, False,
                                                                                                False, False, False,
                                                                                                False, False, False,
                                                                                                False, False, False,
                                                                                                True), (
                                                                                               False, False, False,
                                                                                               False, False, False,
                                                                                               False, False, False,
                                                                                               False, False, False,
                                                                                               False, False, False,
                                                                                               True), (
                                                                                               False, False, False,
                                                                                               False, False, False,
                                                                                               False, False, False,
                                                                                               False, False, False,
                                                                                               False, False, False,
                                                                                               True), (
                                                                                               False, False, False,
                                                                                               False, False, False,
                                                                                               False, False, False,
                                                                                               False, False, False,
                                                                                               False, False, False,
                                                                                               True), (
                                                                                               False, True, False,
                                                                                               False, False, False,
                                                                                               False, True, False,
                                                                                               False, False, False,
                                                                                               False, False, False,
                                                                                               True), (
                                                                                               False, False, False,
                                                                                               False, False, True,
                                                                                               False, True, False,
                                                                                               False, False, False,
                                                                                               False, False, False,
                                                                                               True), (
                                                                                               True, True, True, True,
                                                                                               True, True, True, True,
                                                                                               True, True, True, True,
                                                                                               True, True, True, True)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_keep():
        actual_df = source_df.cols.keep('rank')
        expected_df = op.create.df([('rank', ByteType(), True)], [(10,), (7,), (7,), (8,), (10,), (8,), (None,)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_kurt():
        actual_df = source_df.cols.kurt('height(ft)')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding(0.13863)
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_kurt_all_columns():
        actual_df = source_df.cols.kurt('*')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding({'height(ft)': 0.13863, 'rank': -1.5, 'age': nan, 'weight(t)': -1.43641})
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_lower():
        actual_df = source_df.cols.lower('function')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("Optim'us", -28, 'leader', 10,
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         'bumbl#ebéé  ', 17,
                                                                                         'espionage', 7, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         (
                                                                                         'ironhide&', 26, 'security', 7,
                                                                                         5000000, 4.0, ['Roadbuster'],
                                                                                         '37.789563,-122.400356',
                                                                                         '1980/04/10', '2014/07/10',
                                                                                         [7.924799919128418, 4000.0],
                                                                                         datetime.date(2014, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Security'), None),
                                                                                         (
                                                                                         'Jazz', 13, 'first lieutenant',
                                                                                         8, 5000000, 1.7999999523162842,
                                                                                         ['Meister'],
                                                                                         '33.670666,-117.841553',
                                                                                         '1980/04/10', '2013/06/10',
                                                                                         [3.962399959564209, 1800.0],
                                                                                         datetime.date(2013, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'First Lieutenant'),
                                                                                         None), (
                                                                                         'Megatron', None, 'none', 10,
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$', 300,
                                                                                         'battle station', 8, 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '1980/04/10', '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_lower_all_columns():
        actual_df = source_df.cols.lower('*')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("optim'us", -28, 'leader', 10,
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         'bumbl#ebéé  ', 17,
                                                                                         'espionage', 7, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         (
                                                                                         'ironhide&', 26, 'security', 7,
                                                                                         5000000, 4.0, ['Roadbuster'],
                                                                                         '37.789563,-122.400356',
                                                                                         '1980/04/10', '2014/07/10',
                                                                                         [7.924799919128418, 4000.0],
                                                                                         datetime.date(2014, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Security'), None),
                                                                                         (
                                                                                         'jazz', 13, 'first lieutenant',
                                                                                         8, 5000000, 1.7999999523162842,
                                                                                         ['Meister'],
                                                                                         '33.670666,-117.841553',
                                                                                         '1980/04/10', '2013/06/10',
                                                                                         [3.962399959564209, 1800.0],
                                                                                         datetime.date(2013, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'First Lieutenant'),
                                                                                         None), (
                                                                                         'megatron', None, 'none', 10,
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'metroplex_)^$', 300,
                                                                                         'battle station', 8, 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '1980/04/10', '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_mad():
        actual_df = source_df.cols.mad('height(ft)')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding(0.0)
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_mad_all_columns():
        actual_df = source_df.cols.mad('*')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding({'height(ft)': 0.0, 'rank': 0.0, 'age': 0.0, 'weight(t)': 0.0})
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_max():
        actual_df = source_df.cols.max('height(ft)')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding(300)
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_max_all_columns():
        actual_df = source_df.cols.max('*')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding(
            {'names': 'ironhide&', 'height(ft)': 300, 'function': 'Security', 'rank': 10, 'age': 5000000,
             'weight(t)': 5.7, 'japanese name': ['Roadbuster'], 'last position seen': '37.789563,-122.400356',
             'date arrival': '1980/04/10', 'last date seen': '2016/09/10', 'attributes': [91.44000244140625, None],
             'Date Type': '2016-09-10', 'Tiemstamp': '2014-06-24 00:00:00', 'Cybertronian': 1, 'function(binary)': None,
             'NullType': None})
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_mean():
        actual_df = source_df.cols.mean('height(ft)')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding(65.6)
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_mean_all_columns():
        actual_df = source_df.cols.mean('*')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding({'height(ft)': 65.6, 'rank': 8.33333, 'age': 5000000.0, 'weight(t)': 3.56})
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_median():
        actual_df = source_df.cols.median('height(ft)')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding(-28.0)
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_median_all_columns():
        actual_df = source_df.cols.median('*')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding(
            {'height(ft)': -28.0, 'rank': 7.0, 'age': 5000000.0, 'weight(t)': 1.7999999523162842})
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_min():
        actual_df = source_df.cols.min('height(ft)')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding(-28)
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_min_all_columns():
        actual_df = source_df.cols.min('*')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding(
            {'names': 'Jazz', 'height(ft)': -28, 'function': 'Battle Station', 'rank': 7, 'age': 5000000,
             'weight(t)': 1.8, 'japanese name': ['Bumble', 'Goldback'], 'last position seen': '10.642707,-71.612534',
             'date arrival': '1980/04/10', 'last date seen': '2011/04/10', 'attributes': [None, 5700.0],
             'Date Type': '2011-04-10', 'Tiemstamp': '2014-06-24 00:00:00', 'Cybertronian': 1, 'function(binary)': None,
             'NullType': None})
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_mode():
        actual_df = source_df.cols.mode('height(ft)')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding(None)
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_mode_all_columns():
        actual_df = source_df.cols.mode('*')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding(
            [{'names': None}, {'height(ft)': None}, {'function': None}, {'rank': [8, 7, 10]}, {'age': 5000000},
             {'weight(t)': None}, {'japanese name': None}, {'last position seen': None}, {'date arrival': '1980/04/10'},
             {'last date seen': None}, {'attributes': None}, {'Date Type': None},
             {'Tiemstamp': datetime.datetime(2014, 6, 24, 0, 0)}, {'Cybertronian': True}, {'function(binary)': None},
             {'NullType': None}])
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_move_after():
        actual_df = source_df.cols.move('rank', 'after', 'attributes')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('rank', ByteType(), True),
             ('Date Type', DateType(), True), ('Tiemstamp', TimestampType(), True),
             ('Cybertronian', BooleanType(), True), ('function(binary)', BinaryType(), True),
             ('NullType', NullType(), True)], [("Optim'us", -28, 'Leader', 5000000, 4.300000190734863,
                                                ['Inochi', 'Convoy'], '19.442735,-99.201111', '1980/04/10',
                                                '2016/09/10', [8.53439998626709, 4300.0], 10,
                                                datetime.date(2016, 9, 10), datetime.datetime(2014, 6, 24, 0, 0), True,
                                                bytearray(b'Leader'), None), (
                                               'bumbl#ebéé  ', 17, 'Espionage', 5000000, 2.0, ['Bumble', 'Goldback'],
                                               '10.642707,-71.612534', '1980/04/10', '2015/08/10',
                                               [5.334000110626221, 2000.0], 7, datetime.date(2015, 8, 10),
                                               datetime.datetime(2014, 6, 24, 0, 0), True, bytearray(b'Espionage'),
                                               None), ('ironhide&', 26, 'Security', 5000000, 4.0, ['Roadbuster'],
                                                       '37.789563,-122.400356', '1980/04/10', '2014/07/10',
                                                       [7.924799919128418, 4000.0], 7, datetime.date(2014, 6, 24),
                                                       datetime.datetime(2014, 6, 24, 0, 0), True,
                                                       bytearray(b'Security'), None), (
                                               'Jazz', 13, 'First Lieutenant', 5000000, 1.7999999523162842, ['Meister'],
                                               '33.670666,-117.841553', '1980/04/10', '2013/06/10',
                                               [3.962399959564209, 1800.0], 8, datetime.date(2013, 6, 24),
                                               datetime.datetime(2014, 6, 24, 0, 0), True,
                                               bytearray(b'First Lieutenant'), None), (
                                               'Megatron', None, 'None', 5000000, 5.699999809265137, ['Megatron'], None,
                                               '1980/04/10', '2012/05/10', [None, 5700.0], 10,
                                               datetime.date(2012, 5, 10), datetime.datetime(2014, 6, 24, 0, 0), True,
                                               bytearray(b'None'), None), (
                                               'Metroplex_)^$', 300, 'Battle Station', 5000000, None, ['Metroflex'],
                                               None, '1980/04/10', '2011/04/10', [91.44000244140625, None], 8,
                                               datetime.date(2011, 4, 10), datetime.datetime(2014, 6, 24, 0, 0), True,
                                               bytearray(b'Battle Station'), None), (
                                               None, None, None, None, None, None, None, None, None, None, None, None,
                                               None, None, None, None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_move_before():
        actual_df = source_df.cols.move('rank', 'before', 'attributes')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True), ('rank', ByteType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("Optim'us", -28, 'Leader',
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          10,
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         'bumbl#ebéé  ', 17,
                                                                                         'Espionage', 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10', 7,
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         ('ironhide&', 26, 'Security',
                                                                                          5000000, 4.0, ['Roadbuster'],
                                                                                          '37.789563,-122.400356',
                                                                                          '1980/04/10', '2014/07/10', 7,
                                                                                          [7.924799919128418, 4000.0],
                                                                                          datetime.date(2014, 6, 24),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Security'), None),
                                                                                         (
                                                                                         'Jazz', 13, 'First Lieutenant',
                                                                                         5000000, 1.7999999523162842,
                                                                                         ['Meister'],
                                                                                         '33.670666,-117.841553',
                                                                                         '1980/04/10', '2013/06/10', 8,
                                                                                         [3.962399959564209, 1800.0],
                                                                                         datetime.date(2013, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'First Lieutenant'),
                                                                                         None), (
                                                                                         'Megatron', None, 'None',
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10', 10,
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$', 300,
                                                                                         'Battle Station', 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '1980/04/10', '2011/04/10', 8,
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_move_beginning():
        actual_df = source_df.cols.move('rank', 'beginning')
        expected_df = op.create.df(
            [('rank', ByteType(), True), ('names', StringType(), True), ('height(ft)', ShortType(), True),
             ('function', StringType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [(10, "Optim'us", -28, 'Leader',
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         7, 'bumbl#ebéé  ', 17,
                                                                                         'Espionage', 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         (
                                                                                         7, 'ironhide&', 26, 'Security',
                                                                                         5000000, 4.0, ['Roadbuster'],
                                                                                         '37.789563,-122.400356',
                                                                                         '1980/04/10', '2014/07/10',
                                                                                         [7.924799919128418, 4000.0],
                                                                                         datetime.date(2014, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Security'), None),
                                                                                         (8, 'Jazz', 13,
                                                                                          'First Lieutenant', 5000000,
                                                                                          1.7999999523162842,
                                                                                          ['Meister'],
                                                                                          '33.670666,-117.841553',
                                                                                          '1980/04/10', '2013/06/10',
                                                                                          [3.962399959564209, 1800.0],
                                                                                          datetime.date(2013, 6, 24),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(
                                                                                              b'First Lieutenant'),
                                                                                          None), (
                                                                                         10, 'Megatron', None, 'None',
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         8, 'Metroplex_)^$', 300,
                                                                                         'Battle Station', 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '1980/04/10', '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_move_end():
        actual_df = source_df.cols.move('rank', 'end')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True), ('rank', ByteType(), True)], [(
                                                                                                                     "Optim'us",
                                                                                                                     -28,
                                                                                                                     'Leader',
                                                                                                                     5000000,
                                                                                                                     4.300000190734863,
                                                                                                                     [
                                                                                                                         'Inochi',
                                                                                                                         'Convoy'],
                                                                                                                     '19.442735,-99.201111',
                                                                                                                     '1980/04/10',
                                                                                                                     '2016/09/10',
                                                                                                                     [
                                                                                                                         8.53439998626709,
                                                                                                                         4300.0],
                                                                                                                     datetime.date(
                                                                                                                         2016,
                                                                                                                         9,
                                                                                                                         10),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'Leader'),
                                                                                                                     None,
                                                                                                                     10),
                                                                                                                     (
                                                                                                                     'bumbl#ebéé  ',
                                                                                                                     17,
                                                                                                                     'Espionage',
                                                                                                                     5000000,
                                                                                                                     2.0,
                                                                                                                     [
                                                                                                                         'Bumble',
                                                                                                                         'Goldback'],
                                                                                                                     '10.642707,-71.612534',
                                                                                                                     '1980/04/10',
                                                                                                                     '2015/08/10',
                                                                                                                     [
                                                                                                                         5.334000110626221,
                                                                                                                         2000.0],
                                                                                                                     datetime.date(
                                                                                                                         2015,
                                                                                                                         8,
                                                                                                                         10),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'Espionage'),
                                                                                                                     None,
                                                                                                                     7),
                                                                                                                     (
                                                                                                                     'ironhide&',
                                                                                                                     26,
                                                                                                                     'Security',
                                                                                                                     5000000,
                                                                                                                     4.0,
                                                                                                                     [
                                                                                                                         'Roadbuster'],
                                                                                                                     '37.789563,-122.400356',
                                                                                                                     '1980/04/10',
                                                                                                                     '2014/07/10',
                                                                                                                     [
                                                                                                                         7.924799919128418,
                                                                                                                         4000.0],
                                                                                                                     datetime.date(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'Security'),
                                                                                                                     None,
                                                                                                                     7),
                                                                                                                     (
                                                                                                                     'Jazz',
                                                                                                                     13,
                                                                                                                     'First Lieutenant',
                                                                                                                     5000000,
                                                                                                                     1.7999999523162842,
                                                                                                                     [
                                                                                                                         'Meister'],
                                                                                                                     '33.670666,-117.841553',
                                                                                                                     '1980/04/10',
                                                                                                                     '2013/06/10',
                                                                                                                     [
                                                                                                                         3.962399959564209,
                                                                                                                         1800.0],
                                                                                                                     datetime.date(
                                                                                                                         2013,
                                                                                                                         6,
                                                                                                                         24),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'First Lieutenant'),
                                                                                                                     None,
                                                                                                                     8),
                                                                                                                     (
                                                                                                                     'Megatron',
                                                                                                                     None,
                                                                                                                     'None',
                                                                                                                     5000000,
                                                                                                                     5.699999809265137,
                                                                                                                     [
                                                                                                                         'Megatron'],
                                                                                                                     None,
                                                                                                                     '1980/04/10',
                                                                                                                     '2012/05/10',
                                                                                                                     [
                                                                                                                         None,
                                                                                                                         5700.0],
                                                                                                                     datetime.date(
                                                                                                                         2012,
                                                                                                                         5,
                                                                                                                         10),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'None'),
                                                                                                                     None,
                                                                                                                     10),
                                                                                                                     (
                                                                                                                     'Metroplex_)^$',
                                                                                                                     300,
                                                                                                                     'Battle Station',
                                                                                                                     5000000,
                                                                                                                     None,
                                                                                                                     [
                                                                                                                         'Metroflex'],
                                                                                                                     None,
                                                                                                                     '1980/04/10',
                                                                                                                     '2011/04/10',
                                                                                                                     [
                                                                                                                         91.44000244140625,
                                                                                                                         None],
                                                                                                                     datetime.date(
                                                                                                                         2011,
                                                                                                                         4,
                                                                                                                         10),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'Battle Station'),
                                                                                                                     None,
                                                                                                                     8),
                                                                                                                     (
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_mul():
        actual_df = source_df.cols.mul(['height(ft)', 'rank'])
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', FloatType(), True), ('function', StringType(), True),
             ('rank', FloatType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True), ('mul', FloatType(), True)], [(
                                                                                                                     "Optim'us",
                                                                                                                     -28.0,
                                                                                                                     'Leader',
                                                                                                                     10.0,
                                                                                                                     5000000,
                                                                                                                     4.300000190734863,
                                                                                                                     [
                                                                                                                         'Inochi',
                                                                                                                         'Convoy'],
                                                                                                                     '19.442735,-99.201111',
                                                                                                                     '1980/04/10',
                                                                                                                     '2016/09/10',
                                                                                                                     [
                                                                                                                         8.53439998626709,
                                                                                                                         4300.0],
                                                                                                                     datetime.date(
                                                                                                                         2016,
                                                                                                                         9,
                                                                                                                         10),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'Leader'),
                                                                                                                     None,
                                                                                                                     -280.0),
                                                                                                                     (
                                                                                                                     'bumbl#ebéé  ',
                                                                                                                     17.0,
                                                                                                                     'Espionage',
                                                                                                                     7.0,
                                                                                                                     5000000,
                                                                                                                     2.0,
                                                                                                                     [
                                                                                                                         'Bumble',
                                                                                                                         'Goldback'],
                                                                                                                     '10.642707,-71.612534',
                                                                                                                     '1980/04/10',
                                                                                                                     '2015/08/10',
                                                                                                                     [
                                                                                                                         5.334000110626221,
                                                                                                                         2000.0],
                                                                                                                     datetime.date(
                                                                                                                         2015,
                                                                                                                         8,
                                                                                                                         10),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'Espionage'),
                                                                                                                     None,
                                                                                                                     119.0),
                                                                                                                     (
                                                                                                                     'ironhide&',
                                                                                                                     26.0,
                                                                                                                     'Security',
                                                                                                                     7.0,
                                                                                                                     5000000,
                                                                                                                     4.0,
                                                                                                                     [
                                                                                                                         'Roadbuster'],
                                                                                                                     '37.789563,-122.400356',
                                                                                                                     '1980/04/10',
                                                                                                                     '2014/07/10',
                                                                                                                     [
                                                                                                                         7.924799919128418,
                                                                                                                         4000.0],
                                                                                                                     datetime.date(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'Security'),
                                                                                                                     None,
                                                                                                                     182.0),
                                                                                                                     (
                                                                                                                     'Jazz',
                                                                                                                     13.0,
                                                                                                                     'First Lieutenant',
                                                                                                                     8.0,
                                                                                                                     5000000,
                                                                                                                     1.7999999523162842,
                                                                                                                     [
                                                                                                                         'Meister'],
                                                                                                                     '33.670666,-117.841553',
                                                                                                                     '1980/04/10',
                                                                                                                     '2013/06/10',
                                                                                                                     [
                                                                                                                         3.962399959564209,
                                                                                                                         1800.0],
                                                                                                                     datetime.date(
                                                                                                                         2013,
                                                                                                                         6,
                                                                                                                         24),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'First Lieutenant'),
                                                                                                                     None,
                                                                                                                     104.0),
                                                                                                                     (
                                                                                                                     'Megatron',
                                                                                                                     None,
                                                                                                                     'None',
                                                                                                                     10.0,
                                                                                                                     5000000,
                                                                                                                     5.699999809265137,
                                                                                                                     [
                                                                                                                         'Megatron'],
                                                                                                                     None,
                                                                                                                     '1980/04/10',
                                                                                                                     '2012/05/10',
                                                                                                                     [
                                                                                                                         None,
                                                                                                                         5700.0],
                                                                                                                     datetime.date(
                                                                                                                         2012,
                                                                                                                         5,
                                                                                                                         10),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'None'),
                                                                                                                     None,
                                                                                                                     None),
                                                                                                                     (
                                                                                                                     'Metroplex_)^$',
                                                                                                                     300.0,
                                                                                                                     'Battle Station',
                                                                                                                     8.0,
                                                                                                                     5000000,
                                                                                                                     None,
                                                                                                                     [
                                                                                                                         'Metroflex'],
                                                                                                                     None,
                                                                                                                     '1980/04/10',
                                                                                                                     '2011/04/10',
                                                                                                                     [
                                                                                                                         91.44000244140625,
                                                                                                                         None],
                                                                                                                     datetime.date(
                                                                                                                         2011,
                                                                                                                         4,
                                                                                                                         10),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'Battle Station'),
                                                                                                                     None,
                                                                                                                     2400.0),
                                                                                                                     (
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_mul_all_columns():
        actual_df = source_df.cols.mul('*')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', FloatType(), True), ('function', StringType(), True),
             ('rank', FloatType(), True), ('age', FloatType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True), ('mul', FloatType(), True)], [(
                                                                                                                     "Optim'us",
                                                                                                                     -28.0,
                                                                                                                     'Leader',
                                                                                                                     10.0,
                                                                                                                     5000000.0,
                                                                                                                     4.300000190734863,
                                                                                                                     [
                                                                                                                         'Inochi',
                                                                                                                         'Convoy'],
                                                                                                                     '19.442735,-99.201111',
                                                                                                                     '1980/04/10',
                                                                                                                     '2016/09/10',
                                                                                                                     [
                                                                                                                         8.53439998626709,
                                                                                                                         4300.0],
                                                                                                                     datetime.date(
                                                                                                                         2016,
                                                                                                                         9,
                                                                                                                         10),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'Leader'),
                                                                                                                     None,
                                                                                                                     -6020000256.0),
                                                                                                                     (
                                                                                                                     'bumbl#ebéé  ',
                                                                                                                     17.0,
                                                                                                                     'Espionage',
                                                                                                                     7.0,
                                                                                                                     5000000.0,
                                                                                                                     2.0,
                                                                                                                     [
                                                                                                                         'Bumble',
                                                                                                                         'Goldback'],
                                                                                                                     '10.642707,-71.612534',
                                                                                                                     '1980/04/10',
                                                                                                                     '2015/08/10',
                                                                                                                     [
                                                                                                                         5.334000110626221,
                                                                                                                         2000.0],
                                                                                                                     datetime.date(
                                                                                                                         2015,
                                                                                                                         8,
                                                                                                                         10),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'Espionage'),
                                                                                                                     None,
                                                                                                                     1190000000.0),
                                                                                                                     (
                                                                                                                     'ironhide&',
                                                                                                                     26.0,
                                                                                                                     'Security',
                                                                                                                     7.0,
                                                                                                                     5000000.0,
                                                                                                                     4.0,
                                                                                                                     [
                                                                                                                         'Roadbuster'],
                                                                                                                     '37.789563,-122.400356',
                                                                                                                     '1980/04/10',
                                                                                                                     '2014/07/10',
                                                                                                                     [
                                                                                                                         7.924799919128418,
                                                                                                                         4000.0],
                                                                                                                     datetime.date(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'Security'),
                                                                                                                     None,
                                                                                                                     3640000000.0),
                                                                                                                     (
                                                                                                                     'Jazz',
                                                                                                                     13.0,
                                                                                                                     'First Lieutenant',
                                                                                                                     8.0,
                                                                                                                     5000000.0,
                                                                                                                     1.7999999523162842,
                                                                                                                     [
                                                                                                                         'Meister'],
                                                                                                                     '33.670666,-117.841553',
                                                                                                                     '1980/04/10',
                                                                                                                     '2013/06/10',
                                                                                                                     [
                                                                                                                         3.962399959564209,
                                                                                                                         1800.0],
                                                                                                                     datetime.date(
                                                                                                                         2013,
                                                                                                                         6,
                                                                                                                         24),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'First Lieutenant'),
                                                                                                                     None,
                                                                                                                     936000000.0),
                                                                                                                     (
                                                                                                                     'Megatron',
                                                                                                                     None,
                                                                                                                     'None',
                                                                                                                     10.0,
                                                                                                                     5000000.0,
                                                                                                                     5.699999809265137,
                                                                                                                     [
                                                                                                                         'Megatron'],
                                                                                                                     None,
                                                                                                                     '1980/04/10',
                                                                                                                     '2012/05/10',
                                                                                                                     [
                                                                                                                         None,
                                                                                                                         5700.0],
                                                                                                                     datetime.date(
                                                                                                                         2012,
                                                                                                                         5,
                                                                                                                         10),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'None'),
                                                                                                                     None,
                                                                                                                     None),
                                                                                                                     (
                                                                                                                     'Metroplex_)^$',
                                                                                                                     300.0,
                                                                                                                     'Battle Station',
                                                                                                                     8.0,
                                                                                                                     5000000.0,
                                                                                                                     None,
                                                                                                                     [
                                                                                                                         'Metroflex'],
                                                                                                                     None,
                                                                                                                     '1980/04/10',
                                                                                                                     '2011/04/10',
                                                                                                                     [
                                                                                                                         91.44000244140625,
                                                                                                                         None],
                                                                                                                     datetime.date(
                                                                                                                         2011,
                                                                                                                         4,
                                                                                                                         10),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'Battle Station'),
                                                                                                                     None,
                                                                                                                     None),
                                                                                                                     (
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_names():
        actual_df = source_df.cols.names()
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding(
            ['names', 'height(ft)', 'function', 'rank', 'age', 'weight(t)', 'japanese name', 'last position seen',
             'date arrival', 'last date seen', 'attributes', 'Date Type', 'Tiemstamp', 'Cybertronian',
             'function(binary)', 'NullType'])
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_nest():
        actual_df = source_df.cols.nest(['height(ft)', 'rank'], separator=' ', output_cols='new col')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True),
             ('height(ft)new col', StringType(), False), ('ranknew col', StringType(), False)], [("Optim'us", -28,
                                                                                                  'Leader', 10, 5000000,
                                                                                                  4.300000190734863,
                                                                                                  ['Inochi', 'Convoy'],
                                                                                                  '19.442735,-99.201111',
                                                                                                  '1980/04/10',
                                                                                                  '2016/09/10',
                                                                                                  [8.53439998626709,
                                                                                                   4300.0],
                                                                                                  datetime.date(2016, 9,
                                                                                                                10),
                                                                                                  datetime.datetime(
                                                                                                      2014, 6, 24, 0,
                                                                                                      0), True,
                                                                                                  bytearray(b'Leader'),
                                                                                                  None, '-28 10',
                                                                                                  '-28 10'), (
                                                                                                 'bumbl#ebéé  ', 17,
                                                                                                 'Espionage', 7,
                                                                                                 5000000, 2.0,
                                                                                                 ['Bumble', 'Goldback'],
                                                                                                 '10.642707,-71.612534',
                                                                                                 '1980/04/10',
                                                                                                 '2015/08/10',
                                                                                                 [5.334000110626221,
                                                                                                  2000.0],
                                                                                                 datetime.date(2015, 8,
                                                                                                               10),
                                                                                                 datetime.datetime(2014,
                                                                                                                   6,
                                                                                                                   24,
                                                                                                                   0,
                                                                                                                   0),
                                                                                                 True, bytearray(
                                                                                                     b'Espionage'),
                                                                                                 None, '17 7', '17 7'),
                                                                                                 ('ironhide&', 26,
                                                                                                  'Security', 7,
                                                                                                  5000000, 4.0,
                                                                                                  ['Roadbuster'],
                                                                                                  '37.789563,-122.400356',
                                                                                                  '1980/04/10',
                                                                                                  '2014/07/10',
                                                                                                  [7.924799919128418,
                                                                                                   4000.0],
                                                                                                  datetime.date(2014, 6,
                                                                                                                24),
                                                                                                  datetime.datetime(
                                                                                                      2014, 6, 24, 0,
                                                                                                      0), True,
                                                                                                  bytearray(
                                                                                                      b'Security'),
                                                                                                  None, '26 7', '26 7'),
                                                                                                 ('Jazz', 13,
                                                                                                  'First Lieutenant', 8,
                                                                                                  5000000,
                                                                                                  1.7999999523162842,
                                                                                                  ['Meister'],
                                                                                                  '33.670666,-117.841553',
                                                                                                  '1980/04/10',
                                                                                                  '2013/06/10',
                                                                                                  [3.962399959564209,
                                                                                                   1800.0],
                                                                                                  datetime.date(2013, 6,
                                                                                                                24),
                                                                                                  datetime.datetime(
                                                                                                      2014, 6, 24, 0,
                                                                                                      0), True,
                                                                                                  bytearray(
                                                                                                      b'First Lieutenant'),
                                                                                                  None, '13 8', '13 8'),
                                                                                                 ('Megatron', None,
                                                                                                  'None', 10, 5000000,
                                                                                                  5.699999809265137,
                                                                                                  ['Megatron'], None,
                                                                                                  '1980/04/10',
                                                                                                  '2012/05/10',
                                                                                                  [None, 5700.0],
                                                                                                  datetime.date(2012, 5,
                                                                                                                10),
                                                                                                  datetime.datetime(
                                                                                                      2014, 6, 24, 0,
                                                                                                      0), True,
                                                                                                  bytearray(b'None'),
                                                                                                  None, '10', '10'), (
                                                                                                 'Metroplex_)^$', 300,
                                                                                                 'Battle Station', 8,
                                                                                                 5000000, None,
                                                                                                 ['Metroflex'], None,
                                                                                                 '1980/04/10',
                                                                                                 '2011/04/10',
                                                                                                 [91.44000244140625,
                                                                                                  None],
                                                                                                 datetime.date(2011, 4,
                                                                                                               10),
                                                                                                 datetime.datetime(2014,
                                                                                                                   6,
                                                                                                                   24,
                                                                                                                   0,
                                                                                                                   0),
                                                                                                 True, bytearray(
                                                                                                     b'Battle Station'),
                                                                                                 None, '300 8',
                                                                                                 '300 8'), (
                                                                                                 None, None, None, None,
                                                                                                 None, None, None, None,
                                                                                                 None, None, None, None,
                                                                                                 None, None, None, None,
                                                                                                 '', '')])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_nest_array():
        actual_df = source_df.cols.nest(['height(ft)', 'rank', 'rank'], shape='array', output_cols='new col')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', StringType(), True), ('function', StringType(), True),
             ('rank', StringType(), True), ('age', StringType(), True), ('weight(t)', StringType(), True),
             ('japanese name', StringType(), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', StringType(), True), ('Date Type', StringType(), True), ('Tiemstamp', StringType(), True),
             ('Cybertronian', StringType(), True), ('function(binary)', StringType(), True),
             ('NullType', StringType(), True), ('height(ft)new col', ArrayType(StringType(), True), False),
             ('ranknew col', ArrayType(StringType(), True), False)], [("Optim'us", '-28', 'Leader', '10', '5000000',
                                                                       '4.3', '[Inochi, Convoy]',
                                                                       '19.442735,-99.201111', '1980/04/10',
                                                                       '2016/09/10', '[8.5344, 4300.0]', '2016-09-10',
                                                                       '2014-06-24 00:00:00', 'true', 'Leader', None,
                                                                       ['-28', '10', '10'], ['-28', '10', '10']), (
                                                                      'bumbl#ebéé  ', '17', 'Espionage', '7', '5000000',
                                                                      '2.0', '[Bumble, Goldback]',
                                                                      '10.642707,-71.612534', '1980/04/10',
                                                                      '2015/08/10', '[5.334, 2000.0]', '2015-08-10',
                                                                      '2014-06-24 00:00:00', 'true', 'Espionage', None,
                                                                      ['17', '7', '7'], ['17', '7', '7']), (
                                                                      'ironhide&', '26', 'Security', '7', '5000000',
                                                                      '4.0', '[Roadbuster]', '37.789563,-122.400356',
                                                                      '1980/04/10', '2014/07/10', '[7.9248, 4000.0]',
                                                                      '2014-06-24', '2014-06-24 00:00:00', 'true',
                                                                      'Security', None, ['26', '7', '7'],
                                                                      ['26', '7', '7']), (
                                                                      'Jazz', '13', 'First Lieutenant', '8', '5000000',
                                                                      '1.8', '[Meister]', '33.670666,-117.841553',
                                                                      '1980/04/10', '2013/06/10', '[3.9624, 1800.0]',
                                                                      '2013-06-24', '2014-06-24 00:00:00', 'true',
                                                                      'First Lieutenant', None, ['13', '8', '8'],
                                                                      ['13', '8', '8']), (
                                                                      'Megatron', None, 'None', '10', '5000000', '5.7',
                                                                      '[Megatron]', None, '1980/04/10', '2012/05/10',
                                                                      '[, 5700.0]', '2012-05-10', '2014-06-24 00:00:00',
                                                                      'true', 'None', None, [None, '10', '10'],
                                                                      [None, '10', '10']), (
                                                                      'Metroplex_)^$', '300', 'Battle Station', '8',
                                                                      '5000000', None, '[Metroflex]', None,
                                                                      '1980/04/10', '2011/04/10', '[91.44,]',
                                                                      '2011-04-10', '2014-06-24 00:00:00', 'true',
                                                                      'Battle Station', None, ['300', '8', '8'],
                                                                      ['300', '8', '8']), (
                                                                      None, None, None, None, None, None, None, None,
                                                                      None, None, None, None, None, None, None, None,
                                                                      [None, None, None], [None, None, None])])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_nest_vector():
        source_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True)], [("Optim'us", -28, 'Leader', 10, 5000000, 4.300000190734863,
                                                          ['Inochi', 'Convoy'], '19.442735,-99.201111', '1980/04/10',
                                                          '2016/09/10', [8.53439998626709, 4300.0],
                                                          datetime.date(2016, 9, 10),
                                                          datetime.datetime(2014, 6, 24, 0, 0), True,
                                                          bytearray(b'Leader')), (
                                                         'bumbl#ebéé  ', 17, 'Espionage', 7, 5000000, 2.0,
                                                         ['Bumble', 'Goldback'], '10.642707,-71.612534', '1980/04/10',
                                                         '2015/08/10', [5.334000110626221, 2000.0],
                                                         datetime.date(2015, 8, 10),
                                                         datetime.datetime(2014, 6, 24, 0, 0), True,
                                                         bytearray(b'Espionage')), (
                                                         'ironhide&', 26, 'Security', 7, 5000000, 4.0, ['Roadbuster'],
                                                         '37.789563,-122.400356', '1980/04/10', '2014/07/10',
                                                         [7.924799919128418, 4000.0], datetime.date(2014, 6, 24),
                                                         datetime.datetime(2014, 6, 24, 0, 0), True,
                                                         bytearray(b'Security')), (
                                                         'Jazz', 13, 'First Lieutenant', 8, 5000000, 1.7999999523162842,
                                                         ['Meister'], '33.670666,-117.841553', '1980/04/10',
                                                         '2013/06/10', [3.962399959564209, 1800.0],
                                                         datetime.date(2013, 6, 24),
                                                         datetime.datetime(2014, 6, 24, 0, 0), True,
                                                         bytearray(b'First Lieutenant'))])
        actual_df = source_df.cols.nest(['rank', 'rank'], shape='vector', output_cols='new col')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('new col', VectorUDT(), True)], [("Optim'us", -28, 'Leader', 10,
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'),
                                                                                          DenseVector([10.0])), (
                                                                                         'bumbl#ebéé  ', 17,
                                                                                         'Espionage', 7, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'),
                                                                                         DenseVector([7.0])), (
                                                                                         'ironhide&', 26, 'Security', 7,
                                                                                         5000000, 4.0, ['Roadbuster'],
                                                                                         '37.789563,-122.400356',
                                                                                         '1980/04/10', '2014/07/10',
                                                                                         [7.924799919128418, 4000.0],
                                                                                         datetime.date(2014, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Security'),
                                                                                         DenseVector([7.0])), (
                                                                                         'Jazz', 13, 'First Lieutenant',
                                                                                         8, 5000000, 1.7999999523162842,
                                                                                         ['Meister'],
                                                                                         '33.670666,-117.841553',
                                                                                         '1980/04/10', '2013/06/10',
                                                                                         [3.962399959564209, 1800.0],
                                                                                         datetime.date(2013, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'First Lieutenant'),
                                                                                         DenseVector([8.0]))])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_nest_vector_all_columns():
        source_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True)], [("Optim'us", -28, 'Leader', 10, 5000000, 4.300000190734863,
                                                          ['Inochi', 'Convoy'], '19.442735,-99.201111', '1980/04/10',
                                                          '2016/09/10', [8.53439998626709, 4300.0],
                                                          datetime.date(2016, 9, 10),
                                                          datetime.datetime(2014, 6, 24, 0, 0), True,
                                                          bytearray(b'Leader')), (
                                                         'bumbl#ebéé  ', 17, 'Espionage', 7, 5000000, 2.0,
                                                         ['Bumble', 'Goldback'], '10.642707,-71.612534', '1980/04/10',
                                                         '2015/08/10', [5.334000110626221, 2000.0],
                                                         datetime.date(2015, 8, 10),
                                                         datetime.datetime(2014, 6, 24, 0, 0), True,
                                                         bytearray(b'Espionage')), (
                                                         'ironhide&', 26, 'Security', 7, 5000000, 4.0, ['Roadbuster'],
                                                         '37.789563,-122.400356', '1980/04/10', '2014/07/10',
                                                         [7.924799919128418, 4000.0], datetime.date(2014, 6, 24),
                                                         datetime.datetime(2014, 6, 24, 0, 0), True,
                                                         bytearray(b'Security')), (
                                                         'Jazz', 13, 'First Lieutenant', 8, 5000000, 1.7999999523162842,
                                                         ['Meister'], '33.670666,-117.841553', '1980/04/10',
                                                         '2013/06/10', [3.962399959564209, 1800.0],
                                                         datetime.date(2013, 6, 24),
                                                         datetime.datetime(2014, 6, 24, 0, 0), True,
                                                         bytearray(b'First Lieutenant'))])
        actual_df = source_df.cols.nest(['rank', 'rank'], shape='vector', output_cols='new col')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('new col', VectorUDT(), True)], [("Optim'us", -28, 'Leader', 10,
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'),
                                                                                          DenseVector([10.0])), (
                                                                                         'bumbl#ebéé  ', 17,
                                                                                         'Espionage', 7, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'),
                                                                                         DenseVector([7.0])), (
                                                                                         'ironhide&', 26, 'Security', 7,
                                                                                         5000000, 4.0, ['Roadbuster'],
                                                                                         '37.789563,-122.400356',
                                                                                         '1980/04/10', '2014/07/10',
                                                                                         [7.924799919128418, 4000.0],
                                                                                         datetime.date(2014, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Security'),
                                                                                         DenseVector([7.0])), (
                                                                                         'Jazz', 13, 'First Lieutenant',
                                                                                         8, 5000000, 1.7999999523162842,
                                                                                         ['Meister'],
                                                                                         '33.670666,-117.841553',
                                                                                         '1980/04/10', '2013/06/10',
                                                                                         [3.962399959564209, 1800.0],
                                                                                         datetime.date(2013, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'First Lieutenant'),
                                                                                         DenseVector([8.0]))])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_percentile():
        actual_df = source_df.cols.percentile('height(ft)', [0.05, 0.25], 1)
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding({'0.05': -28.0, '0.25': -28.0})
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_percentile_all_columns():
        actual_df = source_df.cols.percentile('*', [0.05, 0.25], 1)
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding(
            {'height(ft)': {'0.05': -28.0, '0.25': -28.0}, 'rank': {'0.05': 7.0, '0.25': 7.0},
             'age': {'0.05': 5000000.0, '0.25': 5000000.0},
             'weight(t)': {'0.05': 1.7999999523162842, '0.25': 1.7999999523162842}})
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_qcut():
        actual_df = source_df.cols.qcut('rank', 4)
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True),
             ('rank_qcut', DoubleType(), True)], [("Optim'us", -28, 'Leader', 10, 5000000, 4.300000190734863,
                                                   ['Inochi', 'Convoy'], '19.442735,-99.201111', '1980/04/10',
                                                   '2016/09/10', [8.53439998626709, 4300.0], datetime.date(2016, 9, 10),
                                                   datetime.datetime(2014, 6, 24, 0, 0), True, bytearray(b'Leader'),
                                                   None, 3.0), ('bumbl#ebéé  ', 17, 'Espionage', 7, 5000000, 2.0,
                                                                ['Bumble', 'Goldback'], '10.642707,-71.612534',
                                                                '1980/04/10', '2015/08/10', [5.334000110626221, 2000.0],
                                                                datetime.date(2015, 8, 10),
                                                                datetime.datetime(2014, 6, 24, 0, 0), True,
                                                                bytearray(b'Espionage'), None, 1.0), (
                                                  'ironhide&', 26, 'Security', 7, 5000000, 4.0, ['Roadbuster'],
                                                  '37.789563,-122.400356', '1980/04/10', '2014/07/10',
                                                  [7.924799919128418, 4000.0], datetime.date(2014, 6, 24),
                                                  datetime.datetime(2014, 6, 24, 0, 0), True, bytearray(b'Security'),
                                                  None, 1.0), (
                                                  'Jazz', 13, 'First Lieutenant', 8, 5000000, 1.7999999523162842,
                                                  ['Meister'], '33.670666,-117.841553', '1980/04/10', '2013/06/10',
                                                  [3.962399959564209, 1800.0], datetime.date(2013, 6, 24),
                                                  datetime.datetime(2014, 6, 24, 0, 0), True,
                                                  bytearray(b'First Lieutenant'), None, 2.0), (
                                                  'Megatron', None, 'None', 10, 5000000, 5.699999809265137,
                                                  ['Megatron'], None, '1980/04/10', '2012/05/10', [None, 5700.0],
                                                  datetime.date(2012, 5, 10), datetime.datetime(2014, 6, 24, 0, 0),
                                                  True, bytearray(b'None'), None, 3.0), (
                                                  'Metroplex_)^$', 300, 'Battle Station', 8, 5000000, None,
                                                  ['Metroflex'], None, '1980/04/10', '2011/04/10',
                                                  [91.44000244140625, None], datetime.date(2011, 4, 10),
                                                  datetime.datetime(2014, 6, 24, 0, 0), True,
                                                  bytearray(b'Battle Station'), None, 2.0)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_qcut_all_columns():
        actual_df = source_df.cols.qcut('*', 4)
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True),
             ('height(ft)_qcut', DoubleType(), True), ('rank_qcut', DoubleType(), True),
             ('age_qcut', DoubleType(), True), ('weight(t)_qcut', DoubleType(), True)], [("Optim'us", -28, 'Leader', 10,
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None,
                                                                                          0.0, 2.0, 1.0, 3.0), (
                                                                                         'bumbl#ebéé  ', 17,
                                                                                         'Espionage', 7, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None,
                                                                                         2.0, 1.0, 1.0, 2.0), (
                                                                                         'ironhide&', 26, 'Security', 7,
                                                                                         5000000, 4.0, ['Roadbuster'],
                                                                                         '37.789563,-122.400356',
                                                                                         '1980/04/10', '2014/07/10',
                                                                                         [7.924799919128418, 4000.0],
                                                                                         datetime.date(2014, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Security'), None,
                                                                                         3.0, 1.0, 1.0, 3.0), (
                                                                                         'Jazz', 13, 'First Lieutenant',
                                                                                         8, 5000000, 1.7999999523162842,
                                                                                         ['Meister'],
                                                                                         '33.670666,-117.841553',
                                                                                         '1980/04/10', '2013/06/10',
                                                                                         [3.962399959564209, 1800.0],
                                                                                         datetime.date(2013, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'First Lieutenant'),
                                                                                         None, 1.0, 2.0, 1.0, 1.0)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_range():
        actual_df = source_df.cols.range('height(ft)')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding({'height(ft)': {'min': -28, 'max': 300}})
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_range_all_columns():
        actual_df = source_df.cols.range('*')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding(
            {'names': {'min': 'Jazz', 'max': 'ironhide&'}, 'height(ft)': {'min': -28, 'max': 300},
             'function': {'min': 'Battle Station', 'max': 'Security'}, 'rank': {'min': 7, 'max': 10},
             'age': {'min': 5000000, 'max': 5000000}, 'weight(t)': {'min': 1.8, 'max': 5.7},
             'japanese name': {'min': ['Bumble', 'Goldback'], 'max': ['Roadbuster']},
             'last position seen': {'min': '10.642707,-71.612534', 'max': '37.789563,-122.400356'},
             'date arrival': {'min': '1980/04/10', 'max': '1980/04/10'},
             'last date seen': {'min': '2011/04/10', 'max': '2016/09/10'},
             'attributes': {'min': [None, 5700.0], 'max': [91.44000244140625, None]},
             'Date Type': {'min': datetime.date(2011, 4, 10), 'max': datetime.date(2016, 9, 10)},
             'Tiemstamp': {'min': datetime.datetime(2014, 6, 24, 0, 0), 'max': datetime.datetime(2014, 6, 24, 0, 0)},
             'Cybertronian': {'min': 1, 'max': 1},
             'function(binary)': {'min': bytearray(b'Battle Station'), 'max': bytearray(b'Security')},
             'NullType': {'min': None, 'max': None}})
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_remove():
        actual_df = source_df.cols.remove('function', 'i')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("Optim'us", -28, 'Leader', 10,
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         'bumbl#ebéé  ', 17, 'Esponage',
                                                                                         7, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         ('ironhide&', 26, 'Securty', 7,
                                                                                          5000000, 4.0, ['Roadbuster'],
                                                                                          '37.789563,-122.400356',
                                                                                          '1980/04/10', '2014/07/10',
                                                                                          [7.924799919128418, 4000.0],
                                                                                          datetime.date(2014, 6, 24),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Security'), None),
                                                                                         ('Jazz', 13, 'Frst Leutenant',
                                                                                          8, 5000000,
                                                                                          1.7999999523162842,
                                                                                          ['Meister'],
                                                                                          '33.670666,-117.841553',
                                                                                          '1980/04/10', '2013/06/10',
                                                                                          [3.962399959564209, 1800.0],
                                                                                          datetime.date(2013, 6, 24),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(
                                                                                              b'First Lieutenant'),
                                                                                          None), (
                                                                                         'Megatron', None, 'None', 10,
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$', 300,
                                                                                         'Battle Staton', 8, 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '1980/04/10', '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_remove_accents():
        actual_df = source_df.cols.remove_accents('function')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("Optim'us", -28, 'Leader', 10,
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         'bumbl#ebéé  ', 17,
                                                                                         'Espionage', 7, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         (
                                                                                         'ironhide&', 26, 'Security', 7,
                                                                                         5000000, 4.0, ['Roadbuster'],
                                                                                         '37.789563,-122.400356',
                                                                                         '1980/04/10', '2014/07/10',
                                                                                         [7.924799919128418, 4000.0],
                                                                                         datetime.date(2014, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Security'), None),
                                                                                         (
                                                                                         'Jazz', 13, 'First Lieutenant',
                                                                                         8, 5000000, 1.7999999523162842,
                                                                                         ['Meister'],
                                                                                         '33.670666,-117.841553',
                                                                                         '1980/04/10', '2013/06/10',
                                                                                         [3.962399959564209, 1800.0],
                                                                                         datetime.date(2013, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'First Lieutenant'),
                                                                                         None), (
                                                                                         'Megatron', None, 'None', 10,
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$', 300,
                                                                                         'Battle Station', 8, 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '1980/04/10', '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, 'None', None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_remove_accents_all_columns():
        actual_df = source_df.cols.remove_accents('function')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("Optim'us", -28, 'Leader', 10,
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         'bumbl#ebéé  ', 17,
                                                                                         'Espionage', 7, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         (
                                                                                         'ironhide&', 26, 'Security', 7,
                                                                                         5000000, 4.0, ['Roadbuster'],
                                                                                         '37.789563,-122.400356',
                                                                                         '1980/04/10', '2014/07/10',
                                                                                         [7.924799919128418, 4000.0],
                                                                                         datetime.date(2014, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Security'), None),
                                                                                         (
                                                                                         'Jazz', 13, 'First Lieutenant',
                                                                                         8, 5000000, 1.7999999523162842,
                                                                                         ['Meister'],
                                                                                         '33.670666,-117.841553',
                                                                                         '1980/04/10', '2013/06/10',
                                                                                         [3.962399959564209, 1800.0],
                                                                                         datetime.date(2013, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'First Lieutenant'),
                                                                                         None), (
                                                                                         'Megatron', None, 'None', 10,
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$', 300,
                                                                                         'Battle Station', 8, 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '1980/04/10', '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, 'None', None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_remove_list():
        actual_df = source_df.cols.remove('function', ['a', 'i', 'Es'])
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("Optim'us", -28, 'Leder', 10,
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         'bumbl#ebéé  ', 17, 'ponge', 7,
                                                                                         5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         ('ironhide&', 26, 'Securty', 7,
                                                                                          5000000, 4.0, ['Roadbuster'],
                                                                                          '37.789563,-122.400356',
                                                                                          '1980/04/10', '2014/07/10',
                                                                                          [7.924799919128418, 4000.0],
                                                                                          datetime.date(2014, 6, 24),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Security'), None),
                                                                                         (
                                                                                         'Jazz', 13, 'Frst Leutennt', 8,
                                                                                         5000000, 1.7999999523162842,
                                                                                         ['Meister'],
                                                                                         '33.670666,-117.841553',
                                                                                         '1980/04/10', '2013/06/10',
                                                                                         [3.962399959564209, 1800.0],
                                                                                         datetime.date(2013, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'First Lieutenant'),
                                                                                         None), (
                                                                                         'Megatron', None, 'None', 10,
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$', 300,
                                                                                         'Bttle Stton', 8, 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '1980/04/10', '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_remove_list_output():
        actual_df = source_df.cols.remove('function', ['a', 'i', 'Es'], output_cols='function_new')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True),
             ('function_new', StringType(), True)], [("Optim'us", -28, 'Leader', 10, 5000000, 4.300000190734863,
                                                      ['Inochi', 'Convoy'], '19.442735,-99.201111', '1980/04/10',
                                                      '2016/09/10', [8.53439998626709, 4300.0],
                                                      datetime.date(2016, 9, 10), datetime.datetime(2014, 6, 24, 0, 0),
                                                      True, bytearray(b'Leader'), None, 'Leder'), (
                                                     'bumbl#ebéé  ', 17, 'Espionage', 7, 5000000, 2.0,
                                                     ['Bumble', 'Goldback'], '10.642707,-71.612534', '1980/04/10',
                                                     '2015/08/10', [5.334000110626221, 2000.0],
                                                     datetime.date(2015, 8, 10), datetime.datetime(2014, 6, 24, 0, 0),
                                                     True, bytearray(b'Espionage'), None, 'ponge'), (
                                                     'ironhide&', 26, 'Security', 7, 5000000, 4.0, ['Roadbuster'],
                                                     '37.789563,-122.400356', '1980/04/10', '2014/07/10',
                                                     [7.924799919128418, 4000.0], datetime.date(2014, 6, 24),
                                                     datetime.datetime(2014, 6, 24, 0, 0), True, bytearray(b'Security'),
                                                     None, 'Securty'), (
                                                     'Jazz', 13, 'First Lieutenant', 8, 5000000, 1.7999999523162842,
                                                     ['Meister'], '33.670666,-117.841553', '1980/04/10', '2013/06/10',
                                                     [3.962399959564209, 1800.0], datetime.date(2013, 6, 24),
                                                     datetime.datetime(2014, 6, 24, 0, 0), True,
                                                     bytearray(b'First Lieutenant'), None, 'Frst Leutennt'), (
                                                     'Megatron', None, 'None', 10, 5000000, 5.699999809265137,
                                                     ['Megatron'], None, '1980/04/10', '2012/05/10', [None, 5700.0],
                                                     datetime.date(2012, 5, 10), datetime.datetime(2014, 6, 24, 0, 0),
                                                     True, bytearray(b'None'), None, 'None'), (
                                                     'Metroplex_)^$', 300, 'Battle Station', 8, 5000000, None,
                                                     ['Metroflex'], None, '1980/04/10', '2011/04/10',
                                                     [91.44000244140625, None], datetime.date(2011, 4, 10),
                                                     datetime.datetime(2014, 6, 24, 0, 0), True,
                                                     bytearray(b'Battle Station'), None, 'Bttle Stton'), (
                                                     None, None, None, None, None, None, None, None, None, None, None,
                                                     None, None, None, None, None, None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_remove_special_chars():
        actual_df = source_df.cols.remove_special_chars('function')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("Optim'us", -28, 'Leader', 10,
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         'bumbl#ebéé  ', 17,
                                                                                         'Espionage', 7, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         (
                                                                                         'ironhide&', 26, 'Security', 7,
                                                                                         5000000, 4.0, ['Roadbuster'],
                                                                                         '37.789563,-122.400356',
                                                                                         '1980/04/10', '2014/07/10',
                                                                                         [7.924799919128418, 4000.0],
                                                                                         datetime.date(2014, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Security'), None),
                                                                                         (
                                                                                         'Jazz', 13, 'First Lieutenant',
                                                                                         8, 5000000, 1.7999999523162842,
                                                                                         ['Meister'],
                                                                                         '33.670666,-117.841553',
                                                                                         '1980/04/10', '2013/06/10',
                                                                                         [3.962399959564209, 1800.0],
                                                                                         datetime.date(2013, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'First Lieutenant'),
                                                                                         None), (
                                                                                         'Megatron', None, 'None', 10,
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$', 300,
                                                                                         'Battle Station', 8, 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '1980/04/10', '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_remove_special_chars_all_columns():
        actual_df = source_df.cols.remove_special_chars('*')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [('Optimus', -28, 'Leader', 10,
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '1944273599201111',
                                                                                          '19800410', '20160910',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         'bumblebéé  ', 17, 'Espionage',
                                                                                         7, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '1064270771612534', '19800410',
                                                                                         '20150810',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         ('ironhide', 26, 'Security', 7,
                                                                                          5000000, 4.0, ['Roadbuster'],
                                                                                          '37789563122400356',
                                                                                          '19800410', '20140710',
                                                                                          [7.924799919128418, 4000.0],
                                                                                          datetime.date(2014, 6, 24),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Security'), None),
                                                                                         (
                                                                                         'Jazz', 13, 'First Lieutenant',
                                                                                         8, 5000000, 1.7999999523162842,
                                                                                         ['Meister'],
                                                                                         '33670666117841553',
                                                                                         '19800410', '20130610',
                                                                                         [3.962399959564209, 1800.0],
                                                                                         datetime.date(2013, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'First Lieutenant'),
                                                                                         None), (
                                                                                         'Megatron', None, 'None', 10,
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None, '19800410',
                                                                                         '20120510', [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'Metroplex', 300,
                                                                                         'Battle Station', 8, 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '19800410', '20110410',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_remove_white_spaces():
        actual_df = source_df.cols.remove_white_spaces('function')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("Optim'us", -28, 'Leader', 10,
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         'bumbl#ebéé  ', 17,
                                                                                         'Espionage', 7, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         (
                                                                                         'ironhide&', 26, 'Security', 7,
                                                                                         5000000, 4.0, ['Roadbuster'],
                                                                                         '37.789563,-122.400356',
                                                                                         '1980/04/10', '2014/07/10',
                                                                                         [7.924799919128418, 4000.0],
                                                                                         datetime.date(2014, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Security'), None),
                                                                                         ('Jazz', 13, 'FirstLieutenant',
                                                                                          8, 5000000,
                                                                                          1.7999999523162842,
                                                                                          ['Meister'],
                                                                                          '33.670666,-117.841553',
                                                                                          '1980/04/10', '2013/06/10',
                                                                                          [3.962399959564209, 1800.0],
                                                                                          datetime.date(2013, 6, 24),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(
                                                                                              b'First Lieutenant'),
                                                                                          None), (
                                                                                         'Megatron', None, 'None', 10,
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$', 300,
                                                                                         'BattleStation', 8, 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '1980/04/10', '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_remove_white_spaces_all_columns():
        actual_df = source_df.cols.remove_white_spaces('*')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', StringType(), True), ('function', StringType(), True),
             ('rank', StringType(), True), ('age', StringType(), True), ('weight(t)', StringType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', StringType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', StringType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("Optim'us", '-28', 'Leader',
                                                                                          '10', '5000000', '4.3',
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          '2016-09-10',
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0),
                                                                                          'true', bytearray(b'Leader'),
                                                                                          None), ('bumbl#ebéé', '17',
                                                                                                  'Espionage', '7',
                                                                                                  '5000000', '2.0',
                                                                                                  ['Bumble',
                                                                                                   'Goldback'],
                                                                                                  '10.642707,-71.612534',
                                                                                                  '1980/04/10',
                                                                                                  '2015/08/10',
                                                                                                  [5.334000110626221,
                                                                                                   2000.0],
                                                                                                  '2015-08-10',
                                                                                                  datetime.datetime(
                                                                                                      2014, 6, 24, 0,
                                                                                                      0), 'true',
                                                                                                  bytearray(
                                                                                                      b'Espionage'),
                                                                                                  None), (
                                                                                         'ironhide&', '26', 'Security',
                                                                                         '7', '5000000', '4.0',
                                                                                         ['Roadbuster'],
                                                                                         '37.789563,-122.400356',
                                                                                         '1980/04/10', '2014/07/10',
                                                                                         [7.924799919128418, 4000.0],
                                                                                         '2014-06-24',
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0),
                                                                                         'true', bytearray(b'Security'),
                                                                                         None), ('Jazz', '13',
                                                                                                 'FirstLieutenant', '8',
                                                                                                 '5000000', '1.8',
                                                                                                 ['Meister'],
                                                                                                 '33.670666,-117.841553',
                                                                                                 '1980/04/10',
                                                                                                 '2013/06/10',
                                                                                                 [3.962399959564209,
                                                                                                  1800.0], '2013-06-24',
                                                                                                 datetime.datetime(2014,
                                                                                                                   6,
                                                                                                                   24,
                                                                                                                   0,
                                                                                                                   0),
                                                                                                 'true', bytearray(
                b'First Lieutenant'), None), ('Megatron', None, 'None', '10', '5000000', '5.7', ['Megatron'], None,
                                              '1980/04/10', '2012/05/10', [None, 5700.0], '2012-05-10',
                                              datetime.datetime(2014, 6, 24, 0, 0), 'true', bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$', '300',
                                                                                         'BattleStation', '8',
                                                                                         '5000000', None, ['Metroflex'],
                                                                                         None, '1980/04/10',
                                                                                         '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         '2011-04-10',
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0),
                                                                                         'true',
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_rename():
        actual_df = source_df.cols.rename('rank', 'rank(old)')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank(old)', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("Optim'us", -28, 'Leader', 10,
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         'bumbl#ebéé  ', 17,
                                                                                         'Espionage', 7, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         (
                                                                                         'ironhide&', 26, 'Security', 7,
                                                                                         5000000, 4.0, ['Roadbuster'],
                                                                                         '37.789563,-122.400356',
                                                                                         '1980/04/10', '2014/07/10',
                                                                                         [7.924799919128418, 4000.0],
                                                                                         datetime.date(2014, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Security'), None),
                                                                                         (
                                                                                         'Jazz', 13, 'First Lieutenant',
                                                                                         8, 5000000, 1.7999999523162842,
                                                                                         ['Meister'],
                                                                                         '33.670666,-117.841553',
                                                                                         '1980/04/10', '2013/06/10',
                                                                                         [3.962399959564209, 1800.0],
                                                                                         datetime.date(2013, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'First Lieutenant'),
                                                                                         None), (
                                                                                         'Megatron', None, 'None', 10,
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$', 300,
                                                                                         'Battle Station', 8, 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '1980/04/10', '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_rename_function():
        actual_df = source_df.cols.rename(str.upper)
        expected_df = op.create.df(
            [('NAMES', StringType(), True), ('HEIGHT(FT)', ShortType(), True), ('FUNCTION', StringType(), True),
             ('RANK', ByteType(), True), ('AGE', IntegerType(), True), ('WEIGHT(T)', FloatType(), True),
             ('JAPANESE NAME', ArrayType(StringType(), True), True), ('LAST POSITION SEEN', StringType(), True),
             ('DATE ARRIVAL', StringType(), True), ('LAST DATE SEEN', StringType(), True),
             ('ATTRIBUTES', ArrayType(FloatType(), True), True), ('DATE TYPE', DateType(), True),
             ('TIEMSTAMP', TimestampType(), True), ('CYBERTRONIAN', BooleanType(), True),
             ('FUNCTION(BINARY)', BinaryType(), True), ('NULLTYPE', NullType(), True)], [("Optim'us", -28, 'Leader', 10,
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         'bumbl#ebéé  ', 17,
                                                                                         'Espionage', 7, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         (
                                                                                         'ironhide&', 26, 'Security', 7,
                                                                                         5000000, 4.0, ['Roadbuster'],
                                                                                         '37.789563,-122.400356',
                                                                                         '1980/04/10', '2014/07/10',
                                                                                         [7.924799919128418, 4000.0],
                                                                                         datetime.date(2014, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Security'), None),
                                                                                         (
                                                                                         'Jazz', 13, 'First Lieutenant',
                                                                                         8, 5000000, 1.7999999523162842,
                                                                                         ['Meister'],
                                                                                         '33.670666,-117.841553',
                                                                                         '1980/04/10', '2013/06/10',
                                                                                         [3.962399959564209, 1800.0],
                                                                                         datetime.date(2013, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'First Lieutenant'),
                                                                                         None), (
                                                                                         'Megatron', None, 'None', 10,
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$', 300,
                                                                                         'Battle Station', 8, 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '1980/04/10', '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_rename_list():
        actual_df = source_df.cols.rename(['height(ft)', 'height(ft)(tons)', 'rank', 'rank(old)'])
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("Optim'us", -28, 'Leader', 10,
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         'bumbl#ebéé  ', 17,
                                                                                         'Espionage', 7, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         (
                                                                                         'ironhide&', 26, 'Security', 7,
                                                                                         5000000, 4.0, ['Roadbuster'],
                                                                                         '37.789563,-122.400356',
                                                                                         '1980/04/10', '2014/07/10',
                                                                                         [7.924799919128418, 4000.0],
                                                                                         datetime.date(2014, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Security'), None),
                                                                                         (
                                                                                         'Jazz', 13, 'First Lieutenant',
                                                                                         8, 5000000, 1.7999999523162842,
                                                                                         ['Meister'],
                                                                                         '33.670666,-117.841553',
                                                                                         '1980/04/10', '2013/06/10',
                                                                                         [3.962399959564209, 1800.0],
                                                                                         datetime.date(2013, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'First Lieutenant'),
                                                                                         None), (
                                                                                         'Megatron', None, 'None', 10,
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$', 300,
                                                                                         'Battle Station', 8, 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '1980/04/10', '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_replace():
        actual_df = source_df.cols.replace('function', ['Security', 'Leader'], 'Match')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("Optim'us", -28, 'Match', 10,
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         'bumbl#ebéé  ', 17,
                                                                                         'Espionage', 7, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         ('ironhide&', 26, 'Match', 7,
                                                                                          5000000, 4.0, ['Roadbuster'],
                                                                                          '37.789563,-122.400356',
                                                                                          '1980/04/10', '2014/07/10',
                                                                                          [7.924799919128418, 4000.0],
                                                                                          datetime.date(2014, 6, 24),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Security'), None),
                                                                                         (
                                                                                         'Jazz', 13, 'First Lieutenant',
                                                                                         8, 5000000, 1.7999999523162842,
                                                                                         ['Meister'],
                                                                                         '33.670666,-117.841553',
                                                                                         '1980/04/10', '2013/06/10',
                                                                                         [3.962399959564209, 1800.0],
                                                                                         datetime.date(2013, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'First Lieutenant'),
                                                                                         None), (
                                                                                         'Megatron', None, 'None', 10,
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$', 300,
                                                                                         'Battle Station', 8, 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '1980/04/10', '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_reverse():
        actual_df = source_df.cols.reverse('function')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("Optim'us", -28, 'redaeL', 10,
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         'bumbl#ebéé  ', 17,
                                                                                         'eganoipsE', 7, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         (
                                                                                         'ironhide&', 26, 'ytiruceS', 7,
                                                                                         5000000, 4.0, ['Roadbuster'],
                                                                                         '37.789563,-122.400356',
                                                                                         '1980/04/10', '2014/07/10',
                                                                                         [7.924799919128418, 4000.0],
                                                                                         datetime.date(2014, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Security'), None),
                                                                                         (
                                                                                         'Jazz', 13, 'tnanetueiL tsriF',
                                                                                         8, 5000000, 1.7999999523162842,
                                                                                         ['Meister'],
                                                                                         '33.670666,-117.841553',
                                                                                         '1980/04/10', '2013/06/10',
                                                                                         [3.962399959564209, 1800.0],
                                                                                         datetime.date(2013, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'First Lieutenant'),
                                                                                         None), (
                                                                                         'Megatron', None, 'enoN', 10,
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$', 300,
                                                                                         'noitatS elttaB', 8, 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '1980/04/10', '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_reverse_all_columns():
        actual_df = source_df.cols.reverse('*')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("su'mitpO", -28, 'redaeL', 10,
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '111102.99-,537244.91',
                                                                                          '01/40/0891', '01/90/6102',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         '  éébe#lbmub', 17,
                                                                                         'eganoipsE', 7, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '435216.17-,707246.01',
                                                                                         '01/40/0891', '01/80/5102',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         (
                                                                                         '&edihnori', 26, 'ytiruceS', 7,
                                                                                         5000000, 4.0, ['Roadbuster'],
                                                                                         '653004.221-,365987.73',
                                                                                         '01/40/0891', '01/70/4102',
                                                                                         [7.924799919128418, 4000.0],
                                                                                         datetime.date(2014, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Security'), None),
                                                                                         (
                                                                                         'zzaJ', 13, 'tnanetueiL tsriF',
                                                                                         8, 5000000, 1.7999999523162842,
                                                                                         ['Meister'],
                                                                                         '355148.711-,666076.33',
                                                                                         '01/40/0891', '01/60/3102',
                                                                                         [3.962399959564209, 1800.0],
                                                                                         datetime.date(2013, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'First Lieutenant'),
                                                                                         None), (
                                                                                         'nortageM', None, 'enoN', 10,
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '01/40/0891', '01/50/2102',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         '$^)_xelporteM', 300,
                                                                                         'noitatS elttaB', 8, 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '01/40/0891', '01/40/1102',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_schema_dtype():
        actual_df = source_df.cols.schema_dtype('rank')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding(ByteType)
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_select():
        actual_df = source_df.cols.select(0, 'height(ft)')
        expected_df = op.create.df([('names', StringType(), True)],
                                   [("Optim'us",), ('bumbl#ebéé  ',), ('ironhide&',), ('Jazz',), ('Megatron',),
                                    ('Metroplex_)^$',), (None,)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_select_by_dtypes_array():
        actual_df = source_df.cols.select_by_dtypes('array')
        expected_df = op.create.df([('japanese name', ArrayType(StringType(), True), True),
                                    ('attributes', ArrayType(FloatType(), True), True)],
                                   [(['Inochi', 'Convoy'], [8.53439998626709, 4300.0]),
                                    (['Bumble', 'Goldback'], [5.334000110626221, 2000.0]),
                                    (['Roadbuster'], [7.924799919128418, 4000.0]),
                                    (['Meister'], [3.962399959564209, 1800.0]), (['Megatron'], [None, 5700.0]),
                                    (['Metroflex'], [91.44000244140625, None]), (None, None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_select_by_dtypes_float():
        actual_df = source_df.cols.select_by_dtypes('float')
        expected_df = op.create.df([('weight(t)', FloatType(), True)],
                                   [(4.300000190734863,), (2.0,), (4.0,), (1.7999999523162842,), (5.699999809265137,),
                                    (None,), (None,)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_select_by_dtypes_int():
        actual_df = source_df.cols.select_by_dtypes('int')
        expected_df = op.create.df([('age', IntegerType(), True)],
                                   [(5000000,), (5000000,), (5000000,), (5000000,), (5000000,), (5000000,), (None,)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_select_by_dtypes_str():
        actual_df = source_df.cols.select_by_dtypes('str')
        expected_df = op.create.df([('names', StringType(), True), ('function', StringType(), True),
                                    ('last position seen', StringType(), True), ('date arrival', StringType(), True),
                                    ('last date seen', StringType(), True)],
                                   [("Optim'us", 'Leader', '19.442735,-99.201111', '1980/04/10', '2016/09/10'),
                                    ('bumbl#ebéé  ', 'Espionage', '10.642707,-71.612534', '1980/04/10', '2015/08/10'),
                                    ('ironhide&', 'Security', '37.789563,-122.400356', '1980/04/10', '2014/07/10'),
                                    ('Jazz', 'First Lieutenant', '33.670666,-117.841553', '1980/04/10', '2013/06/10'),
                                    ('Megatron', 'None', None, '1980/04/10', '2012/05/10'),
                                    ('Metroplex_)^$', 'Battle Station', None, '1980/04/10', '2011/04/10'),
                                    (None, None, None, None, None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_select_regex():
        actual_df = source_df.cols.select('n.*', regex=True)
        expected_df = op.create.df([('names', StringType(), True)],
                                   [("Optim'us",), ('bumbl#ebéé  ',), ('ironhide&',), ('Jazz',), ('Megatron',),
                                    ('Metroplex_)^$',), (None,)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_skewness():
        actual_df = source_df.cols.skewness('height(ft)')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding(1.4049)
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_skewness_all_columns():
        actual_df = source_df.cols.skewness('*')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding({'height(ft)': 1.4049, 'rank': 0.3818, 'age': nan, 'weight(t)': 0.06521})
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_sort():
        actual_df = source_df.cols.sort()
        expected_df = op.create.df(
            [('Cybertronian', BooleanType(), True), ('Date Type', DateType(), True), ('NullType', NullType(), True),
             ('Tiemstamp', TimestampType(), True), ('age', IntegerType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('date arrival', StringType(), True),
             ('function', StringType(), True), ('function(binary)', BinaryType(), True),
             ('height(ft)', ShortType(), True), ('japanese name', ArrayType(StringType(), True), True),
             ('last date seen', StringType(), True), ('last position seen', StringType(), True),
             ('names', StringType(), True), ('rank', ByteType(), True), ('weight(t)', FloatType(), True)], [(True,
                                                                                                             datetime.date(
                                                                                                                 2016,
                                                                                                                 9, 10),
                                                                                                             None,
                                                                                                             datetime.datetime(
                                                                                                                 2014,
                                                                                                                 6, 24,
                                                                                                                 0, 0),
                                                                                                             5000000, [
                                                                                                                 8.53439998626709,
                                                                                                                 4300.0],
                                                                                                             '1980/04/10',
                                                                                                             'Leader',
                                                                                                             bytearray(
                                                                                                                 b'Leader'),
                                                                                                             -28,
                                                                                                             ['Inochi',
                                                                                                              'Convoy'],
                                                                                                             '2016/09/10',
                                                                                                             '19.442735,-99.201111',
                                                                                                             "Optim'us",
                                                                                                             10,
                                                                                                             4.300000190734863),
                                                                                                            (True,
                                                                                                             datetime.date(
                                                                                                                 2015,
                                                                                                                 8, 10),
                                                                                                             None,
                                                                                                             datetime.datetime(
                                                                                                                 2014,
                                                                                                                 6, 24,
                                                                                                                 0, 0),
                                                                                                             5000000, [
                                                                                                                 5.334000110626221,
                                                                                                                 2000.0],
                                                                                                             '1980/04/10',
                                                                                                             'Espionage',
                                                                                                             bytearray(
                                                                                                                 b'Espionage'),
                                                                                                             17,
                                                                                                             ['Bumble',
                                                                                                              'Goldback'],
                                                                                                             '2015/08/10',
                                                                                                             '10.642707,-71.612534',
                                                                                                             'bumbl#ebéé  ',
                                                                                                             7, 2.0), (
                                                                                                            True,
                                                                                                            datetime.date(
                                                                                                                2014, 6,
                                                                                                                24),
                                                                                                            None,
                                                                                                            datetime.datetime(
                                                                                                                2014, 6,
                                                                                                                24, 0,
                                                                                                                0),
                                                                                                            5000000, [
                                                                                                                7.924799919128418,
                                                                                                                4000.0],
                                                                                                            '1980/04/10',
                                                                                                            'Security',
                                                                                                            bytearray(
                                                                                                                b'Security'),
                                                                                                            26, [
                                                                                                                'Roadbuster'],
                                                                                                            '2014/07/10',
                                                                                                            '37.789563,-122.400356',
                                                                                                            'ironhide&',
                                                                                                            7, 4.0), (
                                                                                                            True,
                                                                                                            datetime.date(
                                                                                                                2013, 6,
                                                                                                                24),
                                                                                                            None,
                                                                                                            datetime.datetime(
                                                                                                                2014, 6,
                                                                                                                24, 0,
                                                                                                                0),
                                                                                                            5000000, [
                                                                                                                3.962399959564209,
                                                                                                                1800.0],
                                                                                                            '1980/04/10',
                                                                                                            'First Lieutenant',
                                                                                                            bytearray(
                                                                                                                b'First Lieutenant'),
                                                                                                            13,
                                                                                                            ['Meister'],
                                                                                                            '2013/06/10',
                                                                                                            '33.670666,-117.841553',
                                                                                                            'Jazz', 8,
                                                                                                            1.7999999523162842),
                                                                                                            (True,
                                                                                                             datetime.date(
                                                                                                                 2012,
                                                                                                                 5, 10),
                                                                                                             None,
                                                                                                             datetime.datetime(
                                                                                                                 2014,
                                                                                                                 6, 24,
                                                                                                                 0, 0),
                                                                                                             5000000,
                                                                                                             [None,
                                                                                                              5700.0],
                                                                                                             '1980/04/10',
                                                                                                             'None',
                                                                                                             bytearray(
                                                                                                                 b'None'),
                                                                                                             None, [
                                                                                                                 'Megatron'],
                                                                                                             '2012/05/10',
                                                                                                             None,
                                                                                                             'Megatron',
                                                                                                             10,
                                                                                                             5.699999809265137),
                                                                                                            (True,
                                                                                                             datetime.date(
                                                                                                                 2011,
                                                                                                                 4, 10),
                                                                                                             None,
                                                                                                             datetime.datetime(
                                                                                                                 2014,
                                                                                                                 6, 24,
                                                                                                                 0, 0),
                                                                                                             5000000, [
                                                                                                                 91.44000244140625,
                                                                                                                 None],
                                                                                                             '1980/04/10',
                                                                                                             'Battle Station',
                                                                                                             bytearray(
                                                                                                                 b'Battle Station'),
                                                                                                             300, [
                                                                                                                 'Metroflex'],
                                                                                                             '2011/04/10',
                                                                                                             None,
                                                                                                             'Metroplex_)^$',
                                                                                                             8, None), (
                                                                                                            None, None,
                                                                                                            None, None,
                                                                                                            None, None,
                                                                                                            None, None,
                                                                                                            None, None,
                                                                                                            None, None,
                                                                                                            None, None,
                                                                                                            None,
                                                                                                            None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_sort_asc():
        actual_df = source_df.cols.sort('asc')
        expected_df = op.create.df(
            [('Cybertronian', BooleanType(), True), ('Date Type', DateType(), True), ('NullType', NullType(), True),
             ('Tiemstamp', TimestampType(), True), ('age', IntegerType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('date arrival', StringType(), True),
             ('function', StringType(), True), ('function(binary)', BinaryType(), True),
             ('height(ft)', ShortType(), True), ('japanese name', ArrayType(StringType(), True), True),
             ('last date seen', StringType(), True), ('last position seen', StringType(), True),
             ('names', StringType(), True), ('rank', ByteType(), True), ('weight(t)', FloatType(), True)], [(True,
                                                                                                             datetime.date(
                                                                                                                 2016,
                                                                                                                 9, 10),
                                                                                                             None,
                                                                                                             datetime.datetime(
                                                                                                                 2014,
                                                                                                                 6, 24,
                                                                                                                 0, 0),
                                                                                                             5000000, [
                                                                                                                 8.53439998626709,
                                                                                                                 4300.0],
                                                                                                             '1980/04/10',
                                                                                                             'Leader',
                                                                                                             bytearray(
                                                                                                                 b'Leader'),
                                                                                                             -28,
                                                                                                             ['Inochi',
                                                                                                              'Convoy'],
                                                                                                             '2016/09/10',
                                                                                                             '19.442735,-99.201111',
                                                                                                             "Optim'us",
                                                                                                             10,
                                                                                                             4.300000190734863),
                                                                                                            (True,
                                                                                                             datetime.date(
                                                                                                                 2015,
                                                                                                                 8, 10),
                                                                                                             None,
                                                                                                             datetime.datetime(
                                                                                                                 2014,
                                                                                                                 6, 24,
                                                                                                                 0, 0),
                                                                                                             5000000, [
                                                                                                                 5.334000110626221,
                                                                                                                 2000.0],
                                                                                                             '1980/04/10',
                                                                                                             'Espionage',
                                                                                                             bytearray(
                                                                                                                 b'Espionage'),
                                                                                                             17,
                                                                                                             ['Bumble',
                                                                                                              'Goldback'],
                                                                                                             '2015/08/10',
                                                                                                             '10.642707,-71.612534',
                                                                                                             'bumbl#ebéé  ',
                                                                                                             7, 2.0), (
                                                                                                            True,
                                                                                                            datetime.date(
                                                                                                                2014, 6,
                                                                                                                24),
                                                                                                            None,
                                                                                                            datetime.datetime(
                                                                                                                2014, 6,
                                                                                                                24, 0,
                                                                                                                0),
                                                                                                            5000000, [
                                                                                                                7.924799919128418,
                                                                                                                4000.0],
                                                                                                            '1980/04/10',
                                                                                                            'Security',
                                                                                                            bytearray(
                                                                                                                b'Security'),
                                                                                                            26, [
                                                                                                                'Roadbuster'],
                                                                                                            '2014/07/10',
                                                                                                            '37.789563,-122.400356',
                                                                                                            'ironhide&',
                                                                                                            7, 4.0), (
                                                                                                            True,
                                                                                                            datetime.date(
                                                                                                                2013, 6,
                                                                                                                24),
                                                                                                            None,
                                                                                                            datetime.datetime(
                                                                                                                2014, 6,
                                                                                                                24, 0,
                                                                                                                0),
                                                                                                            5000000, [
                                                                                                                3.962399959564209,
                                                                                                                1800.0],
                                                                                                            '1980/04/10',
                                                                                                            'First Lieutenant',
                                                                                                            bytearray(
                                                                                                                b'First Lieutenant'),
                                                                                                            13,
                                                                                                            ['Meister'],
                                                                                                            '2013/06/10',
                                                                                                            '33.670666,-117.841553',
                                                                                                            'Jazz', 8,
                                                                                                            1.7999999523162842),
                                                                                                            (True,
                                                                                                             datetime.date(
                                                                                                                 2012,
                                                                                                                 5, 10),
                                                                                                             None,
                                                                                                             datetime.datetime(
                                                                                                                 2014,
                                                                                                                 6, 24,
                                                                                                                 0, 0),
                                                                                                             5000000,
                                                                                                             [None,
                                                                                                              5700.0],
                                                                                                             '1980/04/10',
                                                                                                             'None',
                                                                                                             bytearray(
                                                                                                                 b'None'),
                                                                                                             None, [
                                                                                                                 'Megatron'],
                                                                                                             '2012/05/10',
                                                                                                             None,
                                                                                                             'Megatron',
                                                                                                             10,
                                                                                                             5.699999809265137),
                                                                                                            (True,
                                                                                                             datetime.date(
                                                                                                                 2011,
                                                                                                                 4, 10),
                                                                                                             None,
                                                                                                             datetime.datetime(
                                                                                                                 2014,
                                                                                                                 6, 24,
                                                                                                                 0, 0),
                                                                                                             5000000, [
                                                                                                                 91.44000244140625,
                                                                                                                 None],
                                                                                                             '1980/04/10',
                                                                                                             'Battle Station',
                                                                                                             bytearray(
                                                                                                                 b'Battle Station'),
                                                                                                             300, [
                                                                                                                 'Metroflex'],
                                                                                                             '2011/04/10',
                                                                                                             None,
                                                                                                             'Metroplex_)^$',
                                                                                                             8, None), (
                                                                                                            None, None,
                                                                                                            None, None,
                                                                                                            None, None,
                                                                                                            None, None,
                                                                                                            None, None,
                                                                                                            None, None,
                                                                                                            None, None,
                                                                                                            None,
                                                                                                            None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_sort_desc():
        actual_df = source_df.cols.sort('desc')
        expected_df = op.create.df(
            [('weight(t)', FloatType(), True), ('rank', ByteType(), True), ('names', StringType(), True),
             ('last position seen', StringType(), True), ('last date seen', StringType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('height(ft)', ShortType(), True),
             ('function(binary)', BinaryType(), True), ('function', StringType(), True),
             ('date arrival', StringType(), True), ('attributes', ArrayType(FloatType(), True), True),
             ('age', IntegerType(), True), ('Tiemstamp', TimestampType(), True), ('NullType', NullType(), True),
             ('Date Type', DateType(), True), ('Cybertronian', BooleanType(), True)], [(4.300000190734863, 10,
                                                                                        "Optim'us",
                                                                                        '19.442735,-99.201111',
                                                                                        '2016/09/10',
                                                                                        ['Inochi', 'Convoy'], -28,
                                                                                        bytearray(b'Leader'), 'Leader',
                                                                                        '1980/04/10',
                                                                                        [8.53439998626709, 4300.0],
                                                                                        5000000,
                                                                                        datetime.datetime(2014, 6, 24,
                                                                                                          0, 0), None,
                                                                                        datetime.date(2016, 9, 10),
                                                                                        True), (2.0, 7, 'bumbl#ebéé  ',
                                                                                                '10.642707,-71.612534',
                                                                                                '2015/08/10',
                                                                                                ['Bumble', 'Goldback'],
                                                                                                17,
                                                                                                bytearray(b'Espionage'),
                                                                                                'Espionage',
                                                                                                '1980/04/10',
                                                                                                [5.334000110626221,
                                                                                                 2000.0], 5000000,
                                                                                                datetime.datetime(2014,
                                                                                                                  6, 24,
                                                                                                                  0, 0),
                                                                                                None,
                                                                                                datetime.date(2015, 8,
                                                                                                              10),
                                                                                                True), (
                                                                                       4.0, 7, 'ironhide&',
                                                                                       '37.789563,-122.400356',
                                                                                       '2014/07/10', ['Roadbuster'], 26,
                                                                                       bytearray(b'Security'),
                                                                                       'Security', '1980/04/10',
                                                                                       [7.924799919128418, 4000.0],
                                                                                       5000000,
                                                                                       datetime.datetime(2014, 6, 24, 0,
                                                                                                         0), None,
                                                                                       datetime.date(2014, 6, 24),
                                                                                       True), (
                                                                                       1.7999999523162842, 8, 'Jazz',
                                                                                       '33.670666,-117.841553',
                                                                                       '2013/06/10', ['Meister'], 13,
                                                                                       bytearray(b'First Lieutenant'),
                                                                                       'First Lieutenant', '1980/04/10',
                                                                                       [3.962399959564209, 1800.0],
                                                                                       5000000,
                                                                                       datetime.datetime(2014, 6, 24, 0,
                                                                                                         0), None,
                                                                                       datetime.date(2013, 6, 24),
                                                                                       True), (5.699999809265137, 10,
                                                                                               'Megatron', None,
                                                                                               '2012/05/10',
                                                                                               ['Megatron'], None,
                                                                                               bytearray(b'None'),
                                                                                               'None', '1980/04/10',
                                                                                               [None, 5700.0], 5000000,
                                                                                               datetime.datetime(2014,
                                                                                                                 6, 24,
                                                                                                                 0, 0),
                                                                                               None,
                                                                                               datetime.date(2012, 5,
                                                                                                             10), True),
                                                                                       (None, 8, 'Metroplex_)^$', None,
                                                                                        '2011/04/10', ['Metroflex'],
                                                                                        300,
                                                                                        bytearray(b'Battle Station'),
                                                                                        'Battle Station', '1980/04/10',
                                                                                        [91.44000244140625, None],
                                                                                        5000000,
                                                                                        datetime.datetime(2014, 6, 24,
                                                                                                          0, 0), None,
                                                                                        datetime.date(2011, 4, 10),
                                                                                        True), (
                                                                                       None, None, None, None, None,
                                                                                       None, None, None, None, None,
                                                                                       None, None, None, None, None,
                                                                                       None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_std():
        actual_df = source_df.cols.std('height(ft)')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding(132.66612)
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_std_all_columns():
        actual_df = source_df.cols.std('*')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding({'height(ft)': 132.66612, 'rank': 1.36626, 'age': 0.0, 'weight(t)': 1.64712})
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_sub():
        actual_df = source_df.cols.sub(['height(ft)', 'rank'])
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', FloatType(), True), ('function', StringType(), True),
             ('rank', FloatType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True), ('sub', FloatType(), True)], [(
                                                                                                                     "Optim'us",
                                                                                                                     -28.0,
                                                                                                                     'Leader',
                                                                                                                     10.0,
                                                                                                                     5000000,
                                                                                                                     4.300000190734863,
                                                                                                                     [
                                                                                                                         'Inochi',
                                                                                                                         'Convoy'],
                                                                                                                     '19.442735,-99.201111',
                                                                                                                     '1980/04/10',
                                                                                                                     '2016/09/10',
                                                                                                                     [
                                                                                                                         8.53439998626709,
                                                                                                                         4300.0],
                                                                                                                     datetime.date(
                                                                                                                         2016,
                                                                                                                         9,
                                                                                                                         10),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'Leader'),
                                                                                                                     None,
                                                                                                                     -38.0),
                                                                                                                     (
                                                                                                                     'bumbl#ebéé  ',
                                                                                                                     17.0,
                                                                                                                     'Espionage',
                                                                                                                     7.0,
                                                                                                                     5000000,
                                                                                                                     2.0,
                                                                                                                     [
                                                                                                                         'Bumble',
                                                                                                                         'Goldback'],
                                                                                                                     '10.642707,-71.612534',
                                                                                                                     '1980/04/10',
                                                                                                                     '2015/08/10',
                                                                                                                     [
                                                                                                                         5.334000110626221,
                                                                                                                         2000.0],
                                                                                                                     datetime.date(
                                                                                                                         2015,
                                                                                                                         8,
                                                                                                                         10),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'Espionage'),
                                                                                                                     None,
                                                                                                                     10.0),
                                                                                                                     (
                                                                                                                     'ironhide&',
                                                                                                                     26.0,
                                                                                                                     'Security',
                                                                                                                     7.0,
                                                                                                                     5000000,
                                                                                                                     4.0,
                                                                                                                     [
                                                                                                                         'Roadbuster'],
                                                                                                                     '37.789563,-122.400356',
                                                                                                                     '1980/04/10',
                                                                                                                     '2014/07/10',
                                                                                                                     [
                                                                                                                         7.924799919128418,
                                                                                                                         4000.0],
                                                                                                                     datetime.date(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'Security'),
                                                                                                                     None,
                                                                                                                     19.0),
                                                                                                                     (
                                                                                                                     'Jazz',
                                                                                                                     13.0,
                                                                                                                     'First Lieutenant',
                                                                                                                     8.0,
                                                                                                                     5000000,
                                                                                                                     1.7999999523162842,
                                                                                                                     [
                                                                                                                         'Meister'],
                                                                                                                     '33.670666,-117.841553',
                                                                                                                     '1980/04/10',
                                                                                                                     '2013/06/10',
                                                                                                                     [
                                                                                                                         3.962399959564209,
                                                                                                                         1800.0],
                                                                                                                     datetime.date(
                                                                                                                         2013,
                                                                                                                         6,
                                                                                                                         24),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'First Lieutenant'),
                                                                                                                     None,
                                                                                                                     5.0),
                                                                                                                     (
                                                                                                                     'Megatron',
                                                                                                                     None,
                                                                                                                     'None',
                                                                                                                     10.0,
                                                                                                                     5000000,
                                                                                                                     5.699999809265137,
                                                                                                                     [
                                                                                                                         'Megatron'],
                                                                                                                     None,
                                                                                                                     '1980/04/10',
                                                                                                                     '2012/05/10',
                                                                                                                     [
                                                                                                                         None,
                                                                                                                         5700.0],
                                                                                                                     datetime.date(
                                                                                                                         2012,
                                                                                                                         5,
                                                                                                                         10),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'None'),
                                                                                                                     None,
                                                                                                                     None),
                                                                                                                     (
                                                                                                                     'Metroplex_)^$',
                                                                                                                     300.0,
                                                                                                                     'Battle Station',
                                                                                                                     8.0,
                                                                                                                     5000000,
                                                                                                                     None,
                                                                                                                     [
                                                                                                                         'Metroflex'],
                                                                                                                     None,
                                                                                                                     '1980/04/10',
                                                                                                                     '2011/04/10',
                                                                                                                     [
                                                                                                                         91.44000244140625,
                                                                                                                         None],
                                                                                                                     datetime.date(
                                                                                                                         2011,
                                                                                                                         4,
                                                                                                                         10),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'Battle Station'),
                                                                                                                     None,
                                                                                                                     292.0),
                                                                                                                     (
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_sub_all_columns():
        actual_df = source_df.cols.sub('*')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', FloatType(), True), ('function', StringType(), True),
             ('rank', FloatType(), True), ('age', FloatType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True), ('sub', FloatType(), True)], [(
                                                                                                                     "Optim'us",
                                                                                                                     -28.0,
                                                                                                                     'Leader',
                                                                                                                     10.0,
                                                                                                                     5000000.0,
                                                                                                                     4.300000190734863,
                                                                                                                     [
                                                                                                                         'Inochi',
                                                                                                                         'Convoy'],
                                                                                                                     '19.442735,-99.201111',
                                                                                                                     '1980/04/10',
                                                                                                                     '2016/09/10',
                                                                                                                     [
                                                                                                                         8.53439998626709,
                                                                                                                         4300.0],
                                                                                                                     datetime.date(
                                                                                                                         2016,
                                                                                                                         9,
                                                                                                                         10),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'Leader'),
                                                                                                                     None,
                                                                                                                     -5000042.5),
                                                                                                                     (
                                                                                                                     'bumbl#ebéé  ',
                                                                                                                     17.0,
                                                                                                                     'Espionage',
                                                                                                                     7.0,
                                                                                                                     5000000.0,
                                                                                                                     2.0,
                                                                                                                     [
                                                                                                                         'Bumble',
                                                                                                                         'Goldback'],
                                                                                                                     '10.642707,-71.612534',
                                                                                                                     '1980/04/10',
                                                                                                                     '2015/08/10',
                                                                                                                     [
                                                                                                                         5.334000110626221,
                                                                                                                         2000.0],
                                                                                                                     datetime.date(
                                                                                                                         2015,
                                                                                                                         8,
                                                                                                                         10),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'Espionage'),
                                                                                                                     None,
                                                                                                                     -4999992.0),
                                                                                                                     (
                                                                                                                     'ironhide&',
                                                                                                                     26.0,
                                                                                                                     'Security',
                                                                                                                     7.0,
                                                                                                                     5000000.0,
                                                                                                                     4.0,
                                                                                                                     [
                                                                                                                         'Roadbuster'],
                                                                                                                     '37.789563,-122.400356',
                                                                                                                     '1980/04/10',
                                                                                                                     '2014/07/10',
                                                                                                                     [
                                                                                                                         7.924799919128418,
                                                                                                                         4000.0],
                                                                                                                     datetime.date(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'Security'),
                                                                                                                     None,
                                                                                                                     -4999985.0),
                                                                                                                     (
                                                                                                                     'Jazz',
                                                                                                                     13.0,
                                                                                                                     'First Lieutenant',
                                                                                                                     8.0,
                                                                                                                     5000000.0,
                                                                                                                     1.7999999523162842,
                                                                                                                     [
                                                                                                                         'Meister'],
                                                                                                                     '33.670666,-117.841553',
                                                                                                                     '1980/04/10',
                                                                                                                     '2013/06/10',
                                                                                                                     [
                                                                                                                         3.962399959564209,
                                                                                                                         1800.0],
                                                                                                                     datetime.date(
                                                                                                                         2013,
                                                                                                                         6,
                                                                                                                         24),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'First Lieutenant'),
                                                                                                                     None,
                                                                                                                     -4999997.0),
                                                                                                                     (
                                                                                                                     'Megatron',
                                                                                                                     None,
                                                                                                                     'None',
                                                                                                                     10.0,
                                                                                                                     5000000.0,
                                                                                                                     5.699999809265137,
                                                                                                                     [
                                                                                                                         'Megatron'],
                                                                                                                     None,
                                                                                                                     '1980/04/10',
                                                                                                                     '2012/05/10',
                                                                                                                     [
                                                                                                                         None,
                                                                                                                         5700.0],
                                                                                                                     datetime.date(
                                                                                                                         2012,
                                                                                                                         5,
                                                                                                                         10),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'None'),
                                                                                                                     None,
                                                                                                                     None),
                                                                                                                     (
                                                                                                                     'Metroplex_)^$',
                                                                                                                     300.0,
                                                                                                                     'Battle Station',
                                                                                                                     8.0,
                                                                                                                     5000000.0,
                                                                                                                     None,
                                                                                                                     [
                                                                                                                         'Metroflex'],
                                                                                                                     None,
                                                                                                                     '1980/04/10',
                                                                                                                     '2011/04/10',
                                                                                                                     [
                                                                                                                         91.44000244140625,
                                                                                                                         None],
                                                                                                                     datetime.date(
                                                                                                                         2011,
                                                                                                                         4,
                                                                                                                         10),
                                                                                                                     datetime.datetime(
                                                                                                                         2014,
                                                                                                                         6,
                                                                                                                         24,
                                                                                                                         0,
                                                                                                                         0),
                                                                                                                     True,
                                                                                                                     bytearray(
                                                                                                                         b'Battle Station'),
                                                                                                                     None,
                                                                                                                     None),
                                                                                                                     (
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None,
                                                                                                                     None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_sum():
        actual_df = source_df.cols.sum('height(ft)')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding(328)
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_sum_all_columns():
        actual_df = source_df.cols.sum('*')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding({'height(ft)': 328, 'rank': 50, 'age': 30000000, 'weight(t)': 17.8})
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_trim():
        actual_df = source_df.cols.trim('height(ft)')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', StringType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("Optim'us", '-28', 'Leader',
                                                                                          10, 5000000,
                                                                                          4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         'bumbl#ebéé  ', '17',
                                                                                         'Espionage', 7, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         ('ironhide&', '26', 'Security',
                                                                                          7, 5000000, 4.0,
                                                                                          ['Roadbuster'],
                                                                                          '37.789563,-122.400356',
                                                                                          '1980/04/10', '2014/07/10',
                                                                                          [7.924799919128418, 4000.0],
                                                                                          datetime.date(2014, 6, 24),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Security'), None),
                                                                                         ('Jazz', '13',
                                                                                          'First Lieutenant', 8,
                                                                                          5000000, 1.7999999523162842,
                                                                                          ['Meister'],
                                                                                          '33.670666,-117.841553',
                                                                                          '1980/04/10', '2013/06/10',
                                                                                          [3.962399959564209, 1800.0],
                                                                                          datetime.date(2013, 6, 24),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(
                                                                                              b'First Lieutenant'),
                                                                                          None), (
                                                                                         'Megatron', None, 'None', 10,
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$', '300',
                                                                                         'Battle Station', 8, 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '1980/04/10', '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_trim_all_columns():
        actual_df = source_df.cols.trim('*')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', StringType(), True), ('function', StringType(), True),
             ('rank', StringType(), True), ('age', StringType(), True), ('weight(t)', StringType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', StringType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', StringType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("Optim'us", '-28', 'Leader',
                                                                                          '10', '5000000', '4.3',
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          '2016-09-10',
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0),
                                                                                          'true', bytearray(b'Leader'),
                                                                                          None), ('bumbl#ebéé', '17',
                                                                                                  'Espionage', '7',
                                                                                                  '5000000', '2.0',
                                                                                                  ['Bumble',
                                                                                                   'Goldback'],
                                                                                                  '10.642707,-71.612534',
                                                                                                  '1980/04/10',
                                                                                                  '2015/08/10',
                                                                                                  [5.334000110626221,
                                                                                                   2000.0],
                                                                                                  '2015-08-10',
                                                                                                  datetime.datetime(
                                                                                                      2014, 6, 24, 0,
                                                                                                      0), 'true',
                                                                                                  bytearray(
                                                                                                      b'Espionage'),
                                                                                                  None), (
                                                                                         'ironhide&', '26', 'Security',
                                                                                         '7', '5000000', '4.0',
                                                                                         ['Roadbuster'],
                                                                                         '37.789563,-122.400356',
                                                                                         '1980/04/10', '2014/07/10',
                                                                                         [7.924799919128418, 4000.0],
                                                                                         '2014-06-24',
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0),
                                                                                         'true', bytearray(b'Security'),
                                                                                         None), ('Jazz', '13',
                                                                                                 'First Lieutenant',
                                                                                                 '8', '5000000', '1.8',
                                                                                                 ['Meister'],
                                                                                                 '33.670666,-117.841553',
                                                                                                 '1980/04/10',
                                                                                                 '2013/06/10',
                                                                                                 [3.962399959564209,
                                                                                                  1800.0], '2013-06-24',
                                                                                                 datetime.datetime(2014,
                                                                                                                   6,
                                                                                                                   24,
                                                                                                                   0,
                                                                                                                   0),
                                                                                                 'true', bytearray(
                b'First Lieutenant'), None), ('Megatron', None, 'None', '10', '5000000', '5.7', ['Megatron'], None,
                                              '1980/04/10', '2012/05/10', [None, 5700.0], '2012-05-10',
                                              datetime.datetime(2014, 6, 24, 0, 0), 'true', bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$', '300',
                                                                                         'Battle Station', '8',
                                                                                         '5000000', None, ['Metroflex'],
                                                                                         None, '1980/04/10',
                                                                                         '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         '2011-04-10',
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0),
                                                                                         'true',
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_unique():
        actual_df = source_df.cols.unique('height(ft)')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding({'height(ft)': [300, 26, None, 13, 17, -28]})
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_unique_all_columns():
        actual_df = source_df.cols.unique('*')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding(
            {'names': ['Jazz', None, 'bumbl#ebéé  ', 'ironhide&', "Optim'us", 'Megatron', 'Metroplex_)^$'],
             'height(ft)': [300, 26, None, 13, 17, -28],
             'function': ['Leader', 'First Lieutenant', 'None', 'Security', None, 'Espionage', 'Battle Station'],
             'rank': [None, 8, 7, 10], 'age': [None, 5000000],
             'weight(t)': [5.699999809265137, None, 2.0, 1.7999999523162842, 4.0, 4.300000190734863],
             'japanese name': [['Metroflex'], ['Bumble', 'Goldback'], None, ['Inochi', 'Convoy'], ['Megatron'],
                               ['Meister'], ['Roadbuster']],
             'last position seen': [None, '37.789563,-122.400356', '19.442735,-99.201111', '33.670666,-117.841553',
                                    '10.642707,-71.612534'], 'date arrival': [None, '1980/04/10'],
             'last date seen': ['2011/04/10', None, '2012/05/10', '2013/06/10', '2015/08/10', '2014/07/10',
                                '2016/09/10'],
             'attributes': [[3.962399959564209, 1800.0], [None, 5700.0], None, [8.53439998626709, 4300.0],
                            [7.924799919128418, 4000.0], [91.44000244140625, None], [5.334000110626221, 2000.0]],
             'Date Type': [datetime.date(2012, 5, 10), datetime.date(2015, 8, 10), None, datetime.date(2011, 4, 10),
                           datetime.date(2013, 6, 24), datetime.date(2014, 6, 24), datetime.date(2016, 9, 10)],
             'Tiemstamp': [datetime.datetime(2014, 6, 24, 0, 0), None], 'Cybertronian': [None, True],
             'function(binary)': [bytearray(b'Leader'), bytearray(b'First Lieutenant'), bytearray(b'None'),
                                  bytearray(b'Security'), None, bytearray(b'Espionage'), bytearray(b'Battle Station')],
             'NullType': [None]})
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_unnest_array():
        actual_df = source_df.cols.unnest('attributes')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True),
             ('attributes_0', FloatType(), True), ('attributes_1', FloatType(), True)], [("Optim'us", -28, 'Leader', 10,
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None,
                                                                                          8.53439998626709, 4300.0), (
                                                                                         'bumbl#ebéé  ', 17,
                                                                                         'Espionage', 7, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None,
                                                                                         5.334000110626221, 2000.0), (
                                                                                         'ironhide&', 26, 'Security', 7,
                                                                                         5000000, 4.0, ['Roadbuster'],
                                                                                         '37.789563,-122.400356',
                                                                                         '1980/04/10', '2014/07/10',
                                                                                         [7.924799919128418, 4000.0],
                                                                                         datetime.date(2014, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Security'), None,
                                                                                         7.924799919128418, 4000.0), (
                                                                                         'Jazz', 13, 'First Lieutenant',
                                                                                         8, 5000000, 1.7999999523162842,
                                                                                         ['Meister'],
                                                                                         '33.670666,-117.841553',
                                                                                         '1980/04/10', '2013/06/10',
                                                                                         [3.962399959564209, 1800.0],
                                                                                         datetime.date(2013, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'First Lieutenant'),
                                                                                         None, 3.962399959564209,
                                                                                         1800.0), (
                                                                                         'Megatron', None, 'None', 10,
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None, None,
                                                                                         5700.0), ('Metroplex_)^$', 300,
                                                                                                   'Battle Station', 8,
                                                                                                   5000000, None,
                                                                                                   ['Metroflex'], None,
                                                                                                   '1980/04/10',
                                                                                                   '2011/04/10',
                                                                                                   [91.44000244140625,
                                                                                                    None],
                                                                                                   datetime.date(2011,
                                                                                                                 4, 10),
                                                                                                   datetime.datetime(
                                                                                                       2014, 6, 24, 0,
                                                                                                       0), True,
                                                                                                   bytearray(
                                                                                                       b'Battle Station'),
                                                                                                   None,
                                                                                                   91.44000244140625,
                                                                                                   None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_unnest_array_all_columns():
        actual_df = source_df.cols.unnest('attributes')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True),
             ('attributes_0', FloatType(), True), ('attributes_1', FloatType(), True)], [("Optim'us", -28, 'Leader', 10,
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None,
                                                                                          8.53439998626709, 4300.0), (
                                                                                         'bumbl#ebéé  ', 17,
                                                                                         'Espionage', 7, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None,
                                                                                         5.334000110626221, 2000.0), (
                                                                                         'ironhide&', 26, 'Security', 7,
                                                                                         5000000, 4.0, ['Roadbuster'],
                                                                                         '37.789563,-122.400356',
                                                                                         '1980/04/10', '2014/07/10',
                                                                                         [7.924799919128418, 4000.0],
                                                                                         datetime.date(2014, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Security'), None,
                                                                                         7.924799919128418, 4000.0), (
                                                                                         'Jazz', 13, 'First Lieutenant',
                                                                                         8, 5000000, 1.7999999523162842,
                                                                                         ['Meister'],
                                                                                         '33.670666,-117.841553',
                                                                                         '1980/04/10', '2013/06/10',
                                                                                         [3.962399959564209, 1800.0],
                                                                                         datetime.date(2013, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'First Lieutenant'),
                                                                                         None, 3.962399959564209,
                                                                                         1800.0), (
                                                                                         'Megatron', None, 'None', 10,
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None, None,
                                                                                         5700.0), ('Metroplex_)^$', 300,
                                                                                                   'Battle Station', 8,
                                                                                                   5000000, None,
                                                                                                   ['Metroflex'], None,
                                                                                                   '1980/04/10',
                                                                                                   '2011/04/10',
                                                                                                   [91.44000244140625,
                                                                                                    None],
                                                                                                   datetime.date(2011,
                                                                                                                 4, 10),
                                                                                                   datetime.datetime(
                                                                                                       2014, 6, 24, 0,
                                                                                                       0), True,
                                                                                                   bytearray(
                                                                                                       b'Battle Station'),
                                                                                                   None,
                                                                                                   91.44000244140625,
                                                                                                   None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_upper():
        actual_df = source_df.cols.upper('function')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("Optim'us", -28, 'LEADER', 10,
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         'bumbl#ebéé  ', 17,
                                                                                         'ESPIONAGE', 7, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         (
                                                                                         'ironhide&', 26, 'SECURITY', 7,
                                                                                         5000000, 4.0, ['Roadbuster'],
                                                                                         '37.789563,-122.400356',
                                                                                         '1980/04/10', '2014/07/10',
                                                                                         [7.924799919128418, 4000.0],
                                                                                         datetime.date(2014, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Security'), None),
                                                                                         (
                                                                                         'Jazz', 13, 'FIRST LIEUTENANT',
                                                                                         8, 5000000, 1.7999999523162842,
                                                                                         ['Meister'],
                                                                                         '33.670666,-117.841553',
                                                                                         '1980/04/10', '2013/06/10',
                                                                                         [3.962399959564209, 1800.0],
                                                                                         datetime.date(2013, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'First Lieutenant'),
                                                                                         None), (
                                                                                         'Megatron', None, 'NONE', 10,
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$', 300,
                                                                                         'BATTLE STATION', 8, 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '1980/04/10', '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_upper_all_columns():
        actual_df = source_df.cols.upper('*')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', ShortType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [("OPTIM'US", -28, 'LEADER', 10,
                                                                                          5000000, 4.300000190734863,
                                                                                          ['Inochi', 'Convoy'],
                                                                                          '19.442735,-99.201111',
                                                                                          '1980/04/10', '2016/09/10',
                                                                                          [8.53439998626709, 4300.0],
                                                                                          datetime.date(2016, 9, 10),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Leader'), None), (
                                                                                         'BUMBL#EBÉÉ  ', 17,
                                                                                         'ESPIONAGE', 7, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         (
                                                                                         'IRONHIDE&', 26, 'SECURITY', 7,
                                                                                         5000000, 4.0, ['Roadbuster'],
                                                                                         '37.789563,-122.400356',
                                                                                         '1980/04/10', '2014/07/10',
                                                                                         [7.924799919128418, 4000.0],
                                                                                         datetime.date(2014, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Security'), None),
                                                                                         (
                                                                                         'JAZZ', 13, 'FIRST LIEUTENANT',
                                                                                         8, 5000000, 1.7999999523162842,
                                                                                         ['Meister'],
                                                                                         '33.670666,-117.841553',
                                                                                         '1980/04/10', '2013/06/10',
                                                                                         [3.962399959564209, 1800.0],
                                                                                         datetime.date(2013, 6, 24),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'First Lieutenant'),
                                                                                         None), (
                                                                                         'MEGATRON', None, 'NONE', 10,
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'METROPLEX_)^$', 300,
                                                                                         'BATTLE STATION', 8, 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '1980/04/10', '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_variance():
        actual_df = source_df.cols.variance('height(ft)')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding(17600.3)
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_variance_all_columns():
        actual_df = source_df.cols.variance('*')
        actual_df = json_enconding(actual_df)
        expected_value = json_enconding({'height(ft)': 17600.3, 'rank': 1.86667, 'age': 0.0, 'weight(t)': 2.713})
        assert (expected_value == actual_df)

    @staticmethod
    def test_cols_z_score():
        actual_df = source_df.cols.z_score('height(ft)')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', DoubleType(), True), ('function', StringType(), True),
             ('rank', ByteType(), True), ('age', IntegerType(), True), ('weight(t)', FloatType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [(
                                                                                         "Optim'us", 0.7055305454022474,
                                                                                         'Leader', 10, 5000000,
                                                                                         4.300000190734863,
                                                                                         ['Inochi', 'Convoy'],
                                                                                         '19.442735,-99.201111',
                                                                                         '1980/04/10', '2016/09/10',
                                                                                         [8.53439998626709, 4300.0],
                                                                                         datetime.date(2016, 9, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Leader'), None), (
                                                                                         'bumbl#ebéé  ',
                                                                                         0.366333167805013, 'Espionage',
                                                                                         7, 5000000, 2.0,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         ('ironhide&',
                                                                                          0.29849369228556616,
                                                                                          'Security', 7, 5000000, 4.0,
                                                                                          ['Roadbuster'],
                                                                                          '37.789563,-122.400356',
                                                                                          '1980/04/10', '2014/07/10',
                                                                                          [7.924799919128418, 4000.0],
                                                                                          datetime.date(2014, 6, 24),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Security'), None),
                                                                                         ('Jazz', 0.39648404581365604,
                                                                                          'First Lieutenant', 8,
                                                                                          5000000, 1.7999999523162842,
                                                                                          ['Meister'],
                                                                                          '33.670666,-117.841553',
                                                                                          '1980/04/10', '2013/06/10',
                                                                                          [3.962399959564209, 1800.0],
                                                                                          datetime.date(2013, 6, 24),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(
                                                                                              b'First Lieutenant'),
                                                                                          None), (
                                                                                         'Megatron', None, 'None', 10,
                                                                                         5000000, 5.699999809265137,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$',
                                                                                         1.7668414513064827,
                                                                                         'Battle Station', 8, 5000000,
                                                                                         None, ['Metroflex'], None,
                                                                                         '1980/04/10', '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

    @staticmethod
    def test_cols_z_score_all_columns():
        actual_df = source_df.cols.z_score('*')
        expected_df = op.create.df(
            [('names', StringType(), True), ('height(ft)', DoubleType(), True), ('function', StringType(), True),
             ('rank', DoubleType(), True), ('age', DoubleType(), True), ('weight(t)', DoubleType(), True),
             ('japanese name', ArrayType(StringType(), True), True), ('last position seen', StringType(), True),
             ('date arrival', StringType(), True), ('last date seen', StringType(), True),
             ('attributes', ArrayType(FloatType(), True), True), ('Date Type', DateType(), True),
             ('Tiemstamp', TimestampType(), True), ('Cybertronian', BooleanType(), True),
             ('function(binary)', BinaryType(), True), ('NullType', NullType(), True)], [(
                                                                                         "Optim'us", 0.7055305454022474,
                                                                                         'Leader', 1.2198776221217045,
                                                                                         None, 0.4492691429494289,
                                                                                         ['Inochi', 'Convoy'],
                                                                                         '19.442735,-99.201111',
                                                                                         '1980/04/10', '2016/09/10',
                                                                                         [8.53439998626709, 4300.0],
                                                                                         datetime.date(2016, 9, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Leader'), None), (
                                                                                         'bumbl#ebéé  ',
                                                                                         0.366333167805013, 'Espionage',
                                                                                         0.9758977061467071, None,
                                                                                         0.9471076788576425,
                                                                                         ['Bumble', 'Goldback'],
                                                                                         '10.642707,-71.612534',
                                                                                         '1980/04/10', '2015/08/10',
                                                                                         [5.334000110626221, 2000.0],
                                                                                         datetime.date(2015, 8, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Espionage'), None),
                                                                                         ('ironhide&',
                                                                                          0.29849369228556616,
                                                                                          'Security',
                                                                                          0.9758977061467071, None,
                                                                                          0.2671329350624119,
                                                                                          ['Roadbuster'],
                                                                                          '37.789563,-122.400356',
                                                                                          '1980/04/10', '2014/07/10',
                                                                                          [7.924799919128418, 4000.0],
                                                                                          datetime.date(2014, 6, 24),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(b'Security'), None),
                                                                                         ('Jazz', 0.39648404581365604,
                                                                                          'First Lieutenant',
                                                                                          0.24397259672390328, None,
                                                                                          1.0685317691994, ['Meister'],
                                                                                          '33.670666,-117.841553',
                                                                                          '1980/04/10', '2013/06/10',
                                                                                          [3.962399959564209, 1800.0],
                                                                                          datetime.date(2013, 6, 24),
                                                                                          datetime.datetime(2014, 6, 24,
                                                                                                            0, 0), True,
                                                                                          bytearray(
                                                                                              b'First Lieutenant'),
                                                                                          None), (
                                                                                         'Megatron', None, 'None',
                                                                                         1.2198776221217045, None,
                                                                                         1.2992373410954494,
                                                                                         ['Megatron'], None,
                                                                                         '1980/04/10', '2012/05/10',
                                                                                         [None, 5700.0],
                                                                                         datetime.date(2012, 5, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'None'), None), (
                                                                                         'Metroplex_)^$',
                                                                                         1.7668414513064827,
                                                                                         'Battle Station',
                                                                                         0.24397259672390328, None,
                                                                                         None, ['Metroflex'], None,
                                                                                         '1980/04/10', '2011/04/10',
                                                                                         [91.44000244140625, None],
                                                                                         datetime.date(2011, 4, 10),
                                                                                         datetime.datetime(2014, 6, 24,
                                                                                                           0, 0), True,
                                                                                         bytearray(b'Battle Station'),
                                                                                         None), (
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None, None, None, None, None,
                                                                                         None)])
        assert (expected_df.collect() == actual_df.collect())

