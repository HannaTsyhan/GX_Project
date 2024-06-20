import os
import great_expectations as gx
from great_expectations.checkpoint import Checkpoint
from dotenv import load_dotenv


if __name__ == '__main__':
    load_dotenv()
    context = gx.get_context()
    context.build_data_docs()
    connection_string = f"mssql+pyodbc://{os.getenv('USERID')}:{os.getenv('PASSWORD')}@localhost:1433/AdventureWorks2012?driver=ODBC+Driver+17+for+SQL+Server&charset=utf&autocommit=true"

    datasource = context.sources.add_or_update_sql(
        name="my_datasource", connection_string=connection_string
    )

    table_asset = datasource.add_table_asset(name="my_asset", schema_name="Production", table_name="Product")

    my_asset = context.get_datasource("my_datasource").get_asset("my_asset")
    query_asset = datasource.add_query_asset(name="my_query_asset", query="SELECT  * from Production.Product")

    my_batch_request = my_asset.build_batch_request()

    context.add_or_update_expectation_suite("my_expectation_suite")

    validator = context.get_validator(
        batch_request=my_batch_request,
        expectation_suite_name="my_expectation_suite",
    )
    validator.head()
    validator.expect_column_values_to_not_be_null(column="ProductID")
    validator.expect_column_values_to_be_unique(column="ProductID")
    validator.expect_column_values_to_not_be_null(column="Color", strictly=True)
    validator.expect_column_values_to_not_be_null(column="Name")
    validator.expect_column_values_to_not_be_null(column="ProductNumber")

    expected_class_values = ["H", "M", "L"]
    validator.expect_column_values_to_be_in_set("Class", value_set=expected_class_values)
    expected_weight_unit_values = ["LB", "G"]
    validator.expect_column_values_to_be_in_set("WeightUnitMeasureCode", value_set=expected_weight_unit_values)
    expected_color_values = ["Black", "Blue", "Grey", "Multi", "Red", "Silver", "Yellow", "Silver/Black", "White"]
    validator.expect_column_values_to_be_in_set("Color", value_set=expected_color_values)
    validator.expect_column_mean_to_be_between('Weight', min_value=2.10, max_value=1050)

    validator.save_expectation_suite(discard_failed_expectations=False)


    checkpoint: Checkpoint = Checkpoint(
        name="my_checkpoint",
        run_name_template="%Y%m%d-%H%M%S-my-run-name-template",
        data_context=context,
        batch_request=my_batch_request,
        expectation_suite_name="my_expectation_suite",
        validations=[
            {
                "batch_request": my_batch_request,
                "expectation_suite_name": "my_expectation_suite",
            },
        ],
        action_list=[
            {
                "name": "store_validation_result",
                "action": {"class_name": "StoreValidationResultAction"},
            },
            {
                "name": "store_evaluation_params",
                "action": {"class_name": "StoreEvaluationParametersAction"},
            },
            {
                    "name": "update_data_docs",
                    "action": {"class_name": "UpdateDataDocsAction"}
            }
        ],
        evaluation_parameters={"GT_PARAM": 1000, "LT_PARAM": 50000},
        runtime_configuration={
            "result_format": {
                "result_format": "BOOLEAN_ONLY",
                "unexpected_index_column_names": ["ProductID"],
                "return_unexpected_index_query": True,
            },
        },
    )

    checkpoint_result = checkpoint.run()
    context.build_data_docs()
    context.open_data_docs()