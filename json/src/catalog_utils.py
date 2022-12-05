from dataclasses import dataclass, field
from io import StringIO, BytesIO
import json
import os
import sys
from tempfile import NamedTemporaryFile
from textwrap import dedent

from markdown import markdown
import pandas as pd
from tabulate import tabulate

from .definitions import SPACECRAFT, SC2MISSIONS, THEMATIC_AREAS


def _get_this_file_path():
    return os.path.dirname(__file__)


def get_catalog_dir():
    here = _get_this_file_path()
    return os.path.join(
        os.path.dirname(here),
        "catalog"
    )


def get_schema_path():
    here = _get_this_file_path()
    return os.path.join(
        os.path.dirname(here),
        "schema.json"
    )


def load_schema():
    with open(get_schema_path(), "r") as schema_file:
        schema = json.load(schema_file)
    return schema


@dataclass
class Product:
    product_id: str = ""
    definition: str = ""
    applicable_missions: "list[str]|None" = field(default_factory=lambda: [])
    applicable_spacecraft: "list[str]|None" = field(default_factory=lambda: [])
    thematic_areas: "list[str]|None" = field(default_factory=lambda: [])
    description: str = ""
    link_files_http: str = ""
    link_files_ftp: str = ""
    link_vires_gui: str = ""
    link_notebook: str = ""
    link_hapi: str = ""
    variables_table: str = ""
    related_resources: str = ""
    details: str = ""
    changelog: str = ""
    fast_processing: str = ""
    
    @staticmethod
    def allowed_thematic_areas():
        return THEMATIC_AREAS
    
    @staticmethod
    def allowed_spacecraft():
        return list(SC2MISSIONS.keys())
    
    def __str__(self):
        items = self.as_dict()
        items = [f"{k}:\n{v}" for k, v in items.items()]
        return "\n\n".join(items)

    def as_dict(self):
        items = {}
        for field in self.__dataclass_fields__:
            value = getattr(self, field)
            items[field] = value
        return items
    
    def as_json(self):
        return json.dumps(self.as_dict(), indent=4)

    def get_json_file(self):
        tempfile = NamedTemporaryFile()
        tempfile.write(bytes(self.as_json(), "utf-8"))
        tempfile.seek(0)
        return tempfile

    @property
    def tabulate_variables(self):
        if self.variables_table == "":
            return ""
        try:
            df = pd.read_csv(StringIO(self.variables_table))
            return tabulate(df.values, df.columns, tablefmt="pipe")
        except Exception:
            return "INVALID TABLE"

    @property
    def markdown_links(self):
        s = ""
        if any((self.link_files_http, self.link_files_ftp)):
            s += "- Files:\n"
            if self.link_files_http:
                s += f"\t- <{self.link_files_http}>\n"
            if self.link_files_ftp:
                s += f"\t- {self.link_files_ftp}\n"
        if any((self.link_vires_gui, self.link_notebook, self.link_hapi)):
            s += "- Web services:\n"
            if self.link_vires_gui:
                s += f"\t- [VirES GUI]({self.link_vires_gui})\n"
            if self.link_notebook:
                s += f"\t- [Notebook]({self.link_notebook})\n"
            if self.link_hapi:
                s += f"\t- [HAPI]({self.link_hapi})\n"
        s = s.rstrip()
        return s
    
    @property
    def markdown_preview(self):
        items = [
            f"# {self.product_id}\n\n{self.definition}",
            f"Thematic areas: {', '.join(self.thematic_areas)}",
            f"Applicable missions: {', '.join(self.applicable_missions)}",
            f"Applicable spacecraft: {', '.join(self.applicable_spacecraft)}",
            f"## Description\n\n{self.description}",
            f"## Data access\n\n{self.markdown_links}",
            f"## FAST processing\n\n{self.fast_processing if self.fast_processing else 'N/A'}",
            f"## Preview image\n\n(delivered separately)",
            f"## File contents\n\n{self.tabulate_variables if self.tabulate_variables else 'N/A'}",
            f"## More details\n\n{self.details if self.details else 'N/A'}",
            f"## Related resources\n\n{self.related_resources if self.related_resources else 'N/A'}",
            f"## Changelog\n\n{self.changelog if self.changelog else 'N/A'}",
        ]
        return "\n\n".join(items)
    
    @property
    def html_preview(self):
        return markdown(self.markdown_preview, extensions=['markdown.extensions.tables'])
    
    @classmethod
    def from_json(cls, bytestring):
        product_json = json.loads(bytestring)
        difference = set(product_json.keys()) - set(cls.__dataclass_fields__)
        if difference:
            raise TypeError(f"Mismatching product fields in supplied .json:\n{difference}")
        return cls(**product_json)
    
    @classmethod
    def from_json_file(cls, path):
        with open(path, "r") as f:
            product_json = json.load(f)
        difference = set(product_json.keys()) - set(cls.__dataclass_fields__)
        if difference:
            raise TypeError(f"Mismatching product fields in supplied .json:\n{difference}")
        return cls(**product_json)


@dataclass
class Catalog:
    products: "dict[Product]"
    
    @property
    def product_ids(self):
        return list(self.products.keys())
    
    def get_product(self, product_id):
        return self.products.get(product_id)


def load_catalog(directory=get_catalog_dir()):
    paths = os.listdir(directory)
    paths = [os.path.join(directory, p) for p in paths if ".json" in p]
    products = []
    for path in paths:
        products.append(Product.from_json_file(path))
    products = {p.product_id: p for p in products}
    return Catalog(products=products)


def dump_html_output(html_directory):
    catalog = load_catalog()
    index_items = []
    product_ids = catalog.product_ids
    product_ids.sort()
    for id in product_ids:
        index_items.append(f"<a href='{id}.html'>{id}</a><br>")
        html = catalog.get_product(id).html_preview
        with open(os.path.join(html_directory, f"{id}.html"), "w") as f:
            f.write(html)
    index_content = "\n".join(index_items)
    with open(os.path.join(html_directory, "index.html"), "w") as f:
        f.write(index_content)
