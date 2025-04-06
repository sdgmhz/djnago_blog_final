import threading


class EmailThread(threading.Thread):
    """Thread class for sending emails asynchronously."""

    def __init__(self, email_obj):
        """Initialize the thread with an email object."""
        threading.Thread.__init__(self)
        self.email_obj = email_obj

    def run(self):
        """Execute the email sending process when the thread starts."""
        self.email_obj.send()
