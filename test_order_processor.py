# Characterization tests for order_processor.py
# These tests capture the CURRENT behavior of the code before refactoring 
# Purpose: ensure refactoring does not change observable behavior 

import datetime

from order_processor import proc


def assert_result(result, expected):
    assert {key: value for key, value in result.items() if key != "dt"} == expected
    datetime.datetime.fromisoformat(result["dt"])


def test_standard_order_with_two_items_and_no_discount():
    order = {
        "id": "standard-1",
        "items": [
            {"p": 10.5, "q": 2},
            {"p": 4.25, "q": 3},
        ],
    }

    result = proc(order)

    # Subtotal: 10.5*2 + 4.25*3 = 33.75; tax: 2.70; total: 36.45.
    assert_result(
        result,
        {
            "order_id": "standard-1",
            "sub": 33.75,
            "tax": 2.7,
            "total": 36.45,
            "st": "COMPLETED",
        },
    )


def test_vip_order_applies_ten_percent_discount():
    order = {"id": "vip-1", "items": [{"p": 100, "q": 1}], "c": "VIP"}

    result = proc(order)

    # Discounted subtotal: 90; tax: 7.20; total: 97.20.
    assert_result(
        result,
        {
            "order_id": "vip-1",
            "sub": 90.0,
            "tax": 7.2,
            "total": 97.2,
            "st": "COMPLETED",
        },
    )


def test_employee_order_applies_twenty_percent_discount():
    order = {"id": "employee-1", "items": [{"p": 100, "q": 1}], "c": "EMPLOYEE"}

    result = proc(order)

    # Discounted subtotal: 80; tax: 6.40; total: 86.40.
    assert_result(
        result,
        {
            "order_id": "employee-1",
            "sub": 80.0,
            "tax": 6.4,
            "total": 86.4,
            "st": "COMPLETED",
        },
    )


def test_empty_order_returns_zero_amounts_and_empty_status():
    order = {"id": "empty-1", "items": []}

    result = proc(order)

    assert_result(
        result,
        {
            "order_id": "empty-1",
            "sub": 0,
            "tax": 0,
            "total": 0,
            "st": "EMPTY",
        },
    )


def test_negative_item_quantity_is_treated_as_zero_for_calculation():
    order = {
        "id": "negative-quantity-1",
        "items": [
            {"p": 15, "q": -2},
            {"p": 4, "q": 3},
        ],
    }

    result = proc(order)

    # Negative quantity contributes zero: subtotal 12; tax: 0.96; total: 12.96.
    assert_result(
        result,
        {
            "order_id": "negative-quantity-1",
            "sub": 12.0,
            "tax": 0.96,
            "total": 12.96,
            "st": "COMPLETED",
        },
    )
