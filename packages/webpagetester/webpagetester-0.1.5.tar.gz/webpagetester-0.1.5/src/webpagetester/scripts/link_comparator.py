import multiprocessing as mp
import click
import pathlib

from .. import __version__

found = []
not_found = []


def file_compare(c) -> bool:
    global found
    global not_found
    c = pathlib.Path(c)
    if not c.exists():
        print("No file in:", c.absolute())
    else:
        lines = []
        with c.open("r") as reader:
            lines += reader.readlines()
        for line in lines:
            link = line.replace("\n", "")

            if not link:
                continue

            if not not_found:
                return True

            if link in not_found:
                not_found.remove(link)
                found.append(link)


@click.command(help="v"+__version__)
@click.option('-t', '--target', type=click.STRING, help='Target File.')
@click.option('-c', '--compare', type=click.STRING, help='A file with a url in each line.', multiple=True)
@click.option('-o', '--out', type=click.STRING, help='A file to store or append the report.')
@click.option('-s', '--save', default=500, help='Will save the html response in a separate files.')
def compare_links(target, compare, out, save):
    global not_found
    not_found = []
    if target:
        target = pathlib.Path(target)
        if not target.exists():
            print("No file in:", target.absolute())
        else:
            lines = []
            with target.open("r") as reader:
                lines += reader.readlines()
            for line in lines:
                link = line.replace("\n", "")
                if not link:
                    continue
                if link in not_found:
                    continue
                not_found.append(link)
    for c in compare:
        if file_compare(c):
            break

    print("links that was not found (" + str(len(not_found))+"):")
    for n in not_found:
        print(n)

    if out:
        print("Creating new links Report...", end="")
        file = pathlib.Path(out)
        with file.open("w+") as writer:
            for n in not_found:
                writer.write(n)
                writer.write("\n")
        print("DONE")

    input("Press Enter to close...")

