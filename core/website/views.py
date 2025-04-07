from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages


from .forms import ContactForm


class ContactCreateView(CreateView):
    """Handles the creation of a contact ticket via a form submission."""

    form_class = ContactForm
    template_name = "website/contact.html"
    success_url = reverse_lazy("website:contact")

    def form_valid(self, form):
        """Handles valid form submission and displays a success message."""
        messages.success(self.request, "Ticket submitted successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        """Handles invalid form submission and displays an error message."""
        messages.error(self.request, "Something is wrong")
        return self.render_to_response(self.get_context_data(form=form))
