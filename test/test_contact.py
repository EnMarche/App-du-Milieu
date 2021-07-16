from app.crud import contact

class Test_Contact_IsSubscribed:
    def test_isSubscribed_1(self):
        result = contact.isSubscribed("", [''])
        assert result == False

    def test_isSubscribed_2(self):
        result = contact.isSubscribed("", ['subscribed_emails_local_host', 'subscribed_emails_movement_information', 'subscribed_emails_weekly_letter', 'subscribed_emails_referents', 'citizen_project_host_email', 'subscribed_emails_citizen_project_creation', 'deputy_email', 'candidate_email', 'senator_email'])
        assert result == False

    def test_isSubscribed_3(self):
        result = contact.isSubscribed("fake_role", ['subscribed_emails_local_host', 'subscribed_emails_movement_information', 'subscribed_emails_weekly_letter', 'subscribed_emails_referents', 'citizen_project_host_email', 'subscribed_emails_citizen_project_creation', 'deputy_email', 'candidate_email', 'senator_email'])
        assert result == False

    def test_isSubscribed_4(self):
        result = contact.isSubscribed("referent", ['subscribed_emails_local_host', 'subscribed_emails_movement_information', 'subscribed_emails_weekly_letter', 'subscribed_emails_referents', 'citizen_project_host_email', 'subscribed_emails_citizen_project_creation', 'deputy_email', 'candidate_email', 'senator_email'])
        assert result == True

    def test_isSubscribed_5(self):
        result = contact.isSubscribed("referent", ['subscribed_emails_local_host', 'subscribed_emails_movement_information', 'subscribed_emails_weekly_letter', 'citizen_project_host_email', 'subscribed_emails_citizen_project_creation', 'deputy_email', 'candidate_email', 'senator_email'])
        assert result == False

    def test_isSubscribed_6(self):
        result = contact.isSubscribed("referent", ['subscribed_emails_referents'])
        assert result == True

    def test_isSubscribed_7(self):
        result = contact.isSubscribed("referent", [''])
        assert result == False