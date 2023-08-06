import os
import shutil
import subprocess


class Base:
    """
    docstring
    """

    def __init__(self, framework=str,
                 base_path=str,
                 origin=str,
                 destination=str,
                 docker=False):

        self.framework = framework
        self.base_path = base_path
        self.origin = origin
        self.destination = destination
        self.docker = docker

    def main(self):
        # ordena los path de origen - destination de los proyectos
        # preconfigurados y los copia a la raiz del folder
        self._build_app()

        # valida si el proyecto requiere docker
        # toma el base_path y lo concatena con el nombre framework
        # busca los archivos y los copia al nuevo proyecto creado
        if self.docker:
            self._docker()

    def _build_app(self):
        """
        crea una copia del proyecto preconfigurado, en la raiz
        del folder
        """
        folder_framework = "{}/{}".format(self.origin, self.framework)
        try:
            shutil.copytree(folder_framework, self.destination)
            self._install_requirements(self.destination)
        except Exception:
            print("project already exists")

    def _install_requirements(self, destination):
        """Install requirememts."""
        path_req = "{}/{}".format(destination, 'requirements/requirements.txt')
        subprocess.call(['pip3 install -r {}'.format(path_req)], shell=True)

    # def _docker(self):
    #     """
    #     toma el nombre del framework y busca en los recursos los archivos
    #     del docker y los copia en la raiz del nuevo proyecto
    #     """
    #     list_path = os.listdir(self.base_path)
    #     resource = 'resource'
    #     destination = "{}/{}".format(self.destination, 'docker')
    #     if resource in list_path:
    #         resource_docker = "{}{}/{}/{}".format(self.base_path,
    #                                               resource,
    #                                               self.framework,
    #                                               'docker')

    #         try:
    #             shutil.copytree(resource_docker, destination)
    #         except Exception:
    #             print("project already exists")
