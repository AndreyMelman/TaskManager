from jinja2 import Environment, FileSystemLoader
from pathlib import Path

templates_path = Path(__file__).parent / "email"
env = Environment(loader=FileSystemLoader(templates_path))


def render_email_template(template_name: str, **kwargs) -> str:
    template = env.get_template(template_name)
    return template.render(**kwargs)


def get_welcome_subject(user_email: str) -> str:
    return render_email_template("welcome_subject.txt", user_email=user_email)


def get_welcome_body(user_email: str) -> str:
    return render_email_template("welcome_email.html", user_email=user_email)
