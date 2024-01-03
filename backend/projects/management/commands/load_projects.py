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
        for root, dirs, files in os.walk(folder_path):
            # Exclude backup folders from the scanning process
            dirs[:] = [d for d in dirs if not d.startswith('Backup')]

            for file in files:
                if file.endswith('.flp'):
                    project_path = os.path.join(root, file)

                    # Check if the project is already in the database
                    if not Project.objects.filter(path=project_path).exists():
                        project = pyflp.parse(project_path)

                        # Create a new project entry in the database
                        Project.objects.create(
                            name=os.path.splitext(file)[0],
                            created_on = project.created_on,
                            path = project_path,
                            artists = project.artists,
                            comments = project.comments,
                            genre = project.genre,
                            time_spent = project.time_spent
                        )

                        self.stdout.write(self.style.SUCCESS(f'Successfully added project: {project_path}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Project already exists: {project_path}'))

    def find_flp_file(self, project_path):
        # Dynamically find the project.flp file based on the project folder
        for file_name in os.listdir(project_path):
            if file_name.lower().endswith('.flp'):
                return os.path.join(project_path, file_name)
        return None
