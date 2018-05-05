import os
import sys
import argparse
import subprocess

def existing_dir(path):
    path = os.path.abspath(path)
    if (not os.path.exists(path)) or (not os.path.isdir(path)):
        raise ValueError("%s is not a directory" % path)
    return path

def existing_file(path):
    path = os.path.abspath(path)
    if (not os.path.exists(path)) or (not os.path.isfile(path)):
        raise ValueError("%s is not a file" % path)
    return path

def create_parser():
    parser = argparse.ArgumentParser(description="Join *.crp files from a Scielo *.tar archive to form two parallel corpora")

    parser.add_argument("--tar", metavar="<path>", type=existing_file, help="TAR archive from which to parse files")
    parser.add_argument("-d", "--dir", metavar="<path>", type=existing_dir, help="Untarred directory from which to parse files")

    parser.add_argument("-l", "--langs", required=True, nargs=2, metavar="xx", help="2-char ISO language codes")

    parser.add_argument("-t", "--title", default="corp", help="Optional file basename for generated corpora")

    return parser

def untar(tar_archive):

    extracted_directory = os.path.join( os.path.basename(tar_archive).split(".")[0] )

    untarring = subprocess.Popen(["tar", "-xvf", str(tar_archive)], universal_newlines=True)
    status = untarring.wait()
    if status:
        raise RuntimeError("Untarring %s failed with exit code %d" % (tar_archive, status))

    return extracted_directory


def gen_corpora(source_lang, dest_lang, gma_dir, gma_archive, title="corp", verbose=False):
    """
    source_lang - 2-char ISO language code for source language (whose sentences appear first)
    dest_lang - 2-char ISO language code for dest language (whose sentences appear second)
    gma_dir - Path-like object referring to a directory of files extracted from one of Mariana Neeve's Scielo *.tar archives
    gma_archive - Path-like object referring to a one of Mariana Neeve's Scielo *.tar archives
    Returns - a tuple of paths to both the source and the target corpora
    """

    if not(gma_dir or gma_archive):
        raise ValueError("Must provider either directory or .tar file of .crp files")

    source_corp = os.path.abspath(title + "." + source_lang)
    dest_corp = os.path.abspath(title + "." + dest_lang)

    source_lines = []
    dest_lines = []

    if not gma_dir:
        gma_dir = untar(gma_archive)

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

    if verbose: sys.stderr.write("Generated corpora %s and %s\n" % (source_corp, dest_corp))

    return (source_corp, dest_corp)



if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    (source_corp, dest_corp) = gen_corpora( args.langs[0], args.langs[1], gma_dir=args.dir, gma_archive=args.tar, title=args.title, verbose=True)
