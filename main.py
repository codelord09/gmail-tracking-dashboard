import pandas as pd
import smtplib
import openpyxl
import os

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from docx import Document
from email.mime.base import MIMEBase
from email import encoders

your_email = os.getenv("MAIL_SENDER_EMAIL")
your_password = os.getenv("MAIL_SENDER_APP_PASSWORD")


def get_email_body(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])


email_body_template = get_email_body("email_template.docx")


def load_contacts(file_path="contacts.xlsx"):
    contacts = pd.read_excel(file_path)
    # Clean up column names by removing leading/trailing whitespace and specific Excel-related artifacts.
    contacts.columns = contacts.columns.str.strip().str.replace("_x000d_", "", regex=False)
    return contacts


def pick_resume_file(resume_val):
    return "Neeraj_Gupta_SDE1_1_ML.pdf" if resume_val == 1 else "Neeraj_Gupta_SDE1_0_backend.pdf"


def send_email(receiver_name, company_name, job_link, receiver_email, resume_filename):
    if not your_email or not your_password:
        raise ValueError(
            "Missing mail credentials. Set MAIL_SENDER_EMAIL and MAIL_SENDER_APP_PASSWORD."
        )

    job_link = "" if pd.isna(job_link) else str(job_link)
    body = (
        email_body_template.replace("{receiver_name}", str(receiver_name))
        .replace("{company_name}", str(company_name))
        .replace("{job_link}", job_link)
    )

    # subject = "Immediate Joiner | SDE(GenAI) | IIIT Allahabad | 2+ Years Exp"
    subject = "Immediate Joiner | PineLabs x o9 | SDE(GenAI) | IIIT Allahabad | 2+ Years Exp"

    msg = MIMEMultipart()
    msg["From"] = your_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "html"))

    with open(resume_filename, "rb") as resume:  
        part = MIMEBase("application", "octet-stream")
        part.set_payload(resume.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition", f'attachment; filename="{resume_filename}"'
        )
        msg.attach(part)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(your_email, your_password)
        server.sendmail(your_email, receiver_email, msg.as_string())
    print(f"Email sent to {receiver_name} ({receiver_email}) for {company_name} with {resume_filename}.")


def main():
    contacts = load_contacts()
    for _, row in contacts.iterrows():
        resume_file = pick_resume_file(row.get("Resume", 0))
        send_email(
            row["Receiver Name"],
            row["Company Name"],
            row["Job Link"],
            row["Receiver Email"],
            resume_file,
        )


if __name__ == "__main__":
    main()
