"""
Test custom Django management commands
"""

from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

# Patch will tell us what function we want to mock
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test Commands"""

    def test_wait_for_db_ready(self, wait_for_db_check):
        """Test waiting for database if database is ready."""
        # We just the mock the function to return True
        wait_for_db_check.return_value = True

        call_command('wait_for_db')

        wait_for_db_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')    
    def test_wait_for_db_delay(self, patch_sleep, wait_for_db_delay_check):
        """Test waiting for database when getting OperationalError"""
        # Side effect is used to mock the raising error effect
        # We will call the function 6 time
        #   First two time psycopg2Error(When database is not ready) will be raise
        #   Next 3 time OperationError(when database hasn't set the test database) will be raise
        #   Then after 6th run it will return True.
        wait_for_db_delay_check.side_effect = [Psycopg2Error] * 2 + [OperationalError] * 3 + [True]
        
        call_command('wait_for_db')

        self.assertEqual(wait_for_db_delay_check.call_count, 6)

        wait_for_db_delay_check.assert_called_with(databases=['default'])
        