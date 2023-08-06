"""
Basic use:
    download(year)
    build(year)
    read_dataframe(year)

Helpers:
    whatis(column_name)
    locate(year)
    inspect(year)

Notes:
- prepare() is an alias to run both download(year) and build(year)
"""

from boo.year import make_url
from boo.path import locate
from boo.curl import curl
from boo.file import yield_rows, save_rows, read_df
from boo.columns import CONVERTER_FUNC, SHORT_COLUMNS
from boo.dataframe.canonic import canonic_df


def preclean(path, force: bool):
    """Delete an exisiting file if *force* flag is set to True"""
    if force is True and path.exists():
        path.unlink()


def help_force(year, verb):
    return f"Use {verb}({year}, force=True) to overwrite existing file."


def download(year: int, force=False, directory=None):
    """Download file from Rosstat web site."""
    path = locate(year, directory).raw.path
    url = make_url(year)
    preclean(path, force)
    if not path.exists():
        print(f"Downloading source file for {year} from", url)
        curl(path, url)
        print("Saved as", path)
    else:
        print("Already downloaded:", path)
        print(help_force(year, "download"))
    return path


def build(year, force=False, directory=None,
          worker=CONVERTER_FUNC,
          column_names=SHORT_COLUMNS.all):
    """Create smaller CSV file with fewer columns.
       Columns have names as in *COLUMNS_SHORT*.
       Rows will be modified by *worker* function.
    """
    loc = locate(year, directory)
    src, dst = loc.raw, loc.processed
    preclean(dst.path, force)
    if not dst.exists():
        print("Reading from", src)
        print("Saving to", dst)
        save_rows(path=dst.path,
                  stream=map(worker, yield_rows(src.path)),
                  column_names=column_names)
        print("Done")
    else:
        print("Already built:", dst)
        print(help_force(year, "build"))


def read_intermediate_df(year: int, directory=None):
    src = locate(year, directory).processed
    return read_df(src.path, SHORT_COLUMNS.dtypes)


def read_dataframe(year, directory=None):
    return canonic_df(read_intermediate_df(year, directory))
