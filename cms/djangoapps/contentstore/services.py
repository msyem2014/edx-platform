"""
Contentstore Service
"""


from django.core.exceptions import ObjectDoesNotExist
from opaque_keys.edx.locator import CourseLocator

from cms.djangoapps.models.settings.course_metadata import CourseMetadata
from xmodule.modulestore.django import modulestore


class ContentstoreService(object):
    """
    Contentstore service
    """

    def get_proctoring_escalation_email(self, course_key):
        """
        Returns the proctoring escalation email for a course, or None if not given.

        Example arguments:
        * course_key (String): 'block-v1:edX+DemoX+Demo_Course'
        """
        # Convert course key into id
        course_id = CourseLocator.from_string(course_key)
        course = modulestore().get_course(course_id)

        try:
            metadata = CourseMetadata.fetch_all(course)
        except AttributeError as err:
            raise ObjectDoesNotExist('Course not found for course_key {course_key}.') from err

        proctoring_escalation_email = metadata['proctoring_escalation_email'].get('value')
        return proctoring_escalation_email
