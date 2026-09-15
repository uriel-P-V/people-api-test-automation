import requests
from lxml import etree
from assertpy import assert_that


COVID_TRACKER_HOST = "http://127.0.0.1:3000"


def test_covid_cases_have_crossed_a_million():
    response = requests.get(
        f"{COVID_TRACKER_HOST}/api/v1/summary/latest"
    )

    response_xml = response.text

    tree = etree.fromstring(
        bytes(response_xml, encoding="utf8")
    )

    total_cases = tree.xpath(
        "//data/summary/total_cases"
    )[0].text

    assert_that(int(total_cases)).is_greater_than(1_000_000)


def test_covid_cases_by_region():
    response = requests.get(
        f"{COVID_TRACKER_HOST}/api/v1/summary/latest"
    )

    response_xml = response.text

    tree = etree.fromstring(
        bytes(response_xml, encoding="utf8")
    )
    get_region_cases = etree.XPath("//data//regions//total_cases")

    total_cases = tree.xpath(
        "//data/summary/total_cases"
    )[0].text

    regions = get_region_cases(tree)
    
    total_cases_by_region = 0

    for region in regions:
        total_cases_by_region += int(region.text)

    assert_that(total_cases_by_region).is_greater_than(0)



def test_create_xml():
    data = etree.Element("data")
    summary = etree.SubElement(data, "summary")

    total_cases = etree.SubElement(
        summary,
        "total_cases",
        country="Mexico"
    )

    total_cases.text = "1000000"

    xml_payload = etree.tostring(
        data,
        encoding="unicode"
    )

    headers = {
        "Content-Type": "application/xml",
        "Accept": "application/xml"
    }

    assert_that(xml_payload).contains(
    "<total_cases country=\"Mexico\">1000000</total_cases>"
)
    assert_that(headers["Content-Type"]).is_equal_to(
        "application/xml"
    )



def test_get_usa_cases():
    response = requests.get(
        f"{COVID_TRACKER_HOST}/api/v1/summary/latest"
    )

    tree = etree.fromstring(
        bytes(response.text, encoding="utf8")
    )

    usa_cases = tree.xpath(
        "//data/regions/usa/total_cases"
    )[0].text

    assert_that(int(usa_cases)).is_equal_to(15740193)



def test_get_region_by_name():
    response = requests.get(
        f"{COVID_TRACKER_HOST}/api/v1/summary/latest"
    )

    tree = etree.fromstring(
        bytes(response.text, encoding="utf8")
    )

    usa_cases = tree.xpath(
        "//data/regions/*[name='USA']/total_cases"
    )[0].text

    assert_that(int(usa_cases)).is_equal_to(15740193)



def test_xpath_with_attribute():
    xml = """
    <data>
        <region country="Mexico">
            <total_cases>1000000</total_cases>
        </region>
        <region country="USA">
            <total_cases>2000000</total_cases>
        </region>
    </data>
    """

    tree = etree.fromstring(
        bytes(xml, encoding="utf8")
    )

    usa_cases = tree.xpath(
        "//region[@country='USA']/total_cases"
    )[0].text

    assert_that(usa_cases).is_equal_to("2000000")


def test_xml_namespace():
    xml = """
    <data xmlns="http://example.com/covid">
        <summary>
            <total_cases>1000000</total_cases>
        </summary>
    </data>
    """

    tree = etree.fromstring(
        bytes(xml, encoding="utf8")
    )

    namespaces = {
        "covid": "http://example.com/covid"
    }

    total_cases = tree.xpath(
        "//covid:data/covid:summary/covid:total_cases",
        namespaces=namespaces
    )[0].text

    assert_that(total_cases).is_equal_to("1000000")

def test_serialize_xml():
    data = etree.Element("data")
    summary = etree.SubElement(data, "summary")

    total_cases = etree.SubElement(summary, "total_cases")
    total_cases.text = "1000000"

    xml_payload = etree.tostring(
        data,
        encoding="unicode"
    )


    assert_that(xml_payload).contains(
        "<total_cases>1000000</total_cases>"
    )