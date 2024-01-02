# projects/management/commands/load_projects.py

import os
from django.core.management.base import BaseCommand
from projects.models import Project
import pyflp

class Command(BaseCommand):
    help = 'Load projects from a local folder and populate the database'

    def add_arguments(self, parser):
        parser.add_argument('folder_path', nargs='?', type=str, help='Path to the local folder containing FL Studio projects')

    def handle(self, *args, **options):
        project_folder_path = options['folder_path']

        if not project_folder_path:
            self.stdout.write(self.style.ERROR('Please provide a folder path.'))
            return

        self.load_projects_from_folder(project_folder_path)

    def load_projects_from_folder(self, folder_path):
        for year_folder in os.listdir(folder_path):
            year_path = os.path.join(folder_path, year_folder)
            if os.path.isdir(year_path):
                for month_folder in os.listdir(year_path):
                    month_path = os.path.join(year_path, month_folder)
                    if os.path.isdir(month_path):
                        for project_folder in os.listdir(month_path):
                            project_path = os.path.join(month_path, project_folder)
                            if os.path.isdir(project_path):
                                # Find the project.flp file dynamically based on the project folder
                                flp_file_path = self.find_flp_file(project_path)

                                if flp_file_path:
                                    # Extract relevant information from the project file and create a Project instance
                                    project_name = project_folder
                                    project = Project.objects.create(
                                        name=project_name,
                                        project_file=flp_file_path,
                                        created_on = pyflp.parse(flp_file_path).created_on,
                                    )

                                    # Display a message for each project loaded
                                    self.stdout.write(self.style.SUCCESS(f'Successfully loaded project: {project_name}'))
                                else:
                                    self.stdout.write(self.style.WARNING(f'Project file not found for folder: {project_folder}'))

    def find_flp_file(self, project_path):
        # Dynamically find the project.flp file based on the project folder
        for file_name in os.listdir(project_path):
            if file_name.lower().endswith('.flp'):
                return os.path.join(project_path, file_name)
        return None
