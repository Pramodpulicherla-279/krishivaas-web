# import pytest
# import allure
# from datetime import datetime

# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     """Attach additional information to Allure reports."""
#     outcome = yield
#     report = outcome.get_result()

#     if report.when == 'call' and report.failed:
#         # Attach failure details to Allure report
#         allure.attach(
#             body=f"Test failed: {item.name}\nReason: {call.excinfo}",
#             name="Failure Details",
#             attachment_type=allure.attachment_type.TEXT
#         )

import pytest
import allure
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Add Allure attachments for failed tests"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        allure.attach(
            body=str(item.funcargs),
            name="Test Arguments",
            attachment_type=allure.attachment_type.TEXT
        )