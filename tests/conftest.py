# conftest.py
import pytest
from datetime import datetime
from html import escape  # Use this for escaping HTML content

def pytest_html_report_title(report):
    report.title = "Website Test Report"

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == 'call':
        # Add extra information to the report
        additional_info = '<div class="additional-info">Additional test information</div>'
        report.extra = [escape(additional_info)]