import sketch


if __name__ == "__main__":
    filename = "/Users/shravan/Desktop/simple.sketch"

    document_data = sketch.read(filename)
    print 'Document data: %s' % document_data
