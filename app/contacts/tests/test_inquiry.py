from django.test import TestCase
from django.urls import reverse, resolve
from bikes.models import Bike


class TestInquiryURL(TestCase):
    """
    Test that template bike_details contains
    <form action="{url}" method="POST">
    """

    def test_bike_details_contains_inquiry(self):
        """
        Test that template bike_details contains
        <form action="{% url 'inquiry' %}" method="POST">
        """

        # Get all the bikes ids
        bike_ids = list(Bike.objects.values_list('id', flat=True))

        for id in bike_ids:
            url = reverse('bike_detail', args=[id])
            response = self.client.get(url)
            # Confirm that every bike details page contains <form action="{url}" method="POST">
            self.assertContains(response, f'<form action="{url}" method="POST">')
