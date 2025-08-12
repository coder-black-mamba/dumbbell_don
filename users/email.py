from djoser import email

class CustomActivationEmail(email.ActivationEmail):
    template_name = "email/activation.html"
    template_name_txt = "email/activation.txt"
    subject_template_name = "email/activation_subject.txt"
