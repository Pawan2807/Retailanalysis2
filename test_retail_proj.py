import pytest
from lib.DataReader import read_customers ,read_orders 
from lib.DataManipulation import filter_closed_orders,count_orders_state,filter_orders_generic
from lib.ConfigReader import get_app_config


@pytest.mark.skip()
def test_read_customers_df(spark):
    customers_count=read_customers(spark,"LOCAL").count()
    assert customers_count== 12435


@pytest.mark.skip()
def test_read_orders_df(spark):
    orders_count=read_orders(spark,"LOCAL").count()
    assert orders_count== 68884
   

@pytest.mark.skip("work in progress")
def test_filter_closed_orders(spark):
    orders_df=read_orders(spark,"LOCAL")
    filtered_count=filter_closed_orders(orders_df).count()
    assert filtered_count==7556

@pytest.mark.skip()
def test_read_app_config():
    config=get_app_config("LOCAL")
    assert config["orders.file.path"]== "data/orders.csv"

@pytest.mark.skip()
def test_count_orders_state(spark, expected_results):
    customers_df = read_customers(spark,"LOCAL")
    actual_results=count_orders_state(customers_df)
    assert actual_results.collect() == expected_results.collect()


@pytest.mark.skip()
def test_check_closed_count(spark) :
    orders_df=read_orders(spark,"LOCAL")
    filtered_count=filter_orders_generic(orders_df,"CLOSED").count()
    assert filtered_count==7556



@pytest.mark.skip()
def test_check_pendingpayment_count(spark) :
    orders_df=read_orders(spark,"LOCAL")
    filtered_count=filter_orders_generic(orders_df,"PENDING_PAYMENT").count()
    assert filtered_count==15030


@pytest.mark.skip()
def test_check_complete_count(spark) :
    orders_df=read_orders(spark,"LOCAL")
    filtered_count=filter_orders_generic(orders_df,"COMPLETE").count()
    assert filtered_count==22900


@pytest.mark.parametrize(
       "status,count",
       [("PENDING_PAYMENT",15030),
        ("COMPLETE",22900),
        ("ON_HOLD",3798),
        ("PAYMENT_REVIEW", 729),
        ("PROCESSING",8275),
        ("CLOSED", 7556),
        ("SUSPECTED_FRAUD",1558),
        ("PENDING",7610),
        ("CANCELED",1428)
       ]       
)
def test_check_count(spark,status,count):
    orders_df=read_orders(spark,"LOCAL")
    filtered_count=filter_orders_generic(orders_df,status).count()
    assert filtered_count==count