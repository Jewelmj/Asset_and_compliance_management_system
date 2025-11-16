from datetime import date

from models.document import Document
from models.document_metadata import DocumentMetadata
from models.document_history import DocumentHistory

class DocumentService:
    """
    Handles business logic for documents:
    - Creating documents
    - Updating metadata
    - Checking expiry
    - Running integrity validations
    """

    def create_document(self, name, doc_type, file_path=None, issued_on=None, expires_on=None):
        metadata = DocumentMetadata(file_path=file_path,
                                    issued_on=issued_on,
                                    expires_on=expires_on)

        history = DocumentHistory()

        document = Document(name=name, doc_type=doc_type,
                            metadata=metadata, history=history)

        history.log("Document created")

        return document

    def is_expired(self, document):
        if not document.metadata.expires_on:
            return False

        return date.today() > document.metadata.expires_on

    def check_integrity(self, document):
        """
        A placeholder for integrity validation logic.
        Could check:
        - file exists
        - file not corrupted
        - metadata valid
        """

        if not document.metadata.file_path:
            document.history.log("Integrity check failed: missing file path")
            return False

        document.history.log("Integrity check passed")
        return True

    def update_file(self, document, new_path):
        document.metadata.set_file_path(new_path)
        document.history.log(f"File path updated to {new_path}")

    def update_expiry(self, document, new_expiry_date):
        document.metadata.set_expiry_date(new_expiry_date)
        document.history.log(f"Expiry date updated to {new_expiry_date}")