from typing import Union
from curvenote.models import Project
import logging
import os
from shutil import copyfile
import pkg_resources

from jinja2 import Environment, PackageLoader

from ..client import Session
from .article import LatexArticle

logger = logging.getLogger()


class LatexProject:
    def __init__(self, session: Session, target_folder: str):
        self.session = session
        self.default_template_folder = os.path.join("latex", "templates", "default")
        self.target_folder = os.path.abspath(target_folder)
        self.assets_folder = os.path.join(self.target_folder, "assets")
        self.images_folder = os.path.join(self.target_folder, "assets", "images")
        self.documents_folder = os.path.join(self.target_folder, "documents")
        logger.info(f"Creating {self.images_folder}")
        os.makedirs(self.images_folder, exist_ok=True)
        logger.info(f"Creating {self.documents_folder}")
        os.makedirs(self.documents_folder, exist_ok=True)
        self.articles = []
        self.reference_list = []
        self.jinja = None
        self._configure_jinja()

    @classmethod
    def build_single_article(
        cls,
        session: Session,
        target_folder: str,
        project_id: Union[str, Project],
        article_id: str,
        version: int,
    ):
        latex_project = cls(session, target_folder)
        try:
            latex_project.add_article(project_id, article_id, version)
        except ValueError as err:
            logging.error(f"Error: {str(err)}")
            raise ValueError(
                f"Could not add article to LaTeX project: {str(err)}"
            ) from err

        try:
            logging.info(f"writing to {target_folder}")
            latex_project.write()
        except ValueError as err:
            logging.error(f"Error: {str(err)}")
            logging.error(f"Could not write final document")
            raise ValueError(f"Could not write final document") from err

    def _configure_jinja(self):
        """
        Default jinja syntax doesn't play well with LaTeX.
        Create a custom environment that does.
        http://eosrei.net/articles/2015/11/latex-templates-python-and-jinja2-generate-pdfs
        """
        self.jinja = Environment(
            block_start_string=r"\BLOCK{",
            block_end_string="}",
            variable_start_string=r"\VAR{",
            variable_end_string="}",
            comment_start_string=r"\#{",
            comment_end_string="}",
            line_statement_prefix="%%",
            line_comment_prefix="%#",
            trim_blocks=True,
            autoescape=False,
            loader=PackageLoader("curvenote", self.default_template_folder),
        )

    def add_article(
        self, project_id: Union[str, Project], article_id: str, version: int
    ):
        logging.info("add_article")
        latex_article = LatexArticle(self.session, project_id, article_id)
        logging.info("created article")
        latex_article.fetch(version)
        logging.info("fetch complete")
        latex_article.localize(self.session, self.assets_folder, self.reference_list)
        logging.info("localize complete")

        idx = len(self.articles)
        logging.info(f"number of articles {idx}")
        filename = f"{idx}_{latex_article.block.name}"
        logging.info(f"generate filename {filename}")
        self.articles.append((f"documents/{filename}", latex_article, filename))
        logging.info(f"appended article documents/{filename}")

    def render(self):
        template_assets = ["curvenote_paper.sty", "logo-horizontal-dark.png"]
        logging.info(f"Copying template assets")
        for asset in template_assets:
            src = pkg_resources.resource_filename(
                "curvenote", f"{self.default_template_folder}/{asset}"
            )
            dest = os.path.join(self.target_folder, asset)
            logging.info(f"Copying: {asset} to {dest}")
            copyfile(src, dest)

        logging.info(f"Rendering template...")
        template = self.jinja.get_template("index.tpl.tex")
        try:
            _, first_article, __ = self.articles[0]
            return template.render(
                article_paths=[p for p, *_ in self.articles],
                main_title=first_article.title,
                main_author_list=first_article.author_names,
                main_day=first_article.date.day,
                main_month=first_article.date.month,
                main_year=first_article.date.year,
                oxalink=first_article.oxalink(self.session.site_url),
            )
        except ValueError as err:
            raise ValueError("Need at least one article") from err

    def write(self):
        logging.info(f"Writing articles...")
        for (_, article, filename) in self.articles:
            article_filepath = os.path.join(self.documents_folder, filename + ".tex")
            article.write(article_filepath)

        content = self.render()

        logging.info(f"Writing index.tex...")
        with open(os.path.join(self.target_folder, "index.tex"), "w+") as file:
            file.write(content)

        logging.info(f"Writing main.bib...")
        if len(self.reference_list) > 0:
            with open(os.path.join(self.target_folder, "main.bib"), "w+") as file:
                for reference in self.reference_list:
                    file.write(f"{reference.bibtex}\n")

        logging.info(f"Done!")
