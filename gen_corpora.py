import os
import sys
import argparse

def existing_dir(path):
    path = os.path.abspath(path)
    if (not os.path.exists(path)) or (not os.path.isdir(path)):
        raise ValueError("%s is not a directory" % path)
    return path

def create_parser():
    parser = argparse.ArgumentParser(description="Join *.crp files from a Scielo *.tar archive to form two parallel corpora")

    parser.add_argument("-d", "--dir", required=True, metavar="<path>", type=existing_dir, help="Untarred directory from which to parse files")

    parser.add_argument("-l", "--langs", required=True, nargs=2, metavar="xx", help="2-char ISO language codes")

    parser.add_argument("-t", "--title", default="corp", help="Optional file basename for generated corpora")

    return parser


def gen_corpora(gma_dir, source_lang, dest_lang, title="corp"):
    """
    gma_dir - Path-like object referring to a directory of files extracted from one of Mariana Neeve's Scielo *.tar archives
    source_lang - 2-char ISO language code for source language (whose sentences appear first)
    dest_lang - 2-char ISO language code for dest language (whose sentences appear second)
    Returns - a tuple of paths to both the source and the target corpora
    """

    source_corp = os.path.abspath(title + "." + source_lang)
    dest_corp = os.path.abspath(title + "." + dest_lang)

    source_lines = []
    dest_lines = []

    for entry in filter( lambda p: p.endswith(".crp"), os.listdir(gma_dir) ):
        with open( os.path.join(gma_dir, entry), "r", encoding="utf-8") as r:
            mixed_lines = r.readlines()
        i = 0
        while i < len(mixed_lines):
            source_line = mixed_lines[i + 1].strip()
            dest_line = mixed_lines[i + 2].strip()
            if source_line and dest_line:
                source_lines.append(source_line)
                dest_lines.append(dest_line) 
            i += 3

    with open(source_corp, "w", encoding="utf-8") as w:
       w.write( "\n".join(source_lines) )
    with open(dest_corp, "w", encoding="utf-8") as w:
       w.write( "\n".join(dest_lines) )

    return (source_corp, dest_corp)



if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    (source_corp, dest_corp) = gen_corpora( args.dir, args.langs[0], args.langs[1], title=args.title)
    sys.stderr.write("Generated corpora %s and %s\n" % (source_corp, dest_corp))
