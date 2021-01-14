"""
Contentstore Service Tests
"""


from django.core.exceptions import ObjectDoesNotExist
from opaque_keys import InvalidKeyError

from common.djangoapps.student.roles import CourseStaffRole
from common.djangoapps.student.tests.factories import UserFactory
from cms.djangoapps.contentstore.services import ContentstoreService
from cms.djangoapps.models.settings.course_metadata import CourseMetadata
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from xmodule.modulestore.tests.factories import CourseFactory


class ContentstoreServiceTests(ModuleStoreTestCase):
    """
    Tests for Contentstore Service
    """
    def setUp(self):
        super().setUp()
        self.service = ContentstoreService()
        self.course = CourseFactory.create()
        self.staff = UserFactory()
        CourseStaffRole(self.course.id).add_users(self.staff)
        self.email = 'escalation@test.com'
        self.updated_settings = {
            'proctoring_escalation_email': self.email
        }
        CourseMetadata.update_from_dict(self.updated_settings, self.course, self.staff)

    def test_get_proctoring_escalation_email(self):
        """
        Test that it returns the correct proctoring escalation email
        """
        email = self.service.get_proctoring_escalation_email(str(self.course.id))
        self.assertEqual(email, self.email)

    def test_get_proctoring_escalation_email_no_course(self):
        """
        Test that it raises an exception if the course is not found
        """
        with self.assertRaises(ObjectDoesNotExist):
            self.service.get_proctoring_escalation_email('a/b/c')

    def test_get_proctoring_escalation_email_invalid_key(self):
        """
        Test that it raises an exception if the course_key is invalid
        """
        with self.assertRaises(InvalidKeyError):
            self.service.get_proctoring_escalation_email('invalid key')
