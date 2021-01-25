class CouldNotCreateIndexException(Exception):
	pass

class CouldNotGetDocumentException(Exception):
	pass

class CouldNotSearchDocumentsException(Exception):
	pass

class CouldNotInsertDocumentException(Exception):
	pass

class ExistingDocumentException(Exception):
    pass

class DocumentNotFoundException(Exception):
	pass