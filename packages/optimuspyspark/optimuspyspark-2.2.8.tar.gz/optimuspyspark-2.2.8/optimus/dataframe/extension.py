import json

import humanize
import imgkit
import jinja2
import math
from packaging import version
from pyspark.ml.feature import SQLTransformer
from pyspark.ml.stat import Correlation
from pyspark.serializers import PickleSerializer, AutoBatchedSerializer
from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import *

from optimus import val_to_list
from optimus.helpers.check import is_str
from optimus.helpers.columns import parse_columns, name_col
from optimus.helpers.constants import PYSPARK_NUMERIC_TYPES
from optimus.helpers.decorators import *
from optimus.helpers.functions import collect_as_dict, random_int, traverse, absolute_path
from optimus.helpers.json import json_converter
from optimus.helpers.logger import logger
from optimus.helpers.output import print_html
from optimus.helpers.raiseit import RaiseIt
from optimus.profiler.templates.html import HEADER, FOOTER
from optimus.spark import Spark


@add_method(DataFrame)
def roll_out():
    """
    Just a function to check if the Spark dataframe has been Monkey Patched
    :return:
    """
    print("Yes!")


@add_method(DataFrame)
def to_json(self):
    """
    Return a json from a Spark Dataframe
    :param self:
    :return:
    """
    return json.loads(json.dumps(collect_as_dict(self), ensure_ascii=False, default=json_converter))


@add_method(DataFrame)
def export(self):
    """
    Helper function to export all the dataframe in text format. Aimed to be used in test functions
    :param self:
    :return:
    """
    dict_result = {}
    value = self.collect()
    schema = []
    for col_names in self.cols.names():
        name = col_names

        data_type = self.cols.schema_dtype(col_names)
        if isinstance(data_type, ArrayType):
            data_type = "ArrayType(" + str(data_type.elementType) + "()," + str(data_type.containsNull) + ")"
        else:
            data_type = str(data_type) + "()"

        nullable = self.schema[col_names].nullable

        schema.append("('{name}', {dataType}, {nullable})".format(name=name, dataType=data_type, nullable=nullable))
    schema = ",".join(schema)
    schema = "[" + schema + "]"

    # if there is only an element in the dict just return the value
    if len(dict_result) == 1:
        dict_result = next(iter(dict_result.values()))
    else:
        dict_result = [tuple(v.asDict().values()) for v in value]

    def func(path, _value):
        try:
            if math.isnan(_value):
                r = None
            else:
                r = _value
        except TypeError:
            r = _value
        return r

    dict_result = traverse(dict_result, None, func)

    return "{schema}, {dict_result}".format(schema=schema, dict_result=dict_result)


@add_method(DataFrame)
def sample_n(self, n=10, random=False):
    """
    Return a n number of sample from a dataFrame
    :param self:
    :param n: Number of samples
    :param random: if true get a semi random sample
    :return:
    """
    if random is True:
        seed = random_int()
    elif random is False:
        seed = 0
    else:
        RaiseIt.value_error(random, ["True", "False"])

    rows_count = self.count()
    if n < rows_count:
        fraction = n / rows_count
    else:
        fraction = 1.0

    return self.sample(False, fraction, seed=seed)


@add_method(DataFrame)
def pivot(self, index, column, values):
    """
    Return reshaped DataFrame organized by given index / column values.
    :param self: Spark Dataframe
    :param index: Column to use to make new frame's index.
    :param column: Column to use to make new frame's columns.
    :param values: Column(s) to use for populating new frame's values.
    :return:
    """
    return self.groupby(index).pivot(column).agg(F.first(values))


@add_method(DataFrame)
def melt(self, id_vars, value_vars, var_name="variable", value_name="value", data_type="str"):
    """
    Convert DataFrame from wide to long format.
    :param self: Spark Dataframe
    :param id_vars: column with unique values
    :param value_vars: Column names that are going to be converted to columns values
    :param var_name: Column name for vars
    :param value_name: Column name for values
    :param data_type: All columns must have the same type. It will transform all columns to this data type.
    :return:
    """

    df = self
    id_vars = val_to_list(id_vars)
    # Cast all columns to the same type
    df = df.cols.cast(id_vars + value_vars, data_type)

    vars_and_vals = [F.struct(F.lit(c).alias(var_name), F.col(c).alias(value_name)) for c in value_vars]

    # Add to the DataFrame and explode
    df = df.withColumn("vars_and_vals", F.explode(F.array(*vars_and_vals)))

    cols = id_vars + [F.col("vars_and_vals")[x].alias(x) for x in [var_name, value_name]]

    return df.select(*cols)


@add_method(DataFrame)
def size(self):
    """
    Get the size of a dataframe in bytes
    :param self: Spark Dataframe
    :return:
    """

    def _to_java_object_rdd(rdd):
        """
        Return a JavaRDD of Object by unpickling
        It will convert each Python object into Java object by Pyrolite, whenever the
        RDD is serialized in batch or not.
        """
        rdd = rdd._reserialize(AutoBatchedSerializer(PickleSerializer()))
        return rdd.ctx._jvm.org.apache.spark.mllib.api.python.SerDe.pythonToJava(rdd._jrdd, True)

    if version.parse(Spark.instance.spark.version) < version.parse("2.4.0"):
        java_obj = _to_java_object_rdd(self.rdd)
        n_bytes = Spark.instance.sc._jvm.org.apache.spark.util.SizeEstimator.estimate(java_obj)
    else:
        # TODO: Find a way to calculate the dataframe size in spark 2.4
        n_bytes = -1

    return n_bytes


@add_method(DataFrame)
def run(self):
    """
    This method is a very useful function to break lineage of transformations. By default Spark uses the lazy
    evaluation approach in processing data: transformation functions are not computed into an action is called.
    Sometimes when transformations are numerous, the computations are very extensive because the high number of
    operations that spark needs to run in order to get the results.

    Other important thing is that Apache Spark save task but not result of dataFrame, so tasks are
    accumulated and the same situation happens.

    :param self: Spark Dataframe
    :return:
    """

    self.cache().count()
    return self


@add_method(DataFrame)
def query(self, sql_expression):
    """
    Implements the transformations which are defined by SQL statement. Currently we only support
    SQL syntax like "SELECT ... FROM __THIS__ ..." where "__THIS__" represents the
    underlying table of the input dataframe.
    :param self: Spark Dataframe
    :param sql_expression: SQL expression.
    :return: Dataframe with columns changed by SQL statement.
    """
    sql_transformer = SQLTransformer(statement=sql_expression)
    return sql_transformer.transform(self)


@add_method(DataFrame)
def table_name(self, name=None):
    """
    Create a temp view for a data frame
    :param self:
    :param name:
    :return:
    """
    if not is_str(name):
        RaiseIt.type_error(name, ["string"])

    if len(name) is 0:
        RaiseIt.value_error(name, ["> 0"])

    self.createOrReplaceTempView(name)
    return self


@add_attr(DataFrame)
def partitions(self):
    """
    Return the dataframe partitions number
    :param self: Spark Dataframe
    :return: Number of partitions
    """
    return self.rdd.getNumPartitions()


@add_attr(DataFrame)
def partitioner(self):
    """
    Return the algorithm used to partition the dataframe
    :param self: Spark Dataframe
    :return:
    """
    return self.rdd.partitioner


@add_attr(DataFrame)
def glom(self):
    """

    :param self: Spark Dataframe
    :return:
    """
    return collect_as_dict(self.rdd.glom().collect()[0])


@add_method(DataFrame)
def h_repartition(self, partitions_number=None, col_name=None):
    """
    Apply a repartition to a datataframe based in some heuristics. Also you can pass the number of partitions and
    a column if you need more control.
    See
    https://stackoverflow.com/questions/35800795/number-of-partitions-in-rdd-and-performance-in-spark/35804407#35804407
    :param self: Spark Dataframe
    :param partitions_number: Number of partitions
    :param col_name: Column to be used to apply the repartition id necessary
    :return:
    """
    if partitions_number is None:
        partitions_number = Spark.instance.parallelism * 4

    if col_name is None:
        df = self.repartition(partitions_number)
    else:
        df = self.repartition(partitions_number, col_name)
    return df


@add_method(DataFrame)
def table_image(self, path, limit=10):
    """

    :param self:
    :param limit:
    :param path:
    :return:
    """

    css = absolute_path("/css/styles.css")

    imgkit.from_string(self.table_html(limit=limit, full=True), path, css=css)
    print_html("<img src='" + path + "'>")


@add_method(DataFrame)
def table_html(self, limit=10, columns=None, title=None, full=False):
    """
    Return a HTML table with the dataframe cols, data types and values
    :param self:
    :param columns: Columns to be printed
    :param limit: How many rows will be printed
    :param title: Table title
    :param full: Include html header and footer

    :return:
    """

    columns = parse_columns(self, columns)

    if limit is None:
        limit = 10

    if limit == "all":

        data = collect_as_dict(self.cols.select(columns))
    else:
        data = collect_as_dict(self.cols.select(columns).limit(limit))

    # Load the Jinja template
    template_loader = jinja2.FileSystemLoader(searchpath=absolute_path("/templates"))
    template_env = jinja2.Environment(loader=template_loader, autoescape=True)
    template = template_env.get_template("table.html")

    # Filter only the columns and data type info need it
    dtypes = [(i[0], i[1], j.nullable,) for i, j in zip(self.dtypes, self.schema)]

    # Remove not selected columns
    final_columns = []
    for i in dtypes:
        for j in columns:
            if i[0] == j:
                final_columns.append(i)

    total_rows = self.count()
    if limit == "all":
        limit = total_rows
    elif total_rows < limit:
        limit = total_rows

    total_rows = humanize.intword(total_rows)
    total_cols = self.cols.count()
    total_partitions = self.partitions()

    output = template.render(cols=final_columns, data=data, limit=limit, total_rows=total_rows, total_cols=total_cols,
                             partitions=total_partitions, title=title)

    if full is True:
        output = HEADER + output + FOOTER
    return output


@add_method(DataFrame)
def table(self, limit=None, columns=None, title=None):
    try:
        if __IPYTHON__ and DataFrame.output is "html":
            result = self.table_html(title=title, limit=limit, columns=columns)
            print_html(result)
        else:
            self.show()
    except NameError:

        self.show()


@add_method(DataFrame)
def correlation(self, input_cols, method="pearson", output="json"):
    """
    Calculate the correlation between columns. It will try to cast a column to float where necessary and impute
    missing values
    :param self:
    :param input_cols: Columns to be processed
    :param method: Method used to calculate the correlation
    :param output: array or json
    :return:
    """

    df = self

    # Values in columns can not be null. Warn user
    input_cols = parse_columns(self, input_cols, filter_by_column_dtypes=PYSPARK_NUMERIC_TYPES)
    # try to parse the select column to float and create a vector

    # print(self.cols.count_na(input_cols))

    # Input is not a vector transform to a vector
    output_col = name_col(input_cols, "correlation")
    if len(input_cols) > 1:
        for col_name in input_cols:
            df = df.cols.cast(col_name, "float")
            logger.print("Casting {col_name} to float...".format(col_name=col_name))

        df = df.cols.nest(input_cols, "vector", output_cols=output_col)

    corr = Correlation.corr(df, output_col, method).head()[0].toArray()

    if output is "array":
        result = corr

    elif output is "json":

        # Parse result to json
        col_pair = []
        for col_name in input_cols:
            for col_name_2 in input_cols:
                col_pair.append({"between": col_name, "an": col_name_2})

        # flat array
        values = corr.flatten('F').tolist()

        result = []
        for n, v in zip(col_pair, values):
            # Remove correlation between the same column
            if n["between"] is not n["an"]:
                n["value"] = v
                result.append(n)

        result = sorted(result, key=lambda k: k['value'], reverse=True)

    return {"cols":input_cols, "data":result}


@add_method(DataFrame)
def load_schema(self, spreadsheet_id, range_name):
    """
    Retrieve sheet data using OAuth credentials and Google Python API.
    :param self:
    :param spreadsheet_id:
    :param range_name:
    :return:
    """
    scopes = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    # Setup the Sheets API
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', scopes)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    gsheet = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()


@add_method(DataFrame)
def create_id(self, column="id"):
    """
    Create a unique id for every row.
    :param self:
    :param column:
    :return:
    """

    return self.withColumn(column, F.monotonically_increasing_id())
