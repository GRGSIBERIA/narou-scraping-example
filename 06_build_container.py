import json
import os
import os.path
import hashlib

def make_mimetype(chapter):
    chapter_path = "./data/{}/build".format(chapter)

    with open("{}/mimetype".format(chapter_path), "w") as mimetype:
        mimetype.write("application/epub+zip")


def make_container(chapter):
    chapter_path = "./data/{}/build".format(chapter)
    metainf_path = "{}/META-INF".format(chapter_path)
    if not os.path.exists(metainf_path):
        os.mkdir(metainf_path)
    
    with open("{}/container.xml".format(metainf_path), "w") as container:
        write_str = """<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
<rootfiles>
    <rootfile full-path="package.opf" media-type="application/oebps-package+xml"/>
</rootfiles>
</container>
"""
        container.write(write_str)


def make_toc_xhtml(chapter, sections):
    toc_path = "./data/{}/build/toc.xhtml".format(chapter)

    sectiontexts = ["<li><a href=\"{}.html\">{}</a></li>".format(sec["url"].split("/")[-2], sec["name"]) for sec in sections]

    with open(toc_path, "w", encoding="utf-8") as toc:
        toctext = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html
    xmlns="http://www.w3.org/1999/xhtml"
    xmlns:epub="http://www.idpf.org/2007/ops"
    xml:lang="ja">
<head>
    <meta charset="UTF-8" />
    <title>目次</title>
</head>
<body>
    <nav epub:type="toc">
        <h1>目次</h1>
        <ol>{}</ol>
    </nav>
</body>
</html>""".format("".join(sectiontexts))
        toc.write(toctext)
    

def make_opf(chapter, sections):
    opf_path = "./data/{}/build/package.opf".format(chapter)

    with open(opf_path, "w", encoding="utf-8") as opf:
        title = "本好きの下剋上　～司書になるためには手段を選んでいられません～　{}".format(chapter)
        digest = hashlib.sha256(title.encode("utf-8")).hexdigest()

        metadata = [
            """<?xml version="1.0" encoding="UTF-8"?>""",
            """<package xmlns="http://www.idpf.org/2007/opf" version="3.0" xml:lang="ja" unique-identifier="{}" prefix="ebpaj: http://www.ebpaj.jp/">""".format(digest),
            """<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">""",
            """<dc:title id="title">{}</dc:title>""".format(title),
            """<dc:creator>香月美夜</dc:creator>""",
            """<dc:language>ja</dc:language>""",
            """<dc:identifier id="unique-id">urn:uuid:{}</dc:identifier>""".format(digest),
            """<dc:publisher>竹渕瑛一(GRGSIBERIA)</dc:publisher>"""
            """<meta refines="#title" property="file-as">ホンズキノゲコクジョウ　シショニナルタメニハシュダンヲエランデイラレマセン</meta>""",
            """<meta property="dcterms:modified">2019-10-30T00:00:00Z</meta>""",
            """<meta property="ebpaj:guide-version">1.1.3</meta>""",
            """<meta name="cover" content="cover-id" />""",
            """</metadata>"""
        ]
        manifest = [
            """<manifest>""",
            """<item media-type="image/jpeg" id="cover-id" href="cover.jpg"/>""",
            """<item media-type="text/css" id="css" href="main.css"/>""",
            """<item media-type="application/xhtml+xml" id="toc" href="toc.xhtml" properties="nav"/>""",
            """<item media-type="application/xhtml+xml" id="title" href="title.xhtml"/>""",
        ]
        spine = [
            """<spine page-progression-direction="rtl">""",
            """<itemref linear="yes" idref="title"/>""",
            """<itemref linear="yes" idref="toc"/>"""
        ]
        for section in sections:
            secid = section["url"].split("/")[-2]
            item = """<item media-type="text/html" id="p-{}" href="{}.html"/>""".format(secid, secid)
            itemref = """<itemref linear="yes" idref="p-{}"/>""".format(secid)
            manifest.append(item)
            spine.append(itemref)
        manifest.append("</manifest>")
        spine.append("</spine>")

        metastr = "\n".join(metadata)
        manistr = "\n".join(manifest)
        spinstr = "\n".join(spine)
        text = "{}\n{}\n{}\n".format(metastr, manistr, spinstr)

        opf.write(text + "</package>")


def make_title(chapter):
    title_path = "./data/{}/build/title.xhtml".format(chapter)

    with open(title_path, "w", encoding="utf-8") as title:
        s = [
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
            "<!DOCTYPE html>",
            "<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:epub=\"http://www.idpf.org/2007/ops\">",
            "<head>",
            "   <title>{}</title>".format(chapter),
            "</head>",
            "<body>",
            "   <img src=\"cover.jpg\"/>",
            "</body>",
            "</html>"
        ]
        text = "\n".join(s)
        title.write(text)


if __name__ == "__main__":
    js = json.load(open("./data/chapters.json", "r", encoding="utf-8"))

    for chapter, sections in js.items():
        make_mimetype(chapter)
        make_container(chapter)
        make_toc_xhtml(chapter, sections)
        make_opf(chapter, sections)
        make_title(chapter)