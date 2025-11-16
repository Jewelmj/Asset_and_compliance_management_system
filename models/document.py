import uuid

class Document:
    """
    Pure data model representing a document related to an asset or a jobsite.
    No validation or business logic here.
    """

    def __init__(self, name, doc_type, metadata, history):
        self.document_id = str(uuid.uuid4())
        self.name = name               
        self.doc_type = doc_type      

        self.metadata = metadata        # DocumentMetadata instance
        self.history = history          # DocumentHistory instance

    def __str__(self):
        return f"Document(ID={self.document_id}, Name={self.name}, Type={self.doc_type})"