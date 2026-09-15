from utils import read_file
import requests
import json
from uuid import uuid4
import random

import pytest
from assertpy import assert_that, soft_assertions
from config import BASE_URI
from jsonpath_ng import parse
from cerberus import Validator

schema = {
    "fname": {"type": "string"},
    "lname": {"type": "string"},
    "person_id": {"type": "integer"},
    "timestamp": {"type": "string"}
}

@pytest.fixture
def get_people():
    print("\nANTES DEL TEST")

    response = requests.get(BASE_URI)

    yield response.json()

@pytest.fixture
def create_data():
    payload = read_file("create_person.json")

    random_no = random.randint(0, 1000)
    payload["lname"] = f"Olabini{random_no}"

    yield payload

@pytest.fixture
def new_person():
    person = {
        "fname": "Test",
        "lname": f"Person{uuid4()}"
    }

    payload = json.dumps(person)

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.post(
        url=BASE_URI,
        data=payload,
        headers=headers
    )

    assert_that(response.status_code).is_equal_to(204)


    # Obtener el person_id de la persona recién creada
    response = requests.get(BASE_URI)
    people = response.json()

    for current_person in people:
        if (
            current_person["fname"] == person["fname"]
            and current_person["lname"] == person["lname"]
        ):
            person_id = current_person["person_id"]
            break

    yield person

    requests.delete(f"{BASE_URI}/{person_id}")

@pytest.fixture
def person_to_delete():
    person = {
        "fname": "Delete",
        "lname": f"Person{uuid4()}"
    }

    payload = json.dumps(person)

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.post(
        url=BASE_URI,
        data=payload,
        headers=headers
    )

    assert_that(response.status_code).is_equal_to(204)

    response = requests.get(BASE_URI)
    people = response.json()

    for current_person in people:
        if (
            current_person["fname"] == person["fname"]
            and current_person["lname"] == person["lname"]
        ):
            person["person_id"] = current_person["person_id"]
            break

    return person

def create_person_with_unique_last_name(body=None):
    if body is None:
        unique_last_name = f"User {uuid4()}"

        payload = json.dumps({
            "fname": "New",
            "lname": unique_last_name
        })
    else:
        unique_last_name = body["lname"]
        payload = json.dumps(body)

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.post(
        url=BASE_URI,
        data=payload,
        headers=headers
    )

    assert_that(response.status_code).is_equal_to(204)

    return unique_last_name

def test_get_people():
    response = requests.get(BASE_URI)

    response_json = response.json()

    with soft_assertions():
        assert_that(response.status_code).is_equal_to(200)
        assert_that(response_json).extracting("fname").contains("Kent")


def test_post_person():
    person = {
        "fname": "Uriel",
        "lname": f"Test{uuid4()}"
    }

    payload = json.dumps(person)

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.post(
        url=BASE_URI,
        data=payload,
        headers=headers
    )

    assert_that(response.status_code).is_equal_to(204)


def test_delete_person(person_to_delete):
    person_id = person_to_delete["person_id"]

    url = f"{BASE_URI}/{person_id}"

    response = requests.delete(url)

    assert_that(response.status_code).is_equal_to(200)

def test_put_person(new_person):
    person_id = None

    response = requests.get(BASE_URI)
    people = response.json()

    for person in people:
        if (
            person["fname"] == new_person["fname"]
            and person["lname"] == new_person["lname"]
        ):
            person_id = person["person_id"]
            break

    updated_person = {
        "fname": "John",
        "lname": f"Updated {uuid4()}"
    }

    payload = json.dumps(updated_person)

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    url = f"{BASE_URI}/{person_id}"

    response = requests.put(
        url=url,
        data=payload,
        headers=headers
    )

    assert_that(response.status_code).is_equal_to(200)


def test_new_person(new_person):
    assert_that(new_person["fname"]).is_equal_to("Test")

def test_read_json_file():
    data = read_file("create_person.json")

    assert_that(data["fname"]).is_equal_to("New")
    assert_that(data["lname"]).is_equal_to("Template")


def test_create_data_fixture(create_data):
    assert_that(create_data["fname"]).is_equal_to("New")
    assert_that(create_data["lname"]).starts_with("Olabini")


def test_person_can_be_added_with_a_json_template(create_data):
    unique_last_name = create_person_with_unique_last_name(create_data)

    response = requests.get(BASE_URI)
    peoples = response.json()
    jsonpath_expr = parse("$.[*].lname")

    result = [match.value for match in jsonpath_expr.find(peoples)]

    assert_that(result).contains(unique_last_name)

def test_read_one_operation_has_expected_schema():
    response = requests.get(f"{BASE_URI}/1")
    person = json.loads(response.text)

    validator = Validator(schema, require_all=True)
    is_valid = validator.validate(person)

    assert_that(is_valid, description=validator.errors).is_true()

def test_read_all_operation_has_expected_schema():
    response = requests.get(f"{BASE_URI}")
    persons = json.loads(response.text)

    validator = Validator(schema, require_all=True)

    with soft_assertions():
        for person in persons:
            is_valid = validator.validate(person)
            assert_that(is_valid, description=validator.errors).is_true()