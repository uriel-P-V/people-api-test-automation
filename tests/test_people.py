import requests
import json
from uuid import uuid4

import pytest
from assertpy import assert_that
from config import BASE_URI


@pytest.fixture
def get_people():
    print("\nANTES DEL TEST")

    response = requests.get(BASE_URI)

    yield response.json()

    print("DESPUÉS DEL TEST")


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



def test_get_people():
    response = requests.get(BASE_URI)

    assert_that(response.status_code).is_equal_to(200)

    response_json = response.json()

    assert_that(response_json[0]["fname"]).is_equal_to("Uriel")


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