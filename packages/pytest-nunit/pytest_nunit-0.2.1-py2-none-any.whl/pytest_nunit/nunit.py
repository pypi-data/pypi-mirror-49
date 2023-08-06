import sys
import os
import locale
import platform
from .models.nunit import (
    TestRunType,
    TestResultType,
    TestCaseElementType,
    TestSuiteElementType,
    TestStatusType,
    TestRunStateType,
    TestSuiteTypeType,
    PropertyBagType,
    PropertyType,
    EnvironmentType,
    AssertionStatusType,
    AssertionsType,
    AssertionType,
    AttachmentsType,
    AttachmentType,
    ReasonType,
    FailureType
)
from .attrs2xml import AttrsXmlRenderer, CdataComment

FRAMEWORK_VERSION = "3.6.2"  # Nunit version this was based on
CLR_VERSION = sys.version


PYTEST_TO_NUNIT = {
    "passed": TestStatusType.Passed,
    "failed": TestStatusType.Failed,
    "skipped": TestStatusType.Skipped,
}


def _format_assertions(case):
    # TODO
    return None


def _format_attachments(case):
    if case['attachments']:
        return AttachmentsType(
                attachment=[
                    AttachmentType(filePath=k, description=v)
                    for k, v in case["attachments"].items()
                ]
            )
    else:
        return None


def _getlocale():
    # TODO: Come up with a Python 2/3 friendly way of doing this
    return 'en-US'


class NunitTestRun(object):
    """
    Convert a test report into a Nunit Test Run
    """

    def __init__(self, nunitxml):
        self.nunitxml = nunitxml

    @property
    def environment(self):
        return EnvironmentType(
            framework_version=FRAMEWORK_VERSION,
            clr_version=CLR_VERSION,
            os_version=platform.release(),
            platform=platform.system(),
            cwd=os.getcwd(),
            machine_name=platform.machine(),
            user="",  # TODO: Get sys user but only with a toggle to hide this
            user_domain="",  # TODO: Get sys user but only with a toggle to hide this
            culture=_getlocale(),
            uiculture=_getlocale(),  # TODO: Get UI? Locale
            os_architecture=platform.architecture()[0],
        )

    @property
    def test_cases(self):
        return [
            TestCaseElementType(
                id_=str(case["idref"]),
                name=nodeid,
                fullname=nodeid,
                methodname=nodeid,  # TODO : Use actual function name
                properties=PropertyBagType(
                    property=[
                        PropertyType(name=k, value=v)
                        for k, v in case["properties"].items()
                    ]
                ),
                environment=self.environment,
                settings=None,  # TODO : Add settings as optional fixture
                failure=FailureType(message=CdataComment(text=case['error']), stack_trace=CdataComment(text=case['stack-trace'])),
                reason=ReasonType(message=CdataComment(text=case['reason'])),
                output=CdataComment(text=case['reason']),
                assertions=_format_assertions(case),
                attachments=_format_attachments(case),
                classname="",  # TODO: Use host TestSuite or class if exists
                runstate=TestRunStateType.Skipped if case['outcome'] == 'skipped' else TestRunStateType.Runnable,
                seed=str(sys.flags.hash_randomization),
                result=PYTEST_TO_NUNIT.get(
                    case["outcome"], TestStatusType.Inconclusive
                ),
                label="",  # TODO : Add docstring
                site=None,
                start_time=case["start"].strftime("%Y-%m-%d %H:%M:%S.%f"),
                end_time=case["stop"].strftime("%Y-%m-%d %H:%M:%S.%f"),
                duration=case["duration"],
                asserts=0,  # TODO : Add assert count
            )
            for nodeid, case in self.nunitxml.cases.items()
        ]

    @property
    def test_suites(self):
        return [
            TestSuiteElementType(
                id_="3",  # TODO : Suite numbers
                name=self.nunitxml.suite_name,
                fullname="pytest",
                methodname="",
                classname="",
                test_suite=None,
                properties=PropertyBagType(
                    property=[PropertyType(name="python_version", value=sys.version)]
                ),
                environment=self.environment,
                settings=None,
                failure=None,
                reason=None,
                output=None,
                assertions=None,
                attachments=None,
                test_case=self.test_cases,
                runstate=TestRunStateType.Runnable,
                type_=TestSuiteTypeType.Assembly,
                testcasecount=self.nunitxml.stats["total"],
                result=TestStatusType.Passed,
                label="",
                site=None,
                start_time=self.nunitxml.suite_start_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
                end_time=self.nunitxml.suite_stop_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
                duration=self.nunitxml.suite_time_delta,
                asserts=self.nunitxml.stats["asserts"],
                total=self.nunitxml.stats["total"],
                passed=self.nunitxml.stats["passed"],
                failed=self.nunitxml.stats["failure"],
                warnings=0,
                inconclusive=0,
                skipped=self.nunitxml.stats["skipped"],
            )
        ]

    def as_test_run(self):
        return TestRunType(
            id_="2",
            testcasecount=self.nunitxml.stats["total"],
            result=TestResultType.Passed,
            start_time=self.nunitxml.suite_start_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
            end_time=self.nunitxml.suite_stop_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
            duration=int(self.nunitxml.suite_time_delta),
            total=self.nunitxml.stats["total"],
            passed=self.nunitxml.stats["passed"],
            failed=self.nunitxml.stats["failure"],
            inconclusive=0,
            skipped=self.nunitxml.stats["skipped"],
            asserts=self.nunitxml.stats["asserts"],
            command_line=" ".join(sys.argv),
            filter_=None,
            test_case=None,
            test_suite=self.test_suites,
            engine_version=FRAMEWORK_VERSION,
            clr_version=CLR_VERSION,
        )

    def generate_xml(self):
        tr = self.as_test_run()
        return AttrsXmlRenderer.render(tr, "test-run")
