import sketch


if __name__ == "__main__":
    # from sketch.models.MSRect import MSRect
    # MSRect.render()
    filename = "/Users/shravan/src/sketch/data/test.sketch"

    import tempfile
    import sqlite3
    conn = sqlite3.connect(filename)
    c = conn.cursor()

    c.execute("select value from payload where name='main'")
    payload = c.fetchone()[0]
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(payload)
        print f.name

    document_data = sketch.read(filename)
    # print 'Document data.layers: %s' % document_data

    # print '\n\n'

    page_1 = document_data.pages[0]
    # # print 'Page 1: %s' % page_1

    # print '\n\n'

    layer_group = page_1.layers[0]
    # # print 'Layer 1: %s' % layer_group

    # print '\n\n'
    rectangle_shape_layer = layer_group.layers[0]
    # print 'Rectangle shape layer: %s' % rectangle_shape_layer
    # print '\n\n'

    print "Page render: %s" % document_data.pages[0].render()

    #######################
    # print rectangle_shape_layer.path.points[2].get('curveFrom')
    # print layer_group.layers[0].get('$class')
    # print layer_group.layers[0].get('path')
    # print layer_group.layers[0].get('path').get('$class')
    # print layer_group.layers[0].get('path').get('points')
    # print layer_group.layers[0].get('path').get('points')[0].get('$class')
    # print layer_group.layers[0].get('path').get('points')[0].get('curveFrom').get("$class")
