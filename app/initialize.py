from .documents import WebsiteDocument, TwitterDocument, FacebookDocument, LinkedinDocument


document_classes = [WebsiteDocument, TwitterDocument, FacebookDocument, LinkedinDocument]


if __name__ == "__main__":
    for document in document_classes:
        document.init()
