import os

from .build_app import Base


class PreBuild:
    """
    docstring
    """

    def __init__(self, framework=str,
                 db=None,
                 name_app=str,
                 docker=False,
                 library=False):

        self.framework = framework
        self.db = db
        self.name_app = name_app
        self.docker = docker
        self.base_path = os.path.dirname(os.path.realpath(__file__))
        self.origin = None
        self.destination = None
        self.library = library

    def main(self):
        self._normalize_files()
        self._find_framework()
        self._path_destination_app()
        # enviar data validada

        _build_app = Base(self.framework,
                          self.base_path,
                          self.origin,
                          self.destination,
                          self.docker)
        _build_app.main()

    def _normalize_files(self):
        """
        cambia las extensiones de los siguientes archivos
        - readme.py - readme.md
        - requirements.py -requirements.txt
        - .env.py - .env
        - .gitignore.py - gitignore
        """
        # retrocede a la raiz del paquete
        if self.base_path.endswith('base'):
            self.base_path = self.base_path.replace('base', '')

        for r, d, f in os.walk(self.base_path):
            for files in f:
                if files.lower() == "requirements.py":
                    file_base = os.path.join(r, files)
                    file_new = file_base.replace('.py', '.txt')
                    original_extension = os.rename(file_base, file_new)

                if files.lower() == "readme.py":
                    file_base = os.path.join(r, files)
                    file_new = file_base.replace('.py', '.md')
                    original_extension = os.rename(file_base, file_new)

                if files.lower() == "env_example.py":
                    file_base = os.path.join(r, files)
                    file_new = file_base.replace(
                        'env_example.py', '.env_example')
                    original_extension = os.rename(file_base, file_new)

                if files.lower() == "gitignore.py":
                    file_base = os.path.join(r, files)
                    file_new = file_base.replace('gitignore.py', '.gitignore')
                    original_extension = os.rename(file_base, file_new)

    def _path_destination_app(self):
        app_destination = os.getcwd()
        self.destination = "{}/{}".format(app_destination, self.name_app)

    def _find_framework(self):
        """
        valida que existan los archivos del framework preconfigurado
        para crear el proyecto
        """
        self.origin = "{}{}".format(self.base_path,
                                    'framework')

        list_path = os.listdir(self.origin)
        if self.framework not in list_path:
            raise Exception(
                "skeleton for framework {} not found".format(self.framework))

    def select_db(self):
        self.db = "".join(self.db)
