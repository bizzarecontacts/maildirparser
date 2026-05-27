# By David Dvir , 2026

import csv
import email
import email.header
from email.policy import default
import os


def get_email_body_excerpt(msg, max_length=200):
    """Walks through the email parts to find plain text, cleans it up,

    and returns a short, flattened excerpt.
    """
    body_text = ""

    # If the message is multipart (has HTML, attachments, etc.)
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get_content_disposition())

            # Look for the plain text part and ignore attachments
            if (
                content_type == "text/plain"
                and "attachment" not in content_disposition
            ):
                try:
                    body_text = part.get_content()
                    break
                except Exception:
                    pass
    else:
        # Single part message (just plain text)
        if msg.get_content_type() == "text/plain":
            body_text = msg.get_content()

    # If we couldn't find plain text, check if there's an HTML part we can grab
    if not body_text:
        for part in msg.walk():
            if part.get_content_type() == "text/html":
                try:
                    body_text = part.get_content()
                    break
                except Exception:
                    pass

    if not body_text:
        return "[No Text Body Found]"

    # Clean up text: replace newlines/tabs with spaces so it stays on one row in the CSV
    cleaned_text = " ".join(body_text.split())

    # Truncate to the maximum length and add an ellipsis if it was cut off
    if len(cleaned_text) > max_length:
        return cleaned_text[:max_length].strip() + "..."

    return cleaned_text.strip()


def get_attachment_info(msg):
    """Walks through the email structure to detect attachments and extract their

    filenames cleanly.
    """
    has_attachment = False
    attachment_names = []

    if msg.is_multipart():
        for part in msg.walk():
            content_disposition = part.get_content_disposition()
            filename = part.get_filename()

            # Detect if this section is an attachment
            if content_disposition == "attachment" or filename:
                has_attachment = True

                if filename:
                    # Clean up and decode any complex email-header encodings in the filename
                    try:
                        decoded_chunks = email.header.decode_header(filename)
                        filename_str = "".join(
                            [
                                (
                                    chunk[0].decode(chunk[1] or "utf-8")
                                    if isinstance(chunk[0], bytes)
                                    else chunk[0]
                                )
                                for chunk in decoded_chunks
                            ]
                        )
                        attachment_names.append(filename_str)
                    except Exception:
                        attachment_names.append(filename)
                else:
                    attachment_names.append("[Unnamed Attachment]")

    # Format the list of attachments into a single string for the CSV cell
    attachments_list_str = (
        "; ".join(attachment_names) if attachment_names else "None"
    )

    return has_attachment, attachments_list_str


def parse_maildir_to_csv(maildir_folder, output_csv_path, excerpt_length=200):
    # Defined headers combining all request criteria
    headers = [
        "File Name",
        "Date",
        "From",
        "To",
        "Subject",
        "Excerpt",
        "Has Attachments",
        "Attachment Names",
        "Message-ID",
        "Size (Bytes)",
    ]

    print(f"Scanning directory: {maildir_folder}")

    with open(
        output_csv_path, mode="w", newline="", encoding="utf-8"
    ) as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)

        processed_count = 0

        # Loop through all files in the directory
        for filename in os.listdir(maildir_folder):
            file_path = os.path.join(maildir_folder, filename)

            # Process files only
            if not os.path.isfile(file_path):
                continue

            try:
                file_size = os.path.getsize(file_path)

                # Open and parse the raw email binary stream
                with open(file_path, "rb") as f:
                    msg = email.message_from_binary_file(f, policy=default)

                # Extract envelope metadata
                msg_from = msg.get("From", "N/A")
                msg_to = msg.get("To", "N/A")
                msg_subject = msg.get("Subject", "N/A")
                msg_date = msg.get("Date", "N/A")
                msg_id = msg.get("Message-ID", "N/A")

                # Parse body and attachment data
                msg_excerpt = get_email_body_excerpt(
                    msg, max_length=excerpt_length
                )
                has_attachments, attachment_names = get_attachment_info(msg)

                # Write row to CSV
                writer.writerow(
                    [
                        filename,
                        msg_date,
                        msg_from,
                        msg_to,
                        msg_subject,
                        msg_excerpt,
                        has_attachments,
                        attachment_names,
                        msg_id,
                        file_size,
                    ]
                )
                processed_count += 1

            except Exception as e:
                print(f"Error processing file {filename}: {e}")

    print(
        f"\nSuccessfully processed {processed_count} files. Output saved to: {output_csv_path}"
    )


if __name__ == "__main__":
    # --- CONFIGURATION ---
    # Change target folder path if the files are not running from the local script directory
    TARGET_FOLDER = "."
    OUTPUT_CSV = "email_triage_summary.csv"
    EXCERPT_CHARACTER_LIMIT = 200
    # ---------------------

    parse_maildir_to_csv(
        TARGET_FOLDER, OUTPUT_CSV, excerpt_length=EXCERPT_CHARACTER_LIMIT
    )